"""Dòng "Bơ đã ghi: ..." dưới câu trả lời: lấy từ những gì ĐÃ LƯU THẬT, không phải từ lời Bơ nói."""
import json
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app import main
from app.brain import Brain, kieu_lap, mo_ta_thay_doi
from app.memory import Memory
from tests.test_brain import FakeClient


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "ghi.db")


def _mai(gio: str) -> str:
    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d ") + gio


def test_ghi_gi_thi_bao_nay(memory):
    luc = _mai("20:00")
    client = FakeClient([json.dumps({
        "noi": "Ok hết nha!", "nhac": [{"luc": luc, "viec": "Gọi mẹ", "lap": "ngay"}],
        "viec_can_lam": ["Mua sữa"], "thoi_quen_moi": ["Đọc sách"], "ghi_nho": ["Làm lập trình viên"],
        "ngay_dac_biet": [{"ngay": "15/10", "viec": "Sinh nhật mẹ", "am_lich": False}],
        "nhat_ky": "Đi đá bóng thắng 3-1",
    })])
    r = Brain(memory, client=client).chat("nhờ đủ thứ")
    assert r.da_ghi == [
        f"nhắc 20:00 {luc[8:10]}/{luc[5:7]}: Gọi mẹ (mỗi ngày)", "việc cần làm: Mua sữa", "theo dõi thói quen: Đọc sách",
        "ngày đặc biệt 15/10: Sinh nhật mẹ", "nhớ: Làm lập trình viên", "nhật ký: Đi đá bóng thắng 3-1",
    ]
    assert memory.history_page()[-1]["da_ghi"] == r.da_ghi  # mở lại web vẫn thấy
    assert memory.history_page()[0]["da_ghi"] == []  # tin của người dùng thì không có


def test_hua_ma_khong_ghi_thi_khong_bao(memory):
    """Model nói "để Bơ nhắc nha" nhưng không ghi vào "nhac" (hoặc ghi giờ đã qua) → không có dòng nào."""
    client = FakeClient([
        json.dumps({"noi": "Ok, 8h tối Bơ nhắc nha!"}),
        json.dumps({"noi": "Bơ nhắc rồi đó", "nhac": [{"luc": "2020-01-01 08:00", "viec": "Việc cũ", "lap": ""}]}),
    ])
    brain = Brain(memory, client=client)
    assert brain.chat("8h tối nhắc mình gọi mẹ").da_ghi == []
    assert brain.chat("nhắc chưa?").da_ghi == []
    assert all(m["da_ghi"] == [] for m in memory.history_page())


def test_trung_thi_khong_bao_lai(memory):
    luc = _mai("20:00")
    tra_loi = json.dumps({"noi": "Ok", "nhac": [{"luc": luc, "viec": "Gọi mẹ", "lap": ""}], "viec_can_lam": ["Mua sữa"],
                          "ghi_nho": ["Thích phở"]})
    brain = Brain(memory, client=FakeClient([tra_loi, tra_loi]))
    assert len(brain.chat("một").da_ghi) == 3
    assert brain.chat("hai").da_ghi == []  # model chép lại y hệt: không có gì mới được lưu


def test_xong_viec_tich_thoi_quen_bo_nhac_quen(memory):
    luc = _mai("07:00")
    memory.add_todos(["Mua sữa"])
    memory.add_habits(["Đọc sách", "Chạy bộ"])
    memory.add_reminders([{"luc": luc, "viec": "Uống nước", "lap": "gio_2"}])
    memory.add_facts(["Sống ở Đà Nẵng"])
    client = FakeClient([json.dumps({
        "noi": "Giỏi quá!", "xong_viec": ["Mua sữa"], "thoi_quen_xong": ["Đọc sách"], "thoi_quen_hom_qua": ["Chạy bộ"],
        "huy_nhac": ["Uống nước"], "quen": ["Sống ở Đà Nẵng"], "ghi_nho": ["Sống ở Sài Gòn"],
    })])
    r = Brain(memory, client=client).chat("kể nhiều chuyện")
    assert r.da_ghi == ["bỏ nhắc: Uống nước", "xong việc: Mua sữa", "tích hôm nay: Đọc sách", "tích bù hôm qua: Chạy bộ",
                        "nhớ: Sống ở Sài Gòn", "quên: Sống ở Đà Nẵng"]


def test_kieu_lap_va_gioi_han_so_dong():
    assert [kieu_lap(x) for x in ("", None, "ngay", "ngay_thuong", "tuan", "thang", "gio_3")] == [
        "", "", "mỗi ngày", "thứ 2–6", "mỗi tuần", "mỗi tháng", "mỗi 3 tiếng"]
    rong = {"nhac": {}, "viec": {}, "thoi_quen": {}, "ngay": {}, "nho": [], "nhat_ky": {}}
    assert mo_ta_thay_doi(rong, rong) == []
    nhieu = {**rong, "nho": [f"Điều {i}" for i in range(12)] + ["x" * 200]}
    out = mo_ta_thay_doi(rong, nhieu)
    assert len(out) == 9 and out[-1] == "và 5 mục khác" and out[0] == "nhớ: Điều 0"
    assert len(mo_ta_thay_doi(rong, {**rong, "nho": ["x" * 200]})[0]) == 90  # dòng dài thì cắt bớt


def test_chup_tri_nho_loi_thi_van_tra_loi(memory, monkeypatch):
    brain = Brain(memory, client=FakeClient([json.dumps({"noi": "Vẫn ổn", "viec_can_lam": ["Mua sữa"]})]))
    monkeypatch.setattr(memory, "special_days", lambda: 1 / 0)
    r = brain.chat("hi")
    assert r.noi == "Vẫn ổn" and r.da_ghi == []
    assert [t["viec"] for t in memory.todos()] == ["Mua sữa"]  # việc vẫn được ghi


def test_api_tra_da_ghi_va_lich_su_giu_lai(memory):
    client = FakeClient([json.dumps({"noi": "Ghi rồi nha", "viec_can_lam": ["Trả sách"]}), json.dumps({"noi": "Ừa"})])
    main._brain = Brain(memory, client=client)
    web = TestClient(main.app)
    h = {"X-Bo": "1"}
    assert web.post("/api/chat", json={"text": "nhớ giúp mình trả sách"}, headers=h).json()["da_ghi"] == ["việc cần làm: Trả sách"]
    assert web.post("/api/chat", json={"text": "cảm ơn"}, headers=h).json()["da_ghi"] == []
    lich_su = web.get("/api/history").json()
    assert [m["da_ghi"] for m in lich_su] == [[], ["việc cần làm: Trả sách"], [], []]


def test_sao_luu_giu_dong_da_ghi(memory, tmp_path):
    Brain(memory, client=FakeClient([json.dumps({"noi": "Ok", "viec_can_lam": ["Mua sữa"]})])).chat("hi")
    data = json.loads(json.dumps(memory.export_all()))
    moi = Memory(tmp_path / "moi.db")
    moi.import_all(data)
    assert moi.history_page()[-1]["da_ghi"] == ["việc cần làm: Mua sữa"]
    for row in data["messages"]:  # bản sao lưu cũ (trước khi có cột này) vẫn nạp được
        row.pop("da_ghi")
    moi.import_all(data)
    assert moi.history_page()[-1]["da_ghi"] == []


def test_thiet_bi_khong_nhan_da_ghi(memory, monkeypatch):
    from app import config

    monkeypatch.setattr(config, "DEVICE_KEY", "khoa")
    main._brain = Brain(memory, client=FakeClient([json.dumps({"noi": "Ok", "viec_can_lam": ["Mua sữa"]})]))
    r = TestClient(main.app).post("/api/thiet-bi/chat", json={"text": "hi"}, headers={"X-Device-Key": "khoa"})
    assert set(r.json()) == {"noi", "cam_xuc", "hanh_dong"}  # thiết bị nhỏ chỉ cần gọn
