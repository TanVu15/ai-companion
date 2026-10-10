"""Âm lịch: so với ngày Tết, Trung thu, tháng nhuận đã biết."""
from datetime import date, timedelta

import pytest

from app.am_lich import am_sang_duong, duong_sang_am, mo_ta_am, ngay_le, ten_nam

TET = {2000: date(2000, 2, 5), 2010: date(2010, 2, 14), 2020: date(2020, 1, 25), 2023: date(2023, 1, 22),
       2024: date(2024, 2, 10), 2025: date(2025, 1, 29), 2026: date(2026, 2, 17), 2027: date(2027, 2, 6)}


@pytest.mark.parametrize("nam,ngay", TET.items())
def test_ngay_tet(nam, ngay):
    assert duong_sang_am(ngay) == (1, 1, nam, False)
    assert am_sang_duong(1, 1, nam) == ngay


def test_trung_thu_va_thang_nhuan():
    assert duong_sang_am(date(2025, 10, 6)) == (15, 8, 2025, False)
    assert duong_sang_am(date(2026, 9, 25)) == (15, 8, 2026, False)
    assert duong_sang_am(date(2023, 3, 22)) == (1, 2, 2023, True)  # tháng 2 nhuận 2023
    assert duong_sang_am(date(2025, 7, 25)) == (1, 6, 2025, True)  # tháng 6 nhuận 2025
    assert am_sang_duong(1, 6, 2025, True) == date(2025, 7, 25)
    assert am_sang_duong(1, 5, 2025, True) is None  # 2025 không nhuận tháng 5
    assert am_sang_duong(1, 1, 2026, True) is None
    assert am_sang_duong(0, 1, 2026) is None and am_sang_duong(1, 13, 2026) is None


def test_hai_chieu_khop_nhau_nhieu_nam():
    d = date(2019, 1, 1)
    while d < date(2032, 1, 1):
        ngay, thang, nam, nhuan = duong_sang_am(d)
        assert am_sang_duong(ngay, thang, nam, nhuan) == d
        d += timedelta(days=7)


def test_ten_nam_va_mo_ta():
    assert ten_nam(2026) == "Bính Ngọ" and ten_nam(2025) == "Ất Tỵ" and ten_nam(2024) == "Giáp Thìn"
    assert mo_ta_am(date(2026, 2, 17)) == "mùng 1 tháng 1 năm Bính Ngọ"
    assert mo_ta_am(date(2023, 3, 22)) == "mùng 1 tháng 2 nhuận năm Quý Mão"


def test_ngay_le():
    assert ngay_le(date(2026, 10, 20)) == ["Ngày Phụ nữ Việt Nam 20/10"]
    assert ngay_le(date(2026, 9, 25)) == ["Tết Trung thu"]
    assert ngay_le(date(2026, 2, 16)) == ["Giao thừa (đêm cuối năm âm lịch)"]
    assert ngay_le(date(2026, 2, 17)) == ["mùng 1 Tết Nguyên đán"]
    assert ngay_le(date(2026, 10, 11)) == []
    # tháng 6 nhuận 2025: ngày 15/6 nhuận không phải lễ gì; Vu Lan 2025 là 6/9
    assert ngay_le(date(2025, 9, 6)) == ["Lễ Vu Lan (Rằm tháng Bảy)"]


def test_prompt_co_am_lich_va_le():
    from datetime import datetime

    from app.brain import build_system_prompt

    p = build_system_prompt("Bơ", [], now=datetime(2026, 10, 19, 9, 0))
    assert "Âm lịch: mùng 10 tháng 9 năm Bính Ngọ." in p
    assert "Ngày mai là: Ngày Phụ nữ Việt Nam 20/10." in p and "Hôm nay là: " not in p
    p = build_system_prompt("Bơ", [], now=datetime(2026, 10, 12, 9, 0))
    assert "Ngày mai là" not in p and "đừng lặp lại" not in p


def test_ngay_hiem_khong_ra_ngay_0():
    for d in (date(2054, 5, 7), date(2062, 4, 9)):
        ngay, thang, nam, nhuan = duong_sang_am(d)
        assert ngay >= 1 and am_sang_duong(ngay, thang, nam, nhuan) == d


def test_api_hom_nay(tmp_path, monkeypatch):
    from app import config, main
    from tests.test_api import make_client

    c = make_client(tmp_path, [])
    d = c.get("/api/hom-nay").json()
    ngay, thang, nam, nhuan = duong_sang_am(date.today())
    assert d["duong"] == date.today().strftime("%d/%m/%Y") and d["am"].startswith(f"{ngay}/{thang}")
    assert d["nam_am"] == ten_nam(nam) and isinstance(d["le"], list)
    monkeypatch.setattr(config, "DEVICE_KEY", "k")
    r = c.get("/api/thiet-bi/hom-nay?khong_dau=1", headers={"X-Device-Key": "k"}).json()
    assert r["nam_am"] == main.bo_dau(ten_nam(nam)) and r["thu"].isascii()
    assert c.get("/api/thiet-bi/hom-nay", headers={"X-Device-Key": "sai"}).status_code == 401


def test_le_sap_toi_va_tet():
    from app.am_lich import le_sap_toi, tet_sap_toi

    xs = le_sap_toi(date(2026, 10, 10), 45)
    assert [(x["ten"], x["con_ngay"]) for x in xs] == [
        ("Ngày Phụ nữ Việt Nam 20/10", 10), ("Ngày Nhà giáo Việt Nam 20/11", 41)]
    tet = [x["ten"] for x in le_sap_toi(date(2027, 1, 20), 45)]
    assert "mùng 1 Tết Nguyên đán" in tet and "mùng 2 Tết" not in tet
    assert tet_sap_toi(date(2026, 10, 10)) == {"con_ngay": 119, "ngay": date(2027, 2, 6)}
    assert tet_sap_toi(date(2026, 2, 17))["con_ngay"] == 0  # đúng mùng 1
    assert tet_sap_toi(date(2026, 2, 18))["ngay"] == date(2027, 2, 6)


def test_prompt_le_sap_toi():
    from datetime import datetime

    from app.brain import build_system_prompt

    p = build_system_prompt("Bơ", [], now=datetime(2026, 10, 10, 9, 0))
    assert ("Ngày lễ sắp tới: Ngày Phụ nữ Việt Nam 20/10 (còn 10 ngày); Ngày Nhà giáo Việt Nam 20/11 (còn 41 ngày); "
            "Tết Nguyên đán 06/02/2027 (còn 119 ngày).") in p
    p = build_system_prompt("Bơ", [], now=datetime(2026, 10, 19, 9, 0))
    assert "Phụ nữ Việt Nam 20/10 (còn" not in p  # ngày mai đã có dòng "Ngày mai là"
    p = build_system_prompt("Bơ", [], now=datetime(2027, 1, 20, 9, 0))
    assert p.count("Tết Nguyên đán") == 1 and "mùng 1 Tết Nguyên đán 06/02 (còn 17 ngày)" in p


def test_api_hom_nay_sap_toi(tmp_path, monkeypatch):
    from datetime import timedelta

    from app import config, main
    from tests.test_api import make_client

    c = make_client(tmp_path, [])
    main._brain.memory.add_special_days([{"ngay": (date.today() + timedelta(days=3)).strftime("%d/%m"),
                                          "viec": "Sinh nhật mẹ"}])
    d = c.get("/api/hom-nay").json()
    assert len(d["sap_toi"]) <= 3 and {"ten": "Sinh nhật mẹ", "con_ngay": 3,
            "ngay": (date.today() + timedelta(days=3)).strftime("%d/%m/%Y")} in d["sap_toi"]
    assert [x["con_ngay"] for x in d["sap_toi"]] == sorted(x["con_ngay"] for x in d["sap_toi"])
    monkeypatch.setattr(config, "DEVICE_KEY", "k")
    r = c.get("/api/thiet-bi/hom-nay?khong_dau=1", headers={"X-Device-Key": "k"}).json()
    assert any(x["ten"] == "Sinh nhat me" and x["con_ngay"] == 3 for x in r["sap_toi"])
