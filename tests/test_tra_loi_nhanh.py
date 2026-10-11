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
])
def test_nhan_dien(text, loai):
    assert nhan_dien(text) == loai


@pytest.mark.parametrize("text", [
    "mấy giờ rồi mà mình vẫn chưa ngủ được", "Tết này mình về quê", "hôm nay mình buồn quá",
    "nhớ giúp mình việc cần làm là mua sữa", "hôm nay ngày gì mà vui vậy ta, mình được tăng lương nè Bơ ơi", "", "???",
    "mấy giờ thì mình nên đi ngủ", "còn mấy ngày nữa sinh nhật mình",
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
    # Tắt thì gửi cho AI
    monkeypatch.setattr(config, "MONTHLY_USD_LIMIT", 0)
    monkeypatch.setattr(config, "TRA_LOI_NHANH", False)
    client.replies.append(json.dumps({"noi": "Tầm 7h đó", "cam_xuc": "vui"}))
    assert brain.chat("mấy giờ rồi").noi == "Tầm 7h đó"
