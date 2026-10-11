"""Cài đặt trên web: lưu data/cai_dat.json, ưu tiên hơn .env, sai thì báo lỗi dễ hiểu."""
import pytest
from fastapi.testclient import TestClient

from app import cai_dat, config, main
from app.brain import Brain
from app.memory import Memory
from tests.test_brain import FakeClient


@pytest.fixture
def c(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CAI_DAT_PATH", tmp_path / "cai_dat.json")
    monkeypatch.setattr(cai_dat, "MAC_DINH", {"thanh_pho": "", "gio_yen_lang": "23-6", "tong_ket_tuan": True,
                                                  "chuc_le": True, "nhac_thoi_quen": "20:30"})
    for attr in ("THANH_PHO", "GIO_YEN_LANG", "WEEKLY_RECAP", "CHUC_LE", "NHAC_THOI_QUEN"):
        monkeypatch.setattr(config, attr, getattr(config, attr))  # trả lại như cũ sau test
    main._brain = Brain(Memory(tmp_path / "a.db"), client=FakeClient([]))
    return TestClient(main.app, headers={"X-Bo": "1"})


def test_kiem_tra():
    assert cai_dat.kiem_tra("gio_yen_lang", " 22h - 7h ") == "22-7"
    assert cai_dat.kiem_tra("gio_yen_lang", "") == ""
    assert cai_dat.kiem_tra("thanh_pho", "  Da   Nang ") == "Da Nang"
    for k, v in [("gio_yen_lang", "25-6"), ("gio_yen_lang", "5-5"), ("gio_yen_lang", "tối"),
                 ("tong_ket_tuan", "1"), ("thanh_pho", 3), ("la", 1), ("thanh_pho", "x" * 61)]:
        with pytest.raises(ValueError):
            cai_dat.kiem_tra(k, v)


def test_mac_dinh_lay_tu_env(c):
    d = c.get("/api/cai-dat").json()
    assert d == {"hien_tai": {"thanh_pho": "", "gio_yen_lang": "23-6", "tong_ket_tuan": True, "chuc_le": True,
                              "nhac_thoi_quen": "20:30"},
                 "da_chinh": []}


def test_luu_va_ap_dung(c):
    r = c.put("/api/cai-dat", json={"gio_yen_lang": "22-7", "tong_ket_tuan": False})
    assert r.status_code == 200
    assert r.json()["hien_tai"]["gio_yen_lang"] == "22-7" and r.json()["da_chinh"] == ["gio_yen_lang", "tong_ket_tuan"]
    assert config.GIO_YEN_LANG == "22-7" and config.WEEKLY_RECAP is False
    assert c.get("/api/suc-khoe").json()["gio_yen_lang"] == "22-7"
    # sai một mục thì không lưu gì
    assert c.put("/api/cai-dat", json={"gio_yen_lang": "1-2", "tong_ket_tuan": "bật"}).status_code == 400
    assert config.GIO_YEN_LANG == "22-7"
    # về mặc định
    d = c.delete("/api/cai-dat").json()
    assert d["hien_tai"]["gio_yen_lang"] == "23-6" and d["da_chinh"] == []
    assert config.WEEKLY_RECAP is True


def test_doi_thanh_pho_tao_lai_thoi_tiet(c):
    assert main._brain.weather is None
    c.put("/api/cai-dat", json={"thanh_pho": "Da Nang"})
    assert main._brain.weather is not None and main._brain.weather.thanh_pho == "Da Nang"
    c.put("/api/cai-dat", json={"thanh_pho": ""})
    assert main._brain.weather is None


def test_file_hong_thi_dung_env(c):
    config.CAI_DAT_PATH.write_text("{hỏng", encoding="utf-8")
    assert c.get("/api/cai-dat").json()["da_chinh"] == []
    config.CAI_DAT_PATH.write_text('{"gio_yen_lang": "99-1", "thanh_pho": "Hue"}', encoding="utf-8")
    assert c.get("/api/cai-dat").json()["hien_tai"]["thanh_pho"] == "Hue"
    assert config.GIO_YEN_LANG == "23-6"


def test_giong_env_thi_khong_luu(c):
    d = c.put("/api/cai-dat", json={"thanh_pho": "", "gio_yen_lang": "22-7", "tong_ket_tuan": True}).json()
    assert d["da_chinh"] == ["gio_yen_lang"]  # chỉ mục khác .env mới được lưu
    d = c.put("/api/cai-dat", json={"gio_yen_lang": "23-6"}).json()
    assert d["da_chinh"] == [] and config.GIO_YEN_LANG == "23-6"


def test_get_chi_doc(c):
    config.CAI_DAT_PATH.write_text('{"thanh_pho": "Hue"}', encoding="utf-8")
    assert c.get("/api/cai-dat").json()["hien_tai"]["thanh_pho"] == "Hue"
    assert config.THANH_PHO != "Hue"  # chỉ áp dụng khi lưu hoặc khởi động


def test_tat_chuc_le(c):
    d = c.put("/api/cai-dat", json={"chuc_le": False}).json()
    assert d["da_chinh"] == ["chuc_le"] and config.CHUC_LE is False


def test_gio_nhac_thoi_quen(c):
    assert cai_dat.kiem_tra("nhac_thoi_quen", " 21h ") == "21:00"
    assert cai_dat.kiem_tra("nhac_thoi_quen", "") == ""
    assert c.put("/api/cai-dat", json={"nhac_thoi_quen": "25:00"}).status_code == 400
    d = c.put("/api/cai-dat", json={"nhac_thoi_quen": "21h15"}).json()
    assert d["hien_tai"]["nhac_thoi_quen"] == "21:15" and config.NHAC_THOI_QUEN == "21:15"
    c.put("/api/cai-dat", json={"nhac_thoi_quen": ""})
    assert config.NHAC_THOI_QUEN == ""
