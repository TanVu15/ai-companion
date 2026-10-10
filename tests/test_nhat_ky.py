"""Test nhật ký ngày: Bơ ghi một dòng khi Tân kể chuyện trong ngày."""
import json
from datetime import date, datetime

import pytest

from app.brain import Brain, build_system_prompt, parse_reply
from app.memory import Memory
from tests.test_api import make_client
from tests.test_brain import FakeClient


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "t.db")


def reply(noi="Ok", **extra):
    return json.dumps({"noi": noi, "cam_xuc": "vui", "hanh_dong": "khong", **extra})


def test_parse_nhat_ky():
    assert parse_reply(reply(nhat_ky="  Đi đá  bóng, thắng 3-1 ")).nhat_ky == "Đi đá bóng, thắng 3-1"
    assert parse_reply(reply(nhat_ky=["rác"])).nhat_ky == ""
    assert "nhat_ky" not in parse_reply(reply(nhat_ky="x")).to_dict()


def test_them_trung_gioi_han(memory):
    d = date(2026, 10, 10)
    assert memory.add_diary("Đi đá bóng", d)
    assert not memory.add_diary("đi đá bóng.", d)  # trùng
    assert not memory.add_diary("   ", d)
    assert memory.add_diary("Đi đá bóng", date(2026, 10, 11))  # ngày khác thì được
    for i in range(20):
        memory.add_diary(f"Việc {i}", d)
    assert len(memory.diary_recent(d, 1)) == Memory.DIARY_PER_DAY


def test_gan_day_va_theo_ngay(memory):
    for day, text in [(date(2026, 10, 1), "Cũ"), (date(2026, 10, 8), "A"), (date(2026, 10, 10), "B"),
                      (date(2026, 10, 10), "C")]:
        memory.add_diary(text, day)
    assert [x["noi_dung"] for x in memory.diary_recent(date(2026, 10, 10), 3)] == ["A", "B", "C"]
    days = memory.diary_days(limit=2)
    assert [d["ngay"] for d in days] == ["2026-10-10", "2026-10-08"]
    assert [x["noi_dung"] for x in days[0]["dong"]] == ["B", "C"]
    assert [d["ngay"] for d in memory.diary_days(before="2026-10-08")] == ["2026-10-01"]
    memory.delete_diary(days[0]["dong"][0]["id"])
    assert [x["noi_dung"] for x in memory.diary_days()[0]["dong"]] == ["C"]


def test_prompt_nhat_ky():
    now = datetime(2026, 10, 10, 20, 0)
    p = build_system_prompt("P", [], now=now, diary=[
        {"ngay": "2026-10-09", "noi_dung": "Đi phỏng vấn"}, {"ngay": "2026-10-10", "noi_dung": "Đá bóng"},
        {"ngay": "2026-10-10", "noi_dung": "Ăn phở"}])
    assert "## Nhật ký mấy ngày gần đây" in p
    assert "- hôm qua (09/10): Đi phỏng vấn" in p and "- hôm nay: Đá bóng; Ăn phở" in p
    assert "Nhật ký mấy ngày gần đây (" not in build_system_prompt("P", [], now=now)


def test_chat_ghi_nhat_ky(memory):
    client = FakeClient([reply("Đỉnh!", nhat_ky="Đá bóng thắng 3-1"), reply("Ừ")])
    brain = Brain(memory, client=client)
    brain.chat("hôm nay mình đá bóng thắng 3-1")
    assert [x["noi_dung"] for x in memory.diary_recent()] == ["Đá bóng thắng 3-1"]
    brain.chat("hôm nay mình làm gì nhỉ")
    assert "- hôm nay: Đá bóng thắng 3-1" in client.calls[1]["system"]


def test_api_nhat_ky_va_sao_luu(tmp_path):
    c = make_client(tmp_path, [])
    from app import main

    main._brain.memory.add_diary("Đi chơi")
    data = c.get("/api/nhat-ky").json()
    assert data[0]["ngay"] == date.today().isoformat() and data[0]["dong"][0]["noi_dung"] == "Đi chơi"
    assert c.get("/api/nhat-ky?truoc=xau").status_code == 400
    backup = c.get("/api/sao-luu").json()
    assert backup["diary"][0]["content"] == "Đi chơi"
    assert c.delete(f"/api/nhat-ky/{data[0]['dong'][0]['id']}").status_code == 200
    assert c.get("/api/nhat-ky").json() == []
    c.post("/api/khoi-phuc", json=backup)
    assert c.get("/api/nhat-ky").json()[0]["dong"][0]["noi_dung"] == "Đi chơi"
