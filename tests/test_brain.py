"""Test bằng bộ não giả, không gọi API thật."""
import json
from types import SimpleNamespace

import pytest

from app import config
from app.brain import Brain, clean_history, parse_reply
from app.memory import Memory


class FakeClient:
    """Giả lập anthropic.Anthropic: trả về câu trả lời định sẵn và ghi lại yêu cầu."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []
        self.messages = SimpleNamespace(create=self._create)

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        text = self.replies.pop(0)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)])


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "test.db")


def test_parse_valid_json():
    r = parse_reply('{"noi": "Chào!", "cam_xuc": "vui", "hanh_dong": "vay_tay", "ghi_nho": ["Tên là Tân"]}')
    assert (r.noi, r.cam_xuc, r.hanh_dong, r.ghi_nho) == ("Chào!", "vui", "vay_tay", ["Tên là Tân"])


def test_parse_json_wrapped_in_text():
    r = parse_reply('Đây nè:\n```json\n{"noi": "Ok", "cam_xuc": "buon"}\n```')
    assert r.noi == "Ok" and r.cam_xuc == "buon" and r.hanh_dong == "khong"


def test_parse_unknown_emotion_falls_back():
    r = parse_reply('{"noi": "Hi", "cam_xuc": "gian_du", "hanh_dong": "bay"}')
    assert r.cam_xuc == "binh_thuong" and r.hanh_dong == "khong"


def test_parse_plain_text_still_usable():
    r = parse_reply("Xin chào bạn")
    assert r.noi == "Xin chào bạn" and r.cam_xuc == "binh_thuong"


def test_clean_history_starts_with_user_and_alternates():
    h = [
        {"role": "assistant", "content": "a"},
        {"role": "user", "content": "b"},
        {"role": "user", "content": "c"},
        {"role": "assistant", "content": "d"},
    ]
    out = clean_history(h)
    assert [m["role"] for m in out] == ["user", "assistant"]
    assert out[0]["content"] == "b\nc"


def test_chat_saves_messages_and_facts(memory):
    client = FakeClient([json.dumps({"noi": "Chào Tân!", "cam_xuc": "vui", "hanh_dong": "vay_tay",
                                     "ghi_nho": ["Tên là Tân", "Thích tập gym"]})])
    brain = Brain(memory, client=client)
    reply = brain.chat("Mình là Tân, mê tập gym")

    assert reply.noi == "Chào Tân!"
    assert memory.all_facts() == ["Tên là Tân", "Thích tập gym"]
    assert [m["role"] for m in memory.recent_messages(10)] == ["user", "assistant"]


def test_facts_are_sent_back_to_brain_next_time(memory):
    client = FakeClient([
        json.dumps({"noi": "Ok", "ghi_nho": ["Tên là Tân"]}),
        json.dumps({"noi": "Nhớ chứ, Tân!", "ghi_nho": []}),
    ])
    brain = Brain(memory, client=client)
    brain.chat("Mình tên Tân")
    brain.chat("Bạn còn nhớ tên mình không?")

    second = client.calls[1]
    assert "Tên là Tân" in second["system"]
    assert [m["role"] for m in second["messages"]] == ["user", "assistant", "user"]


def test_duplicate_facts_ignored(memory):
    memory.add_facts(["A", "A", " ", "B"])
    assert memory.all_facts() == ["A", "B"]


def test_daily_limit_stops_api_calls(memory, monkeypatch):
    monkeypatch.setattr(config, "DAILY_LIMIT", 1)
    client = FakeClient([json.dumps({"noi": "1"})])
    brain = Brain(memory, client=client)
    brain.chat("một")
    reply = brain.chat("hai")
    assert len(client.calls) == 1
    assert "mai" in reply.noi


def test_old_messages_get_summarized(memory, monkeypatch):
    monkeypatch.setattr(config, "HISTORY_LIMIT", 2)
    monkeypatch.setattr(config, "SUMMARY_BATCH", 2)
    client = FakeClient([
        json.dumps({"noi": "a1"}),                       # lượt 1: chưa đủ tin cũ
        json.dumps({"noi": "a2"}),                       # lượt 2: có 2 tin cũ -> tóm tắt
        "Tân kể chuyện tập gym.",                        # câu trả lời tóm tắt
        json.dumps({"noi": "a3"}),
    ])
    brain = Brain(memory, client=client)
    brain.chat("u1")
    assert memory.latest_summary() == ("", 0)
    brain.chat("u2")
    summary, upto = memory.latest_summary()
    assert summary == "Tân kể chuyện tập gym." and upto == 2
    assert "u1" in client.calls[2]["messages"][0]["content"]

    brain.chat("u3")
    assert "Tân kể chuyện tập gym." in client.calls[3]["system"]
    # tin 1-2 đã tóm tắt; tin 3-4 chờ lần tóm tắt sau; tin 5-6 vẫn gửi nguyên văn
    assert [m["id"] for m in memory.messages_to_summarize(2)] == [3, 4]


def test_summary_failure_does_not_break_chat(memory, monkeypatch):
    monkeypatch.setattr(config, "HISTORY_LIMIT", 1)
    monkeypatch.setattr(config, "SUMMARY_BATCH", 1)
    client = FakeClient([json.dumps({"noi": "ok"})])  # không có câu cho tóm tắt -> lỗi
    reply = Brain(memory, client=client).chat("hi")
    assert reply.noi == "ok"
    assert memory.latest_summary() == ("", 0)


def test_near_duplicate_facts_ignored(memory):
    memory.add_facts(["Thích tập gym"])
    memory.add_facts(["thích  tập gym.", "Thích Tập Gym!"])
    assert memory.all_facts() == ["Thích tập gym"]


def test_outdated_fact_is_replaced(memory):
    memory.add_facts(["Sống ở Huế", "Tên là Tân"])
    client = FakeClient([json.dumps({"noi": "Chúc mừng nhà mới!", "ghi_nho": ["Sống ở Đà Nẵng"],
                                     "quen": ["sống ở huế"]})])
    Brain(memory, client=client).chat("Mình mới chuyển ra Đà Nẵng rồi")
    assert memory.all_facts() == ["Tên là Tân", "Sống ở Đà Nẵng"]
    assert "quen" in client.calls[0]["system"]


def test_parse_bad_quen_is_ignored():
    r = parse_reply('{"noi": "Hi", "quen": "không phải danh sách"}')
    assert r.quen == []


def test_long_fact_list_gets_merged(memory, monkeypatch):
    monkeypatch.setattr(config, "FACTS_MERGE_AT", 3)
    memory.add_facts(["Thích gym", "Mê tập gym"])
    client = FakeClient([
        json.dumps({"noi": "ok", "ghi_nho": ["Tên là Tân"]}),
        'Đây: ["Thích tập gym", "Tên là Tân"]',
    ])
    Brain(memory, client=client).chat("Mình là Tân")
    assert memory.all_facts() == ["Thích tập gym", "Tên là Tân"]
    assert "Mê tập gym" in client.calls[1]["messages"][0]["content"]


def test_bad_merge_keeps_facts_and_waits(memory, monkeypatch):
    monkeypatch.setattr(config, "FACTS_MERGE_AT", 2)
    client = FakeClient([
        json.dumps({"noi": "ok", "ghi_nho": ["A", "B"]}),
        "xin lỗi, không làm được",                      # gộp lỗi -> giữ nguyên
        json.dumps({"noi": "ok2", "ghi_nho": ["C"]}),     # chưa thêm đủ 10 điều -> không gộp lại
    ])
    brain = Brain(memory, client=client)
    brain.chat("1")
    brain.chat("2")
    assert memory.all_facts() == ["A", "B", "C"]
    assert len(client.calls) == 3
