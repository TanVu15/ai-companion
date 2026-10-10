"""Test tổng kết tuần: tối Chủ nhật Bơ điểm lại tuần qua, mỗi tuần một lần."""
import json
from datetime import datetime

import pytest

from app import config
from app.brain import Brain
from app.memory import Memory
from tests.test_brain import FakeClient

SUNDAY_EVENING = datetime(2026, 10, 11, 20, 0)  # Chủ nhật


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "w.db")


def talk(memory, n):
    for i in range(n):
        memory.add_message("user", f"chuyện số {i}")


def test_recap_conditions(memory, monkeypatch):
    brain = Brain(memory, client=FakeClient([]))
    talk(memory, 4)
    assert brain._recap_week(SUNDAY_EVENING) == ""  # ít chuyện quá
    talk(memory, 1)
    assert brain._recap_week(SUNDAY_EVENING) == "2026-W41"
    assert brain._recap_week(datetime(2026, 10, 11, 10, 0)) == ""  # sáng Chủ nhật
    assert brain._recap_week(datetime(2026, 10, 10, 20, 0)) == ""  # thứ Bảy
    monkeypatch.setattr(config, "WEEKLY_RECAP", False)
    assert brain._recap_week(SUNDAY_EVENING) == ""


def test_greet_does_recap_once(memory, monkeypatch):
    talk(memory, 6)  # vừa nói chuyện xong, nhưng tổng kết tuần vẫn chào
    client = FakeClient([json.dumps({"noi": "Tuần này bạn giỏi ghê!", "cam_xuc": "vui"})])
    brain = Brain(memory, client=client)
    monkeypatch.setattr(brain, "_recap_week", lambda now=None: "" if memory.get_kv("tong_ket_tuan") else "2026-W41")
    assert brain.greet().noi == "Tuần này bạn giỏi ghê!"
    trigger = client.calls[0]["messages"][-1]["content"]
    assert "điểm lại tuần qua" in trigger and "- chuyện số 5" in trigger
    assert memory.get_kv("tong_ket_tuan") == "2026-W41"
    assert brain.greet() is None  # đã điểm lại rồi, lại vừa nói chuyện → im
    assert len(client.calls) == 1


def test_recap_not_marked_when_special_day_wins(memory, monkeypatch):
    from datetime import date

    talk(memory, 6)
    memory.add_special_days([{"ngay": date.today().strftime("%d/%m"), "viec": "Sinh nhật"}])
    brain = Brain(memory, client=FakeClient([json.dumps({"noi": "Chúc mừng!"})]))
    monkeypatch.setattr(brain, "_recap_week", lambda now=None: "2026-W41")
    brain.greet()
    assert memory.get_kv("tong_ket_tuan") == ""  # lần sau mở web mới điểm lại tuần


def test_chi_dip_khong_hoi_tham_thuong(memory):
    from datetime import timedelta

    memory.add_followups(["Đi thi"])
    old = (datetime.now() - timedelta(hours=20)).strftime("%Y-%m-%d %H:%M:%S")
    memory.conn.execute("UPDATE followups SET created_at = ?", (old,))
    memory.conn.commit()
    client = FakeClient([json.dumps({"noi": "Chúc mừng!"})])
    brain = Brain(memory, client=client)
    assert brain.greet(only_occasion=True) is None and client.calls == []  # hỏi thăm thường thì chờ mở web
    from datetime import date

    memory.add_special_days([{"ngay": date.today().strftime("%d/%m"), "viec": "Sinh nhật"}])
    assert brain.greet(only_occasion=True).noi == "Chúc mừng!"
