"""Test cổng cho thiết bị phần cứng (bộ não giả)."""
import json

from app import config, main
from tests.test_api import make_client


def test_device_disabled_without_key(tmp_path):
    c = make_client(tmp_path, [])
    assert c.post("/api/thiet-bi/chat", json={"text": "hi"}).status_code == 403


def test_device_wrong_key(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DEVICE_KEY", "esp-123")
    c = make_client(tmp_path, [])
    r = c.post("/api/thiet-bi/chat", json={"text": "hi"}, headers={"X-Device-Key": "sai"})
    assert r.status_code == 401


def test_device_chat_and_no_accent(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DEVICE_KEY", "esp-123")
    monkeypatch.setattr(config, "APP_PASSWORD", "bo123")  # thiết bị không cần mật khẩu web
    reply = json.dumps({"noi": "Chào Tân, hôm nay đi đâu đó? 😄", "cam_xuc": "vui", "hanh_dong": "vay_tay"})
    c = make_client(tmp_path, [reply, reply])
    h = {"X-Device-Key": "esp-123"}
    r = c.post("/api/thiet-bi/chat", json={"text": "hi"}, headers=h)
    assert r.status_code == 200 and r.json()["noi"].startswith("Chào Tân")
    r = c.post("/api/thiet-bi/chat?khong_dau=1", json={"text": "hi"}, headers=h)
    assert r.json() == {"noi": "Chao Tan, hom nay di dau do?", "cam_xuc": "vui", "hanh_dong": "vay_tay"}


def test_device_greet_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DEVICE_KEY", "esp-123")
    c = make_client(tmp_path, [])
    assert c.post("/api/thiet-bi/chao", headers={"X-Device-Key": "esp-123"}).json() == {"noi": None}


def test_bo_dau():
    assert main.bo_dau("Đà Nẵng ơi, Bơ nhớ!") == "Da Nang oi, Bo nho!"


def test_device_todos(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DEVICE_KEY", "esp-123")
    c = make_client(tmp_path, [])
    main.get_brain().memory.add_todos(["Mua sữa", "Trả sách"])
    main.get_brain().memory.done_todos(["Trả sách"])
    h = {"X-Device-Key": "esp-123"}
    assert c.get("/api/thiet-bi/viec", headers=h).json() == [{"viec": "Mua sữa"}]
    assert c.get("/api/thiet-bi/viec?khong_dau=1", headers=h).json() == [{"viec": "Mua sua"}]
    assert c.get("/api/thiet-bi/viec", headers={"X-Device-Key": "sai"}).status_code == 401
