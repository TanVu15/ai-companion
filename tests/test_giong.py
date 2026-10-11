"""Giọng AI (edge-tts): dùng hàm tổng hợp giả, KHÔNG gọi mạng Microsoft."""
import asyncio

import pytest

from app import cai_dat, config, giong
from tests.test_api import make_client


@pytest.fixture
def gia(monkeypatch, tmp_path):
    goi = []

    async def tong_hop(text, g, toc_do, cao_do):
        goi.append((text, g, toc_do, cao_do))
        return b"ID3" + text.encode("utf-8")

    monkeypatch.setattr(giong, "tong_hop", tong_hop)
    monkeypatch.setattr(config, "AM_THANH_DIR", tmp_path / "am_thanh")
    monkeypatch.setattr(config, "CAI_DAT_PATH", tmp_path / "cai_dat.json")
    monkeypatch.setattr(config, "GIONG", "vi-VN-HoaiMyNeural")
    monkeypatch.setattr(config, "TOC_DO_GIONG", 0)
    monkeypatch.setattr(config, "CAO_DO_GIONG", 8)
    return goi


def test_doc_va_luu_dem(gia):
    mp3 = asyncio.run(giong.doc("  Chào   bạn nha  "))
    assert mp3 == b"ID3" + "Chào bạn nha".encode()
    assert gia == [("Chào bạn nha", "vi-VN-HoaiMyNeural", "+0%", "+8Hz")]
    # lần hai lấy trong đệm, không gọi lại
    assert asyncio.run(giong.doc("Chào bạn nha")) == mp3 and len(gia) == 1
    # đổi giọng là file khác
    config.GIONG = "vi-VN-NamMinhNeural"
    asyncio.run(giong.doc("Chào bạn nha"))
    assert gia[-1][1] == "vi-VN-NamMinhNeural"


def test_don_bot_khi_qua_nhieu_file(gia, monkeypatch):
    monkeypatch.setattr(config, "AM_THANH_GIU", 3)
    for i in range(6):
        asyncio.run(giong.doc(f"câu {i}"))
    assert len(list(config.AM_THANH_DIR.glob("*.mp3"))) == 3


def test_loi_mang_bao_giong_loi(gia, monkeypatch):
    async def hong(*a):
        raise OSError("không có mạng")

    monkeypatch.setattr(giong, "tong_hop", hong)
    with pytest.raises(giong.GiongLoi):
        asyncio.run(giong.doc("xin chào"))
    with pytest.raises(giong.GiongLoi):
        asyncio.run(giong.doc("   "))


def test_endpoint_giong(gia, tmp_path):
    c = make_client(tmp_path, [])
    r = c.post("/api/giong", json={"text": "Meo meo"})
    assert r.status_code == 200 and r.headers["content-type"] == "audio/mpeg" and r.content == b"ID3Meo meo"
    assert c.post("/api/giong", json={"text": ""}).status_code == 503
    # thiếu header X-Bo thì bị chặn như các lệnh khác
    from fastapi.testclient import TestClient
    from app import main
    assert TestClient(main.app).post("/api/giong", json={"text": "hi"}).status_code == 403


def test_cai_dat_giong(gia):
    cai_dat.luu({"giong": "vi-VN-NamMinhNeural", "toc_do_giong": "10", "cao_do_giong": -5})
    assert (config.GIONG, config.TOC_DO_GIONG, config.CAO_DO_GIONG) == ("vi-VN-NamMinhNeural", 10, -5)
    assert giong.tham_so() == ("vi-VN-NamMinhNeural", "+10%", "-5Hz")
    for sai in [{"giong": "en-US-Bad"}, {"toc_do_giong": 99}, {"cao_do_giong": "cao"}, {"toc_do_giong": True}]:
        with pytest.raises(ValueError):
            cai_dat.luu(sai)


def test_tach_cau_doc_cau_dau_ngan_khong_mat_chu():
    import json
    import subprocess

    js = """const { boTachCauDoc: f } = require('./web/doc_to.js');
    console.log(JSON.stringify([f('Chào bạn! Hôm nay trời đẹp ghê. Bơ muốn đi chơi quá.'), f('x'.repeat(500)).join(''),
      f('a '.repeat(300)).every(s => s.length <= 220), f('   ')]))"""
    r = subprocess.run(["node", "-e", js], cwd=config.ROOT, capture_output=True, text=True)
    dau, dai, vua, rong = json.loads(r.stdout)
    assert dau == ["Chào bạn!", "Hôm nay trời đẹp ghê. Bơ muốn đi chơi quá."]  # câu đầu riêng để đọc ngay
    assert dai == "x" * 500 and vua and rong == []
