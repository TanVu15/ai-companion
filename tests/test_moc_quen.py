"""Test chuỗi ngày trò chuyện, mốc quen nhau và tìm trong nhật ký."""
import json
from datetime import date, datetime, timedelta

import pytest

from app.brain import Brain
from app.memory import Memory
from tests.test_api import make_client
from tests.test_brain import FakeClient


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "t.db")


def msg_on(memory, day: date, role="user", text="hi"):
    memory.conn.execute("INSERT INTO messages (role, content, created_at) VALUES (?, ?, ?)",
                        (role, text, f"{day.isoformat()} 10:00:00"))
    memory.conn.commit()


def test_chuoi_ngay(memory):
    today = date(2026, 10, 10)
    assert memory.streak(today) == 0
    for k in (1, 2, 3, 5):
        msg_on(memory, today - timedelta(days=k))
    assert memory.streak(today) == 3  # hôm nay chưa nói: tính tới hôm qua
    msg_on(memory, today)
    assert memory.streak(today) == 4
    msg_on(memory, today - timedelta(days=4), role="assistant")  # Bơ nói không tính
    assert memory.streak(today) == 4
    assert memory.stats(today)["chuoi_ngay"] == 4


def test_moc_quen(memory, monkeypatch):
    start = date.today() - timedelta(days=99)  # hôm nay là ngày thứ 100
    msg_on(memory, start)
    msg_on(memory, date.today() - timedelta(days=1))
    client = FakeClient([json.dumps({"noi": "Tròn 100 ngày rồi nè!", "cam_xuc": "vui"})])
    brain = Brain(memory, client=client)
    morning = datetime.combine(date.today(), datetime.min.time()).replace(hour=9)
    assert brain._moc_quen(morning) == 100
    assert brain._moc_quen(morning.replace(hour=6)) == 0
    monkeypatch.setattr("app.brain.datetime", type("D", (datetime,), {"now": classmethod(lambda c, tz=None: morning)}))
    r = brain.greet()
    assert r.noi == "Tròn 100 ngày rồi nè!"
    assert "tròn 100 ngày" in client.calls[0]["messages"][-1]["content"]
    assert brain._moc_quen(morning) == 0  # đã nhắc rồi


def test_khong_phai_moc(memory):
    msg_on(memory, date.today() - timedelta(days=40))
    brain = Brain(memory, client=FakeClient([]))
    assert brain._moc_quen(datetime.now().replace(hour=12)) == 0
    memory.conn.execute("DELETE FROM messages")
    msg_on(memory, date.today() - timedelta(days=729))  # tròn 2 năm
    assert brain._moc_quen(datetime.now().replace(hour=12)) == 730


def test_tim_ca_nhat_ky(tmp_path):
    c = make_client(tmp_path, [])
    from app import main

    main._brain.memory.add_diary("Đá bóng thắng 3-1")
    main._brain.memory.add_message("user", "mai đá bóng nha")
    res = c.get("/api/tim?q=da bong").json()
    assert res[0]["role"] == "nhat_ky" and res[0]["content"] == "Đá bóng thắng 3-1"
    assert any(r["role"] == "user" for r in res)
