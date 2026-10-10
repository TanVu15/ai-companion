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


class FlakyClient(FakeClient):
    """Báo lỗi `fails` lần đầu rồi mới trả lời."""

    def __init__(self, replies, error, fails):
        super().__init__(replies)
        self.error, self.fails = error, fails

    def _create(self, **kwargs):
        if self.fails > 0:
            self.fails -= 1
            self.calls.append(kwargs)
            raise self.error
        return super()._create(**kwargs)


class _StatusError(Exception):
    def __init__(self, status_code, msg="lỗi"):
        super().__init__(msg)
        self.status_code = status_code


def test_retry_on_network_error(memory):
    waits = []
    client = FlakyClient([json.dumps({"noi": "Ok"})], ConnectionError("mất mạng"), fails=2)
    r = Brain(memory, client=client, sleep=waits.append).chat("hi")
    assert r.noi == "Ok" and waits == [1, 2]


def test_no_retry_on_bad_key_and_message_rolled_back(memory):
    client = FlakyClient([], _StatusError(401), fails=5)
    with pytest.raises(_StatusError):
        Brain(memory, client=client, sleep=lambda s: None).chat("hi")
    assert len(client.calls) == 1  # sai key thì thử lại cũng vô ích
    assert memory.recent_messages(10) == []  # tin lỗi không nằm lại trong lịch sử


def test_gives_up_after_max_retries(memory, monkeypatch):
    monkeypatch.setattr(config, "API_RETRIES", 2)
    client = FlakyClient([], _StatusError(529), fails=10)
    with pytest.raises(_StatusError):
        Brain(memory, client=client, sleep=lambda s: None).chat("hi")
    assert len(client.calls) == 3


def test_friendly_errors():
    from app.brain import friendly_error

    assert "API key" in friendly_error(_StatusError(401))
    assert "hết tiền" in friendly_error(_StatusError(400, "Your credit balance is too low"))
    assert "quá tải" in friendly_error(_StatusError(529))
    assert "Mất mạng" in friendly_error(ConnectionError())


def test_usage_tracked_and_costed(memory, monkeypatch):
    from app.brain import cost_usd

    class UsageClient(FakeClient):
        def _create(self, **kwargs):
            r = super()._create(**kwargs)
            r.usage = SimpleNamespace(input_tokens=1000, output_tokens=200)
            return r

    Brain(memory, client=UsageClient([json.dumps({"noi": "a"}), json.dumps({"noi": "b"})])).chat("1")
    Brain(memory, client=UsageClient([json.dumps({"noi": "b"})])).chat("2")
    u = memory.usage_since("2000-01-01")
    assert u == {"calls": 2, "input_tokens": 2000, "output_tokens": 400}
    monkeypatch.setattr(config, "PRICE_INPUT_PER_MTOK", 1.0)
    monkeypatch.setattr(config, "PRICE_OUTPUT_PER_MTOK", 5.0)
    assert cost_usd(u) == pytest.approx(0.004)


def test_two_messages_at_once_do_not_interleave(memory):
    import threading
    import time as _time

    class SlowClient(FakeClient):
        def _create(self, **kwargs):
            _time.sleep(0.05)
            return super()._create(**kwargs)

    brain = Brain(memory, client=SlowClient([json.dumps({"noi": "A"}), json.dumps({"noi": "B"})]))
    ts = [threading.Thread(target=brain.chat, args=(t,)) for t in ("một", "hai")]
    [t.start() for t in ts]
    [t.join() for t in ts]
    roles = [m["role"] for m in memory.recent_messages(10)]
    assert roles == ["user", "assistant", "user", "assistant"]  # không bị user, user, assistant, assistant


def test_monthly_budget_stops_brain(memory, monkeypatch):
    monkeypatch.setattr(config, "MONTHLY_USD_LIMIT", 0.01)
    monkeypatch.setattr(config, "PRICE_INPUT_PER_MTOK", 1.0)
    monkeypatch.setattr(config, "PRICE_OUTPUT_PER_MTOK", 5.0)
    memory.add_usage("chat", 5000, 1000)  # = 0.005 + 0.005 = 0.01 đô
    client = FakeClient([])
    brain = Brain(memory, client=client)
    r = brain.chat("hi")
    assert "ngân sách" in r.noi and client.calls == []
    memory.add_followups(["Đi thi"])
    assert brain.greet() is None
    monkeypatch.setattr(config, "MONTHLY_USD_LIMIT", 0)  # 0 = không giới hạn
    assert not brain.over_budget()


def test_parse_ignores_text_after_json():
    r = parse_reply('{"noi": "Chào Tân", "cam_xuc": "vui"}\n(mình dùng {} cho vui)')
    assert r.noi == "Chào Tân" and r.cam_xuc == "vui"


def test_parse_cut_off_json_still_gets_noi():
    r = parse_reply('{"noi": "Hôm nay \\"vui\\" ghê", "cam_xuc": "vui", "ghi_nho": ["Thích')
    assert r.noi == 'Hôm nay "vui" ghê'


def test_background_housekeeping_does_not_block(memory, monkeypatch):
    monkeypatch.setattr(config, "HISTORY_LIMIT", 2)
    monkeypatch.setattr(config, "SUMMARY_BATCH", 2)
    for i in range(4):
        memory.add_message("user" if i % 2 == 0 else "assistant", f"tin {i}")
    client = FakeClient([json.dumps({"noi": "Ok"}), "Tóm tắt nè"])
    brain = Brain(memory, client=client, background=True)
    assert brain.chat("mới").noi == "Ok"
    with brain._lock:  # chờ việc nền xong
        pass
    import time as _t
    for _ in range(50):
        if memory.latest_summary()[0]:
            break
        _t.sleep(0.02)
    assert memory.latest_summary()[0] == "Tóm tắt nè"
