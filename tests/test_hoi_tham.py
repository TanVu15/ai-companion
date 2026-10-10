"""Test Bơ chủ động hỏi thăm chuyện cũ (bộ não giả, không gọi API thật)."""
import json
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app import main
from app.brain import Brain, build_system_prompt, parse_reply
from app.memory import Memory
from tests.test_brain import FakeClient


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "t.db")


def set_age(memory, table, hours):
    """Giả vờ mọi dòng trong bảng được tạo cách đây `hours` giờ."""
    t = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    memory.conn.execute(f"UPDATE {table} SET created_at = ?", (t,))
    memory.conn.commit()


def reply(noi="Ok", **extra):
    return json.dumps({"noi": noi, "cam_xuc": "vui", "hanh_dong": "khong", **extra})


def test_parse_followup_fields():
    r = parse_reply(reply(hoi_tham=["Chiều nay tập chân"], da_hoi=["Thi toán"]))
    assert r.hoi_tham == ["Chiều nay tập chân"] and r.da_hoi == ["Thi toán"]
    assert "hoi_tham" not in r.to_dict()  # giao diện không thấy mục nội bộ


def test_followup_waits_then_expires(memory):
    memory.add_followups(["Chiều nay tập chân", "chiều nay tập chân."])  # trùng → 1
    assert memory.pending_followups(min_hours=3) == []  # mới kể, chưa hỏi
    set_age(memory, "followups", 20)
    assert [f["content"] for f in memory.pending_followups(min_hours=3)] == ["Chiều nay tập chân"]
    set_age(memory, "followups", 24 * 8)
    assert memory.pending_followups(min_hours=3) == []  # quá 7 ngày thì thôi


def test_done_followup_removed(memory):
    memory.add_followups(["Đi phỏng vấn"])
    memory.done_followups(["đi phỏng vấn"])
    assert memory.pending_followups(min_hours=0) == []


def test_prompt_lists_followups_with_day():
    now = datetime(2026, 10, 10, 9, 0)
    p = build_system_prompt("Bơ", [], followups=[{"content": "Tập chân", "created_at": "2026-10-09 17:00:00"}], now=now)
    assert "## Chuyện nên hỏi thăm" in p and "Tập chân (kể hôm qua)" in p and "09:00 (buổi sáng), thứ Bảy ngày 10/10/2026" in p
    assert "## Chuyện nên hỏi thăm" not in build_system_prompt("Bơ", [], now=now)


def test_chat_saves_and_marks_followups(memory):
    client = FakeClient([reply(hoi_tham=["Chiều nay tập chân"]), reply("Tập chân sao rồi?", da_hoi=["Chiều nay tập chân"])])
    brain = Brain(memory, client=client)
    brain.chat("chiều nay mình tập chân")
    set_age(memory, "followups", 20)
    brain.chat("hello")
    assert "Chiều nay tập chân" in client.calls[1]["system"]
    assert memory.pending_followups(min_hours=0) == []


def test_greet_asks_after_long_gap(memory):
    memory.add_message("user", "chiều nay mình tập chân")
    memory.add_message("assistant", "Cố lên!")
    memory.add_followups(["Chiều nay tập chân"])
    set_age(memory, "messages", 20)
    set_age(memory, "followups", 20)
    client = FakeClient([reply("Hôm qua tập chân sao rồi?", da_hoi=["Chiều nay tập chân"])])
    r = Brain(memory, client=client).greet()
    assert r.noi == "Hôm qua tập chân sao rồi?"
    msgs = client.calls[0]["messages"]
    assert msgs[-1]["role"] == "user" and "vừa mở ứng dụng" in msgs[-1]["content"]
    # Tin nhắn kích hoạt không lưu vào lịch sử, chỉ lưu lời Bơ
    assert memory.recent_messages(10)[-1] == {"role": "assistant", "content": "Hôm qua tập chân sao rồi?"}
    assert memory.pending_followups(min_hours=0) == []


def test_greet_silent_when_nothing_or_recent(memory):
    client = FakeClient([])
    brain = Brain(memory, client=client)
    assert brain.greet() is None  # chưa có chuyện gì để hỏi
    memory.add_followups(["Đi thi"])
    set_age(memory, "followups", 20)
    memory.add_message("user", "hi")  # vừa nói chuyện xong
    assert brain.greet() is None
    assert client.calls == []  # không tốn câu API nào


def test_greet_endpoint(tmp_path):
    mem = Memory(tmp_path / "api.db")
    main._brain = Brain(mem, client=FakeClient([reply("Thi sao rồi?")]))
    c = TestClient(main.app, headers={"X-Bo": "1"})
    assert c.post("/api/chao").json() == {"noi": None}
    mem.add_followups(["Đi thi"])
    set_age(mem, "followups", 20)
    assert c.post("/api/chao").json()["noi"] == "Thi sao rồi?"


def test_prompt_has_weekday_and_time_of_day():
    p = build_system_prompt("Bơ", [], now=datetime(2026, 10, 10, 23, 30))  # thứ Bảy
    assert "23:30 (khuya), thứ Bảy ngày 10/10/2026" in p
    p = build_system_prompt("Bơ", [], now=datetime(2026, 10, 11, 7, 5))
    assert "(buổi sáng), Chủ nhật" in p


def test_greet_after_days_away_without_followups(memory):
    memory.add_message("user", "bye")
    set_age(memory, "messages", 24 * 3)
    client = FakeClient([reply("Ơ 3 ngày rồi không thấy, khỏe không?")])
    brain = Brain(memory, client=client)
    assert brain.greet().noi.startswith("Ơ 3 ngày")
    assert "3 ngày không nói chuyện" in client.calls[0]["messages"][-1]["content"]
    assert brain.greet() is None  # vừa chào xong, mở lại web không chào lặp (không tốn thêm API)


def test_no_miss_greeting_for_new_user_or_short_gap(memory):
    brain = Brain(memory, client=FakeClient([]))
    assert brain.greet() is None  # chưa nói chuyện bao giờ
    memory.add_message("user", "hi")
    set_age(memory, "messages", 20)  # 20 giờ < 2 ngày
    assert brain.greet() is None


def test_reminder_message_not_counted_as_conversation(memory):
    memory.add_message("user", "hi")
    set_age(memory, "messages", 24 * 3)
    memory.add_message("assistant", "Tới giờ rồi nè: uống nước!", tu_dong=True)
    brain = Brain(memory, client=FakeClient([reply("Lâu quá ta!")]))
    assert brain.greet().noi == "Lâu quá ta!"
