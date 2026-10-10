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


def test_xem_va_xoa_dieu_da_nho(tmp_path):
    c = make_client(tmp_path, [])
    main._brain.memory.add_facts(["Tên là Tân", "Thích gym", "Sai"])
    assert c.get("/api/facts").json() == ["Tên là Tân", "Thích gym", "Sai"]
    assert c.request("DELETE", "/api/facts", json={"content": "Sai"}).status_code == 200
    assert c.get("/api/facts").json() == ["Tên là Tân", "Thích gym"]
    assert c.delete("/api/facts/all").status_code == 200
    assert c.get("/api/facts").json() == []


def test_trang_chu_co_nut_xem_tri_nho(tmp_path):
    c = make_client(tmp_path, [])
    assert "Bơ nhớ gì về mình?" in c.get("/").text


def test_password_required_when_set(tmp_path, monkeypatch):
    import base64

    from app import config

    monkeypatch.setattr(config, "APP_PASSWORD", "bo123")
    c = make_client(tmp_path, [])
    r = c.get("/")
    assert r.status_code == 401 and "Basic" in r.headers["www-authenticate"]
    bad = base64.b64encode(b"tan:sai").decode()
    assert c.get("/", headers={"Authorization": f"Basic {bad}"}).status_code == 401
    good = base64.b64encode(b"tan:bo123").decode()
    assert c.get("/api/facts", headers={"Authorization": f"Basic {good}"}).status_code == 200


def test_no_password_by_default(tmp_path):
    c = make_client(tmp_path, [])
    assert c.get("/api/facts").status_code == 200
