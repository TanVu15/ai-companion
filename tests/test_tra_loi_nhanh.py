"""Test trả lời nhanh không tốn API (mấy giờ, ngày âm, Tết, việc cần làm)."""
import json
from datetime import datetime

import pytest

from app import config
from app.brain import Brain
from app.memory import Memory
from app.tra_loi_nhanh import nhan_dien, tra_loi
from tests.test_brain import FakeClient


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "t.db")


@pytest.mark.parametrize("text,loai", [
    ("mấy giờ rồi?", "gio"), ("Bơ ơi mấy giờ rồi", "gio"), ("may gio roi vay", "gio"), ("Bây giờ là mấy giờ?", "gio"),
    ("hôm nay thứ mấy?", "thu"), ("hôm nay ngày mấy", "ngay"), ("Hôm nay là ngày bao nhiêu vậy Bơ", "ngay"),
    ("hôm nay ngày mấy âm?", "am"), ("âm lịch hôm nay", "am"), ("hom nay bao nhieu am lich", "am"),
    ("còn mấy ngày nữa Tết?", "tet"), ("con bao nhieu ngay nua toi tet", "tet"), ("Tết còn mấy ngày nữa nhỉ", "tet"),
    ("bao giờ thì Tết", "tet"), ("mình còn việc gì cần làm không?", "viec"), ("việc cần làm của mình", "viec"),
    ("mấy h rồi", "gio"), ("mấy giờ r", "gio"), ("mấy giờ rồi ta", "gio"), ("thứ mấy rồi", "thu"),
    ("hôm nay thứ mấy ngày mấy", "ngay"), ("hôm nay mùng mấy âm", "am"), ("còn bao lâu nữa tết", "tet"),
    ("có việc gì cần làm không", "viec"), ("việc cần làm hôm nay", "viec"),
    ("thói quen hôm nay", "thoi_quen"), ("Bơ ơi thói quen của mình sao rồi?", "thoi_quen"),
    ("hôm nay mình còn thói quen nào chưa làm", "thoi_quen"),
    ("hôm nay trời thế nào?", "thoi_tiet"), ("mai có mưa không Bơ", "thoi_tiet"), ("thời tiết hôm nay", "thoi_tiet"),
    ("trời hôm nay sao vậy", "thoi_tiet"), ("bây giờ bao nhiêu độ", "thoi_tiet"),
])
def test_nhan_dien(text, loai):
    assert nhan_dien(text) == loai


@pytest.mark.parametrize("text", [
    "mấy giờ rồi mà mình vẫn chưa ngủ được", "Tết này mình về quê", "hôm nay mình buồn quá",
    "nhớ giúp mình việc cần làm là mua sữa", "hôm nay ngày gì mà vui vậy ta, mình được tăng lương nè Bơ ơi", "", "???",
    "mấy giờ thì mình nên đi ngủ", "còn mấy ngày nữa sinh nhật mình",
    "mấy giờ?", "mấy giờ đi?", "mấy giờ vậy bạn", "mấy giờ nhé", "mấy giờ ạ",  # hỏi giờ hẹn, không phải giờ hiện tại
    "tui việc gì phải làm vậy", "việc gì phải làm thế", "em việc gì phải làm", "mình gì phải làm", "mình nào chưa xong",
    "hôm nay ngày gì vậy", "thói quen xấu của mình là thức khuya", "theo dõi giúp mình thói quen đọc sách",
    "Thói quen là gì?", "bơ ơi thói quen của em là gì vậy",
    "trời ơi mệt quá", "may đồ", "mấy độ", "thời tiết thế này chỉ muốn ngủ", "mai mình đi Đà Lạt, trời có lạnh không",
])
def test_khong_nhan_nham(text):
    assert nhan_dien(text) == ""


def test_cau_tra_loi(memory):
    now = datetime(2026, 10, 11, 7, 5)  # Chủ nhật, mùng 2/9 âm năm Bính Ngọ
    assert tra_loi("gio", now)[0] == "Bây giờ là 7 giờ 05 phút nè (07:05)."
    noi = tra_loi("ngay", now)[0]
    assert "Chủ nhật, 11/10/2026" in noi and "âm lịch mùng 2 tháng 9" in noi
    assert "Bính Ngọ" in tra_loi("am", now)[0]
    assert "Còn 118 ngày nữa là Tết" in tra_loi("tet", now)[0] and "thứ Bảy, 06/02/2027" in tra_loi("tet", now)[0]
    assert "Mai là mùng 1 Tết" in tra_loi("tet", datetime(2027, 2, 5))[0]
    assert "Hôm nay là mùng 1 Tết" in tra_loi("tet", datetime(2027, 2, 6))[0]
    assert "Ngày Phụ nữ Việt Nam" in tra_loi("ngay", datetime(2026, 10, 20))[0]
    assert "Đang mùng 2 Tết" in tra_loi("tet", datetime(2027, 2, 7))[0]
    assert "trống trơn" in tra_loi("viec", now, memory)[0]
    memory.add_todos([f"Việc {i}" for i in range(7)])
    noi = tra_loi("viec", now, memory)[0]
    assert noi.startswith("Bạn còn 7 việc: Việc 0;") and "và 2 việc nữa" in noi and "Việc 5" not in noi


def test_brain_khong_goi_api(memory, monkeypatch):
    client = FakeClient([json.dumps({"noi": "Ừa", "cam_xuc": "vui"})])
    brain = Brain(memory, client=client)
    r = brain.chat("mấy giờ rồi Bơ?")
    assert r.noi.startswith("Bây giờ là") and r.msg_id and r.user_msg_id and client.calls == []
    # Hỏi lại câu khác → AI thấy cả câu hỏi nhanh trong lịch sử
    brain.chat("cảm ơn nha")
    roles = [m["content"] for m in client.calls[0]["messages"]]
    assert "mấy giờ rồi Bơ?" in roles[0]
    # Hết ngân sách vẫn trả lời nhanh được
    monkeypatch.setattr(config, "MONTHLY_USD_LIMIT", 0.000001)
    memory.add_usage("chat", 10_000, 10_000)
    assert "Tết" in brain.chat("còn mấy ngày nữa tết").noi
    assert "ngân sách" in brain.chat("kể chuyện đi").noi
    # Câu miễn phí không tính vào DAILY_LIMIT
    monkeypatch.setattr(config, "DAILY_LIMIT", 1)
    assert brain._ai_replies_today() == 1
    # Tắt thì gửi cho AI
    monkeypatch.setattr(config, "DAILY_LIMIT", 300)
    monkeypatch.setattr(config, "MONTHLY_USD_LIMIT", 0)
    monkeypatch.setattr(config, "TRA_LOI_NHANH", False)
    client.replies.append(json.dumps({"noi": "Tầm 7h đó", "cam_xuc": "vui"}))
    assert brain.chat("mấy giờ rồi").noi == "Tầm 7h đó"


def test_api_va_tinh_trang(tmp_path, monkeypatch):
    from tests.test_api import make_client

    c = make_client(tmp_path, [])
    checks = {k["ten"]: k for k in c.get("/api/suc-khoe").json()["kiem_tra"]}
    assert "miễn phí" in checks["Trả lời nhanh"]["ghi_chu"]
    r = c.post("/api/chat", json={"text": "hôm nay thứ mấy?"}).json()
    assert r["noi"].startswith("Hôm nay là") and r["id"] == 2 and r["id_nguoi_dung"] == 1
    c.post("/api/chat", json={"text": "may gio roi"})
    checks = {k["ten"]: k for k in c.get("/api/suc-khoe").json()["kiem_tra"]}
    assert "tự trả lời 2 câu" in checks["Trả lời nhanh"]["ghi_chu"]
    monkeypatch.setattr(config, "TRA_LOI_NHANH", False)
    checks = {k["ten"]: k for k in c.get("/api/suc-khoe").json()["kiem_tra"]}
    assert checks["Trả lời nhanh"]["muc"] == "canh_bao"


def test_thoi_quen(memory):
    from datetime import date

    now = datetime(2026, 10, 11, 21, 0)
    assert "chưa nhờ Bơ theo dõi" in tra_loi("thoi_quen", now, memory)[0]
    memory.add_habits(["Đọc sách", "Chạy bộ"])
    a, b = memory.habits()
    for k in (1, 2):
        memory.set_habit_done(b["id"], True, date(2026, 10, 11 - k))
    memory.set_habit_done(a["id"], True, date(2026, 10, 11))
    noi = tra_loi("thoi_quen", now, memory)[0]
    assert noi.startswith("Hôm nay xong Đọc sách rồi. Còn chưa làm: Chạy bộ (đang chuỗi 2 ngày).")
    memory.set_habit_done(b["id"], True, date(2026, 10, 11))
    assert "làm đủ hết 2 thói quen" in tra_loi("thoi_quen", now, memory)[0]


def test_thoi_tiet(memory):
    class W:
        thanh_pho = "Da Nang"

        def hien_tai(self):
            return "Thời tiết ở Đà Nẵng: bây giờ 28°C, nắng."

    now = datetime(2026, 10, 11, 9, 0)
    assert "Cài đặt" in tra_loi("thoi_tiet", now)[0]
    assert "chưa lấy được" in tra_loi("thoi_tiet", now, co_thanh_pho=True)[0]
    client = FakeClient([])
    brain = Brain(memory, client=client, weather=W())
    assert brain.chat("hôm nay trời thế nào?").noi.startswith("Thời tiết ở Đà Nẵng: bây giờ 28°C") and client.calls == []
