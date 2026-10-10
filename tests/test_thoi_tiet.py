"""Test thời tiết với dữ liệu giả (không gọi mạng thật)."""
import json

from app.brain import Brain, build_system_prompt
from app.memory import Memory
from app.thoi_tiet import ThoiTiet, tom_tat
from tests.test_brain import FakeClient

GEO = {"results": [{"name": "Đà Nẵng", "latitude": 16.07, "longitude": 108.22}]}
FORECAST = {
    "current": {"temperature_2m": 29.6, "weather_code": 61},
    "daily": {"temperature_2m_min": [24.2, 23.8], "temperature_2m_max": [31.4, 30.1],
              "precipitation_probability_max": [80, 20], "weather_code": [63, 2]},
}


class FakeHttp:
    def __init__(self, fail=False):
        self.calls, self.fail = [], fail

    def __call__(self, url, params):
        self.calls.append(url)
        if self.fail:
            raise ConnectionError("mất mạng")
        return GEO if "geocoding" in url else FORECAST


def test_tom_tat():
    assert tom_tat("Đà Nẵng", FORECAST) == (
        "Thời tiết ở Đà Nẵng: bây giờ 30°C, mưa nhẹ; hôm nay 24–31°C, mưa vừa, khả năng mưa 80%; "
        "ngày mai 24–30°C, có mây, khả năng mưa 20%."
    )
    assert tom_tat("X", {}) is None
    assert tom_tat("X", {"daily": {"temperature_2m_min": [None]}}) is None  # dữ liệu lạ không làm sập


def test_nho_ket_qua_mot_gio():
    t = [0.0]
    http = FakeHttp()
    w = ThoiTiet("Da Nang", get=http, clock=lambda: t[0])
    assert "Đà Nẵng" in w.hien_tai()
    w.hien_tai()
    assert len(http.calls) == 2  # tọa độ + dự báo, lần 2 dùng lại
    t[0] = 3601
    w.hien_tai()
    assert len(http.calls) == 3  # hết 1 giờ: hỏi dự báo lại, tọa độ thì nhớ luôn


def test_mat_mang_khong_sao():
    t = [0.0]
    http = FakeHttp(fail=True)
    w = ThoiTiet("Da Nang", get=http, clock=lambda: t[0])
    assert w.hien_tai() is None
    w.hien_tai()
    assert len(http.calls) == 1  # lỗi thì 10 phút sau mới thử lại
    assert ThoiTiet("", get=http).hien_tai() is None


def test_khong_tim_thay_thanh_pho():
    w = ThoiTiet("Xyzabc", get=lambda url, p: {})
    assert w.hien_tai() is None


def test_bo_nao_dua_thoi_tiet_vao(tmp_path):
    w = ThoiTiet("Da Nang", get=FakeHttp())
    client = FakeClient([json.dumps({"noi": "Nhớ mang áo mưa nha"})])
    Brain(Memory(tmp_path / "w.db"), client=client, weather=w).chat("mình sắp ra ngoài")
    assert "Thời tiết ở Đà Nẵng" in client.calls[0]["system"]
    assert "Thời tiết" not in build_system_prompt("Bơ", [])


def test_suc_khoe_bao_thoi_tiet(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient

    from app import config, main

    monkeypatch.setattr(config, "THANH_PHO", "Xyzabc")
    w = ThoiTiet("Xyzabc", get=lambda url, p: {})
    main._brain = Brain(Memory(tmp_path / "h.db"), client=FakeClient([]), weather=w)
    c = TestClient(main.app)

    def row():
        return [k for k in c.get("/api/suc-khoe").json()["kiem_tra"] if k["ten"] == "Thời tiết"][0]

    assert row()["ok"] is True and "sẽ lấy" in row()["ghi_chu"]
    w.hien_tai()
    r = row()
    assert r["muc"] == "canh_bao" and "Không tìm thấy thành phố" in r["ghi_chu"]
    w2 = ThoiTiet("Da Nang", get=FakeHttp())
    main._brain.weather = w2
    w2.hien_tai()
    assert row()["ghi_chu"].startswith("Thời tiết ở Đà Nẵng")


def test_weather_code_ngan_hon_khong_sap():
    d = {"daily": {"temperature_2m_min": [20, 21], "temperature_2m_max": [30, 31], "weather_code": [1]}}
    assert tom_tat("X", d) == "Thời tiết ở X: hôm nay 20–30°C, ít mây; ngày mai 21–31°C."


def test_lay_thoi_tiet_ngoai_khoa(tmp_path):
    seen = []

    class W:
        def hien_tai(self):
            seen.append(brain._lock._is_owned())
            return "Thời tiết ở X: nắng."

    brain = Brain(Memory(tmp_path / "k.db"), client=FakeClient([json.dumps({"noi": "Ok"})]), weather=W())
    brain.chat("hi")
    assert seen == [False]
