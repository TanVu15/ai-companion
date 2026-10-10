"""Test sửa tính cách trên web: lưu riêng trong data/, về mặc định được."""
import json

from app import config
from tests.test_api import make_client


def test_sua_va_ve_mac_dinh(tmp_path, monkeypatch):
    custom = tmp_path / "data" / "persona.md"
    monkeypatch.setattr(config, "PERSONA_CUSTOM_PATH", custom)
    c = make_client(tmp_path, [json.dumps({"noi": "Ok"})])
    goc = config.PERSONA_PATH.read_text(encoding="utf-8")
    assert c.get("/api/tinh-cach").json() == {"noi_dung": goc, "tu_sua": False}
    moi = "Bạn là Bơ, nói chuyện kiểu miền Tây, hay gọi người dùng là 'bồ'."
    assert c.put("/api/tinh-cach", json={"noi_dung": moi}).status_code == 200
    assert c.get("/api/tinh-cach").json() == {"noi_dung": moi + "\n", "tu_sua": True}
    from app import main

    c.post("/api/chat", json={"text": "hi"})
    assert main._brain.client.calls[0]["system"].startswith(moi)  # dùng ngay bản mới
    c.put("/api/tinh-cach", json={"noi_dung": moi + " Thêm."})
    assert (custom.parent / "persona.md.truoc").read_text(encoding="utf-8") == moi + "\n"  # giữ bản trước
    assert c.delete("/api/tinh-cach").status_code == 200
    assert c.get("/api/tinh-cach").json()["tu_sua"] is False
    assert config.PERSONA_PATH.read_text(encoding="utf-8") == goc  # file gốc không bị đụng


def test_tinh_cach_qua_ngan_hoac_dai(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "PERSONA_CUSTOM_PATH", tmp_path / "p.md")
    c = make_client(tmp_path, [])
    assert c.put("/api/tinh-cach", json={"noi_dung": "  ngắn "}).status_code == 400
    assert c.put("/api/tinh-cach", json={"noi_dung": "a" * 20001}).status_code == 400
    assert not (tmp_path / "p.md").exists()


def test_ban_tu_sua_trong_thi_dung_goc(tmp_path, monkeypatch):
    p = tmp_path / "p.md"
    p.write_text("   \n", encoding="utf-8")
    monkeypatch.setattr(config, "PERSONA_CUSTOM_PATH", p)
    from app.brain import current_persona

    assert current_persona()[1] is False
