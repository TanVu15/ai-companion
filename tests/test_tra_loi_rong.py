"""Lỗi Tân gặp ngày 2026-10-11: Bơ chỉ trả lời "...".
Nguyên nhân: model "suy nghĩ" (thinking) ăn hết max_tokens=500 nên không còn chữ nào để nói.
Các test này giả lập đúng phản hồi của API thật trong tình huống đó."""
import json
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app import config, main
from app.brain import Brain
from app.memory import Memory


def _resp(blocks, stop_reason="end_turn"):
    return SimpleNamespace(content=blocks, stop_reason=stop_reason,
                           usage=SimpleNamespace(input_tokens=10, output_tokens=500))


def _text(t):
    return SimpleNamespace(type="text", text=t)


class ScriptedClient:
    """Mỗi lần gọi lấy một phản hồi (hoặc một lỗi) theo thứ tự."""

    def __init__(self, script):
        self.script = list(script)
        self.calls = []
        self.messages = SimpleNamespace(create=self._create)

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        item = self.script.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


class BadRequest(Exception):
    status_code = 400


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "rong.db")


def test_tat_suy_nghi_va_du_cho_cho_chu(memory):
    client = ScriptedClient([_resp([_text(json.dumps({"noi": "Chào nha!"}))])])
    Brain(memory, client=client).chat("hi")
    call = client.calls[0]
    assert call["thinking"] == {"type": "disabled"}
    assert call["max_tokens"] >= 2000  # 500 là quá ít cho câu trả lời JSON nhiều mục


def test_model_khong_cho_tat_suy_nghi_thi_goi_lai(memory):
    client = ScriptedClient([
        BadRequest("thinking.type: 'disabled' is not supported for this model"),
        _resp([_text(json.dumps({"noi": "Vẫn trả lời được nè"}))]),
        _resp([_text(json.dumps({"noi": "Lần hai"}))]),
    ])
    brain = Brain(memory, client=client)
    assert brain.chat("hi").noi == "Vẫn trả lời được nè"
    assert "thinking" not in client.calls[1]
    brain.chat("nữa")
    assert "thinking" not in client.calls[2]  # nhớ luôn, không thử lại tham số bị từ chối


def test_loi_400_khac_khong_bi_nuot(memory):
    client = ScriptedClient([BadRequest("messages: roles must alternate")])
    with pytest.raises(BadRequest):
        Brain(memory, client=client).chat("hi")
    assert len(client.calls) == 1


def test_chi_co_suy_nghi_khong_co_chu_thi_bao_loi_ro(memory, tmp_path):
    thinking_only = _resp([SimpleNamespace(type="thinking", thinking="hmm...")], stop_reason="max_tokens")
    main._brain = Brain(memory, client=ScriptedClient([thinking_only]))
    r = TestClient(main.app).post("/api/chat", json={"text": "hi"}, headers={"X-Bo": "1"})
    assert r.status_code == 502
    assert "max_tokens" in r.json()["detail"] and "..." != r.json()["detail"]
    assert all(m["content"] != "..." for m in memory.recent_messages(10))  # không lưu "..." vào trí nhớ
