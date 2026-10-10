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


def test_index_has_voice_controls(tmp_path):
    html = make_client(tmp_path, []).get("/").text
    assert 'id="mic"' in html and 'id="voiceBtn"' in html and "vi-VN" in html


def test_cost_endpoint(tmp_path):
    c = make_client(tmp_path, [json.dumps({"noi": "Hello!"})])
    c.post("/api/chat", json={"text": "hi"})
    d = c.get("/api/chi-phi").json()
    assert d["hom_nay"]["calls"] == 1 and d["thang_nay"]["calls"] == 1 and d["da_tra_loi_hom_nay"] == 1
    assert 'id="openCost"' in c.get("/").text


def test_backup_and_restore(tmp_path):
    c = make_client(tmp_path, [json.dumps({"noi": "Chào Tân!", "ghi_nho": ["Tên là Tân"], "hoi_tham": ["Mai thi"]})])
    c.post("/api/chat", json={"text": "mình là Tân, mai thi"})
    r = c.get("/api/sao-luu")
    assert r.status_code == 200 and "attachment" in r.headers["content-disposition"]
    backup = r.content
    assert "Tên là Tân" in backup.decode("utf-8")  # chữ có dấu giữ nguyên, dễ đọc

    c2 = make_client(tmp_path / "moi", [])
    assert c2.get("/api/facts").json() == []
    assert c2.post("/api/khoi-phuc", content=backup).json() == {"ok": True}
    assert c2.get("/api/facts").json() == ["Tên là Tân"]
    assert [m["content"] for m in c2.get("/api/history").json()] == ["mình là Tân, mai thi", "Chào Tân!"]
    assert main._brain.memory.export_all()["followups"][0]["content"] == "Mai thi"


def test_restore_rejects_bad_file(tmp_path):
    c = make_client(tmp_path, [json.dumps({"noi": "x", "ghi_nho": ["Giữ lại"]})])
    c.post("/api/chat", json={"text": "hi"})
    assert c.post("/api/khoi-phuc", content=b"khong phai json").status_code == 400
    assert c.post("/api/khoi-phuc", content=b'{"facts": []}').status_code == 400
    bad = json.dumps({"phien_ban": 1, "facts": [{"content": None}]}).encode()
    assert c.post("/api/khoi-phuc", content=bad).status_code == 400
    assert c.get("/api/facts").json() == ["Giữ lại"]  # lỗi thì trí nhớ cũ còn nguyên
