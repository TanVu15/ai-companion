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
