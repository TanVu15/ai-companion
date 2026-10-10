"""Test máy chủ web với bộ não giả."""
import json

from fastapi.testclient import TestClient

from app import main
from app.brain import Brain
from app.memory import Memory
from tests.test_brain import FakeClient


def make_client(tmp_path, replies):
    main._brain = Brain(Memory(tmp_path / "api.db"), client=FakeClient(replies))
    return TestClient(main.app)


def test_index_served(tmp_path):
    c = make_client(tmp_path, [])
    r = c.get("/")
    assert r.status_code == 200 and "Nhắn gì đó" in r.text


def test_chat_endpoint(tmp_path):
    c = make_client(tmp_path, [json.dumps({"noi": "Hello!", "cam_xuc": "vui", "hanh_dong": "gat_dau"})])
    r = c.post("/api/chat", json={"text": "hi"})
    assert r.status_code == 200
    assert r.json() == {"noi": "Hello!", "cam_xuc": "vui", "hanh_dong": "gat_dau"}
    assert len(c.get("/api/history").json()) == 2


def test_empty_message_rejected(tmp_path):
    c = make_client(tmp_path, [])
    assert c.post("/api/chat", json={"text": "   "}).status_code == 400


def test_brain_error_returns_502(tmp_path):
    c = make_client(tmp_path, [])  # không có câu trả lời nào -> FakeClient báo lỗi
    r = c.post("/api/chat", json={"text": "hi"})
    assert r.status_code == 502
