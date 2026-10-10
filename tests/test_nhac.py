"""Test lời nhắc theo giờ (bộ não giả)."""
import json
from datetime import datetime, timedelta

import pytest

from app import config
from app.brain import Brain, parse_reply
from app.memory import Memory
from tests.test_api import make_client
from tests.test_brain import FakeClient


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "n.db")


def fmt(dt):
    return dt.strftime("%Y-%m-%d %H:%M")


def test_parse_reminders_ignores_junk():
    r = parse_reply(json.dumps({"noi": "Ok", "nhac": [{"luc": "2026-10-10 20:00", "viec": "Gọi mẹ"}, "rác", 3]}))
    assert r.nhac == [{"luc": "2026-10-10 20:00", "viec": "Gọi mẹ"}]
    assert parse_reply(json.dumps({"noi": "Ok", "nhac": "sai"})).nhac == []
    assert "nhac" not in r.to_dict()


def test_add_reminders_validates(memory):
    now = datetime(2026, 10, 10, 18, 0)
    n = memory.add_reminders([
        {"luc": "2026-10-10 20:00", "viec": "Gọi mẹ"},
        {"luc": "2026-10-10 20:00", "viec": "gọi mẹ"},     # trùng
        {"luc": "2026-10-09 20:00", "viec": "Đã qua"},     # giờ đã qua
        {"luc": "tối nay", "viec": "Sai giờ"},
        {"luc": "2026-10-10 21:00", "viec": "  "},
    ], now=now)
    assert n == 1 and [r["viec"] for r in memory.upcoming_reminders()] == ["Gọi mẹ"]


def test_due_reminder_fires_once(memory):
    now = datetime.now()
    memory.add_reminders([{"luc": fmt(now + timedelta(minutes=30)), "viec": "Gọi mẹ"}])
    assert memory.pop_due_reminders(now) == []
    assert [r["viec"] for r in memory.pop_due_reminders(now + timedelta(minutes=31))] == ["Gọi mẹ"]
    assert memory.pop_due_reminders(now + timedelta(minutes=32)) == []


def test_chat_creates_reminder_and_brain_announces(memory):
    soon = fmt(datetime.now())  # tới giờ ngay
    client = FakeClient([json.dumps({"noi": "Ok, 8h Bơ nhắc nha!", "nhac": [{"luc": soon, "viec": "Gọi điện cho mẹ"}]})])
    brain = Brain(memory, client=client)
    brain.chat("8h tối nhắc mình gọi mẹ")
    assert "Bây giờ là" in client.calls[0]["system"]
    [r] = brain.due_reminders()
    assert r.noi == "Tới giờ rồi nè: gọi điện cho mẹ!" and r.cam_xuc == "hao_hung"
    assert memory.recent_messages(5)[-1]["content"] == r.noi  # lưu vào lịch sử
    assert brain.due_reminders() == [] and len(client.calls) == 1  # nhắc không tốn câu API


def test_reminder_endpoints(tmp_path, monkeypatch):
    c = make_client(tmp_path, [])
    from app import main

    mem = main._brain.memory
    mem.add_reminders([{"luc": fmt(datetime.now() + timedelta(hours=2)), "viec": "Đi ngủ sớm"},
                       {"luc": fmt(datetime.now()), "viec": "Uống nước"}])
    assert len(c.get("/api/nhac/sap-toi").json()) == 2
    assert [x["noi"] for x in c.get("/api/nhac").json()] == ["Tới giờ rồi nè: uống nước!"]
    [later] = c.get("/api/nhac/sap-toi").json()
    c.delete(f"/api/nhac/{later['id']}")
    assert c.get("/api/nhac/sap-toi").json() == []
    monkeypatch.setattr(config, "DEVICE_KEY", "k")
    assert c.get("/api/thiet-bi/nhac", headers={"X-Device-Key": "k"}).json() == []
