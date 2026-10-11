"""Lỗi lộ ra khi thử lời Bơ tự mở đầu bằng API thật (2026-10-11):
- Bơ tự mở lời mà model vẫn "ghi" từ chuyện cũ (tạo ngày đặc biệt, ghi lại điều nhớ, chuyện hỏi thăm).
- Vừa hỏi thăm xong lại chép đúng chuyện đó vào "hoi_tham" → lần sau hỏi lại.
- Tin cũ "mai mình đi phỏng vấn" (gửi mấy ngày trước) bị hiểu là ngày mai tính từ hôm nay."""
import json
from datetime import datetime, timedelta

import pytest

from app.brain import Brain, build_system_prompt
from app.memory import Memory
from tests.test_brain import FakeClient


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "mo_loi.db")


def _tin_cu(memory, role, text, cach: timedelta):
    i = memory.add_message(role, text)
    luc = (datetime.now() - cach).strftime("%Y-%m-%d %H:%M:%S")
    memory.conn.execute("UPDATE messages SET created_at = ? WHERE id = ?", (luc, i))
    memory.conn.commit()
    return luc


def _co_chuyen_de_hoi(memory):
    """Hôm qua Tân kể sắp đi phỏng vấn → hôm nay mở web là Bơ hỏi thăm."""
    _tin_cu(memory, "user", "Mai mình đi phỏng vấn", timedelta(days=1, hours=2))
    _tin_cu(memory, "assistant", "Cố lên nha!", timedelta(days=1, hours=2))
    memory.add_followups(["Đi phỏng vấn công ty mới"])
    memory.conn.execute("UPDATE followups SET created_at = datetime('now', 'localtime', '-1 day')")
    memory.conn.commit()


def test_bo_tu_mo_loi_thi_khong_ghi_gi_moi(memory):
    _co_chuyen_de_hoi(memory)
    memory.add_reminders([{"luc": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 08:00"), "viec": "Gọi mẹ"}])
    memory.add_todos(["Mua sữa"])
    memory.add_facts(["Tên là Tân"])
    client = FakeClient([json.dumps({
        "noi": "Phỏng vấn sao rồi?", "da_hoi": ["Đi phỏng vấn công ty mới (kể hôm qua)"],
        "ghi_nho": ["Mai đi phỏng vấn"], "quen": ["Tên là Tân"], "hoi_tham": ["Kết quả phỏng vấn"],
        "nhac": [{"luc": "2099-01-01 08:00", "viec": "Bịa ra", "lap": ""}], "huy_nhac": ["Gọi mẹ"],
        "viec_can_lam": ["Việc bịa"], "xong_viec": ["Mua sữa"],
        "ngay_dac_biet": [{"ngay": "04/07", "viec": "Ngày quen nhau", "am_lich": False}],
        "thoi_quen_moi": ["Thói quen bịa"], "nhat_ky": "Chuyện cũ ghi nhầm vào hôm nay",
    })])
    r = Brain(memory, client=client).greet()
    assert r.noi == "Phỏng vấn sao rồi?" and r.da_ghi == []
    assert memory.all_facts() == ["Tên là Tân"]
    assert [x["viec"] for x in memory.upcoming_reminders()] == ["Gọi mẹ"]
    assert [(t["viec"], t["xong"]) for t in memory.todos()] == [("Mua sữa", False)]
    assert memory.special_days() == [] and memory.habits() == [] and memory.diary_recent() == []
    assert memory.pending_followups(min_hours=0) == []  # chuyện vừa hỏi thăm thì vẫn được gạch


def test_vua_hoi_tham_xong_khong_ghi_lai_chuyen_do(memory):
    _co_chuyen_de_hoi(memory)
    client = FakeClient([json.dumps({
        "noi": "Phỏng vấn sao rồi?", "da_hoi": ["Đi phỏng vấn công ty mới (kể hôm qua)"],
        "hoi_tham": ["đi phỏng vấn công ty mới", "Thứ Sáu 16/10 nhận kết quả"],
    })])
    Brain(memory, client=client).chat("Chào Bơ")
    assert [f["content"] for f in memory.pending_followups(min_hours=0)] == ["Thứ Sáu 16/10 nhận kết quả"]


def test_don_dieu_nho_gui_kem_ngay_va_khong_cho_xoa_qua_tay(memory, monkeypatch):
    from datetime import date

    from app import config
    from app.brain import MERGE_PROMPT

    monkeypatch.setattr(config, "FACTS_MERGE_AT", 10)
    dieu = [f"Điều {i}" for i in range(10)]
    memory.add_facts(dieu)
    # AI trả về có 1 điều từ 10 điều: coi như dọn hỏng, giữ nguyên
    client = FakeClient(['["Chỉ còn một"]'])
    brain = Brain(memory, client=client)
    brain.maybe_merge_facts()
    assert memory.all_facts() == dieu
    assert client.calls[0]["messages"][0]["content"].startswith(f"Hôm nay là {date.today():%d/%m/%Y}.\n- Điều 0")
    assert "việc vặt" in MERGE_PROMPT and "ngày đã qua" in MERGE_PROMPT and client.calls[0]["system"] == MERGE_PROMPT
    # dọn vừa phải (10 → 4) thì nhận
    brain = Brain(memory, client=FakeClient([json.dumps(dieu[:4], ensure_ascii=False)]))
    brain.maybe_merge_facts()
    assert memory.all_facts() == dieu[:4]


def test_tin_cu_duoc_ghi_chu_ngay_gui(memory):
    luc = _tin_cu(memory, "user", "Mai mình đi phỏng vấn", timedelta(days=3))
    _tin_cu(memory, "assistant", "Cố lên nha!", timedelta(days=3))
    hom_qua = _tin_cu(memory, "user", "Hơi lo", timedelta(days=1))
    _tin_cu(memory, "assistant", "Ổn mà!", timedelta(days=1))
    client = FakeClient([json.dumps({"noi": "Sao rồi?"})])
    Brain(memory, client=client).chat("Mình về rồi nè")
    tin = [m["content"] for m in client.calls[0]["messages"]]
    assert tin == [
        f"(tin gửi 3 ngày trước, {luc[8:10]}/{luc[5:7]}) Mai mình đi phỏng vấn", "Cố lên nha!",
        f"(tin gửi hôm qua, {hom_qua[8:10]}/{hom_qua[5:7]}) Hơi lo", "Ổn mà!",
        "Mình về rồi nè",  # tin hôm nay giữ nguyên
    ]
    assert [m["content"] for m in memory.recent_messages(10)][0] == "Mai mình đi phỏng vấn"  # trí nhớ không bị sửa
    assert "tin gửi hôm qua" in build_system_prompt("Bạn là Bơ.", []).split("## Tình hình lúc này")[0]  # có lời dặn giải thích
