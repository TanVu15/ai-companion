"""Test bộ chấm điểm tính cách bằng bộ não giả."""
import json

from app import thu_tinh_cach as t
from tests.test_brain import FakeClient


def test_file_tinh_huong_hop_le():
    ds = json.loads(t.TINH_HUONG_PATH.read_text(encoding="utf-8"))
    assert len(ds) == 22
    for th in ds:
        assert th["ten"] and th["tin_nhan"]


def test_dem_cau():
    assert t.dem_cau("Chào! Khỏe hông? Đi tập nha.") == 3
    assert t.dem_cau("Một câu thôi") == 1


def test_cau_tra_loi_tot_duoc_diem_toi_da():
    th = {"ten": "Buồn", "tin_nhan": "buồn quá", "cam_xuc_hop_le": ["buon", "thuong"],
          "phai_co_mot_trong": ["kể"], "khong_duoc_co": ["kkk"]}
    client = FakeClient([json.dumps({"noi": "Thương ghê. Kể Bơ nghe nha?", "cam_xuc": "thuong"})])
    [kq] = t.chay(client, [th])
    assert kq.diem == 1.0


def test_cau_tra_loi_te_bi_tru_diem():
    th = {"ten": "Buồn", "tin_nhan": "buồn quá", "cam_xuc_hop_le": ["buon"],
          "khong_duoc_co": ["kkk"], "phai_ghi_nho": True}
    client = FakeClient(["kkk vui lên đi. Câu hai. Câu ba. Câu bốn."])  # không phải JSON, dài, nhây
    [kq] = t.chay(client, [th])
    assert [ok for _, ok in kq.kiem_tra] == [False, False, False, False, False]
    assert kq.diem == 0.0


def test_da_biet_duoc_dua_vao_bo_nao():
    th = {"ten": "Nhớ tên", "da_biet": ["Tên là Tân"], "tin_nhan": "mình tên gì?", "phai_co_mot_trong": ["Tân"]}
    client = FakeClient([json.dumps({"noi": "Tân chứ ai!", "cam_xuc": "vui"})])
    [kq] = t.chay(client, [th])
    assert "Tên là Tân" in client.calls[0]["system"]
    assert kq.diem == 1.0
    assert "TỔNG ĐIỂM: 100%" in t.in_bao_cao([kq])


def test_hoi_tham_duoc_dua_vao_va_cham():
    th = {"ten": "Hỏi thăm", "can_hoi_tham": ["Chiều nay đi tập chân"], "tin_nhan": "Chào Bơ",
          "phai_co_mot_trong": ["chân"], "phai_da_hoi": True}
    client = FakeClient([json.dumps({"noi": "Hôm qua tập chân sao rồi?", "cam_xuc": "vui",
                                     "da_hoi": ["Chiều nay đi tập chân"]})])
    [kq] = t.chay(client, [th])
    assert "Chiều nay đi tập chân (kể hôm qua)" in client.calls[0]["system"]
    assert kq.diem == 1.0


def test_phai_ghi_hoi_tham():
    th = {"ten": "Sắp phỏng vấn", "tin_nhan": "chiều nay phỏng vấn", "phai_ghi_hoi_tham": True}
    [kq] = t.chay(FakeClient([json.dumps({"noi": "Cố lên!"})]), [th])
    assert ("Ghi lại để hỏi thăm sau", False) in kq.kiem_tra


def test_ngay_dac_biet_va_nhac_lap():
    tot = json.dumps({"noi": "Chúc mừng sinh nhật Tân!", "cam_xuc": "vui",
                      "ngay_dac_biet": [{"ngay": "5/3", "viec": "Sinh nhật"}],
                      "nhac": [{"luc": "2030-01-01 07:00", "viec": "Uống nước", "lap": "ngay"}]})
    th = {"ten": "x", "tin_nhan": "hi", "hom_nay_dac_biet": ["Sinh nhật Tân"], "phai_co_mot_trong": ["sinh nhật"],
          "phai_ghi_ngay_dac_biet": True, "phai_nhac_lap": "ngay"}
    client = FakeClient([tot, json.dumps({"noi": "Ok"})])
    [kq] = t.chay(client, [th])
    assert kq.diem == 1.0 and "Sinh nhật Tân" in client.calls[0]["system"]
    [kq] = t.chay(client, [{**th, "hom_nay_dac_biet": []}])
    assert ("Ghi ngày đặc biệt", False) in kq.kiem_tra and ("Nhắc lặp lại (ngay)", False) in kq.kiem_tra


def test_viec_can_lam_va_tam_trang():
    tot = json.dumps({"noi": "Mua sữa rồi hả, giỏi!", "cam_xuc": "vui", "viec_can_lam": ["Trả sách"],
                      "xong_viec": ["Mua sữa"], "tam_trang": "met"})
    th = {"ten": "x", "tin_nhan": "hi", "viec_dang_co": ["Mua sữa"], "buon_may_ngay": True,
          "phai_ghi_viec": True, "phai_xong_viec": True, "phai_tam_trang": ["met"]}
    client = FakeClient([tot, json.dumps({"noi": "Ok"})])
    [kq] = t.chay(client, [th])
    system = client.calls[0]["system"]
    assert kq.diem == 1.0 and "- Mua sữa" in system and "Tâm trạng gần đây" in system
    [kq] = t.chay(client, [{**th, "viec_dang_co": [], "buon_may_ngay": False}])
    assert ("Gạch việc đã xong", False) in kq.kiem_tra and ("Đoán đúng tâm trạng (met)", False) in kq.kiem_tra


def test_am_lich():
    from datetime import date

    from app.am_lich import duong_sang_am

    ngay, thang, _, _ = duong_sang_am(date.today())
    tot = json.dumps({"noi": f"Hôm nay mùng {ngay} tháng {thang} âm nè!",
                      "ngay_dac_biet": [{"ngay": "15/7", "viec": "Giỗ ông", "am_lich": True}]})
    th = {"ten": "x", "tin_nhan": "hi", "phai_noi_ngay_am": True, "phai_ghi_ngay_am": True}
    [kq] = t.chay(FakeClient([tot]), [th])
    assert kq.diem == 1.0
    [kq] = t.chay(FakeClient([json.dumps({"noi": "Không biết", "ngay_dac_biet": [{"ngay": "15/7", "viec": "Giỗ"}]})]), [th])
    assert ("Nói đúng ngày âm hôm nay", False) in kq.kiem_tra and ("Ghi đúng là ngày âm lịch", False) in kq.kiem_tra
