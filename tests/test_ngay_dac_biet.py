"""Test ngày đặc biệt: Bơ nhớ sinh nhật/kỷ niệm và chúc đúng ngày (một lần mỗi năm)."""
import json
from datetime import date, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app import main
from app.brain import Brain, build_system_prompt, parse_reply
from app.memory import Memory
from tests.test_brain import FakeClient


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "t.db")


def reply(noi="Ok", **extra):
    return json.dumps({"noi": noi, "cam_xuc": "vui", "hanh_dong": "khong", **extra})


def today_ddmm(delta=0):
    return (date.today() + timedelta(days=delta)).strftime("%d/%m")


def test_parse_and_save(memory):
    r = parse_reply(reply(ngay_dac_biet=[{"ngay": "5/3", "viec": "Sinh nhật Tân"}, "rác"]))
    assert r.ngay_dac_biet == [{"ngay": "5/3", "viec": "Sinh nhật Tân"}]
    assert "ngay_dac_biet" not in r.to_dict()
    added = memory.add_special_days(r.ngay_dac_biet + [
        {"ngay": "05/03", "viec": "sinh nhật tân"},  # trùng
        {"ngay": "31/02", "viec": "Ngày sai"},
        {"ngay": "", "viec": "Không ngày"},
        {"ngay": "29/02", "viec": "Sinh nhật bạn Nhuận"},
        {"ngay": "1-12", "viec": "Kỷ niệm"},
    ])
    assert added == 3
    assert [(d["ngay"], d["viec"]) for d in memory.special_days()] == [
        ("29/02", "Sinh nhật bạn Nhuận"), ("05/03", "Sinh nhật Tân"), ("01/12", "Kỷ niệm")]


def test_today_and_leap_day(memory):
    memory.add_special_days([{"ngay": "29/02", "viec": "Nhuận"}, {"ngay": "28/02", "viec": "Hai tám"}])
    assert [d["viec"] for d in memory.special_days_today(date(2027, 2, 28))] == ["Nhuận", "Hai tám"]
    assert [d["viec"] for d in memory.special_days_today(date(2028, 2, 28))] == ["Hai tám"]
    assert [d["viec"] for d in memory.special_days_today(date(2028, 2, 29))] == ["Nhuận"]


def test_prompt_has_special_section():
    p = build_system_prompt("Bơ", [], special=[{"id": 1, "viec": "Sinh nhật Tân"}], now=datetime(2026, 3, 5, 9))
    assert "## Hôm nay là ngày đặc biệt\n- Sinh nhật Tân" in p
    assert "ngày đặc biệt\n" not in build_system_prompt("Bơ", [], now=datetime(2026, 3, 5, 9))


def test_chat_wishes_once_per_year(memory):
    memory.add_special_days([{"ngay": today_ddmm(), "viec": "Sinh nhật Tân"}, {"ngay": today_ddmm(1), "viec": "Mai"}])
    client = FakeClient([reply("Chúc mừng sinh nhật!"), reply("Ừ")])
    brain = Brain(memory, client=client)
    brain.chat("hi")
    assert "Sinh nhật Tân" in client.calls[0]["system"] and "- Mai" not in client.calls[0]["system"]
    brain.chat("hi nữa")
    assert "ngày đặc biệt\n" not in client.calls[1]["system"]  # đã chúc rồi
    assert memory.special_days_today() == []
    assert len(memory.special_days_today(only_unwished=False)) == 1


def test_chat_saves_new_special_day(memory):
    brain = Brain(memory, client=FakeClient([reply(ngay_dac_biet=[{"ngay": "20/11", "viec": "Sinh nhật mẹ"}])]))
    brain.chat("sinh nhật mẹ mình 20/11")
    assert memory.special_days()[0]["viec"] == "Sinh nhật mẹ"


def test_greet_on_special_day_even_if_recent(memory):
    memory.add_message("user", "hi")  # vừa nói chuyện xong
    memory.add_special_days([{"ngay": today_ddmm(), "viec": "Kỷ niệm 1 năm quen Bơ"}])
    client = FakeClient([reply("Chúc mừng kỷ niệm!")])
    brain = Brain(memory, client=client)
    assert brain.greet().noi == "Chúc mừng kỷ niệm!"
    assert "ngày đặc biệt" in client.calls[0]["messages"][-1]["content"]
    assert brain.greet() is None  # đã chúc rồi, lại vừa nói chuyện → im


def test_api_list_delete_and_backup(tmp_path):
    main._brain = Brain(Memory(tmp_path / "a.db"), client=FakeClient([]))
    c = TestClient(main.app, headers={"X-Bo": "1"})
    main._brain.memory.add_special_days([{"ngay": "20/11", "viec": "Sinh nhật mẹ"}])
    lst = c.get("/api/ngay-dac-biet").json()
    assert [d["viec"] for d in lst] == ["Sinh nhật mẹ"]
    backup = c.get("/api/sao-luu").json()
    assert backup["special_days"][0]["day"] == "11-20"
    assert c.delete(f"/api/ngay-dac-biet/{lst[0]['id']}").status_code == 200
    assert c.get("/api/ngay-dac-biet").json() == []
    assert c.post("/api/khoi-phuc", json=backup).status_code == 200
    assert [d["viec"] for d in c.get("/api/ngay-dac-biet").json()] == ["Sinh nhật mẹ"]
