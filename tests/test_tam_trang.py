"""Tâm trạng người dùng: Bơ đoán mỗi tin, xem 7 ngày, mấy ngày buồn thì Bơ nhẹ nhàng hơn."""
import json
from datetime import date

from fastapi.testclient import TestClient

from app import main
from app.brain import Brain, build_system_prompt, parse_reply
from app.memory import Memory
from tests.test_brain import FakeClient


def _msg(mem, day, mood, role="user"):
    mid = mem.add_message(role, "x")
    mem.conn.execute("UPDATE messages SET created_at = ?, tam_trang = ? WHERE id = ?", (f"{day} 10:00:00", mood, mid))
    mem.conn.commit()


def test_parse_tam_trang():
    assert parse_reply('{"noi": "Ừa", "tam_trang": "buon"}').tam_trang == "buon"
    assert parse_reply('{"noi": "Ừa", "tam_trang": "kho_hieu"}').tam_trang == ""
    assert parse_reply('{"noi": "Ừa", "tam_trang": ["buon"]}').tam_trang == ""
    assert parse_reply('{"noi": "Ừa"}').tam_trang == ""


def test_chat_ghi_tam_trang_vao_tin_nguoi_dung(tmp_path):
    mem = Memory(tmp_path / "a.db")
    brain = Brain(mem, client=FakeClient([json.dumps({"noi": "Thương ghê", "tam_trang": "met"})]))
    r = brain.chat("Hôm nay mệt quá")
    row = mem.conn.execute("SELECT tam_trang FROM messages WHERE id = ?", (r.user_msg_id,)).fetchone()
    assert row[0] == "met"
    bo = mem.conn.execute("SELECT tam_trang FROM messages WHERE id = ?", (r.msg_id,)).fetchone()
    assert bo[0] is None  # tin của Bơ không có tâm trạng


def test_moods_by_day_chon_tam_trang_noi_bat(tmp_path):
    mem = Memory(tmp_path / "a.db")
    _msg(mem, "2026-10-04", "binh_thuong")
    _msg(mem, "2026-10-05", "binh_thuong")
    _msg(mem, "2026-10-05", "buon")
    _msg(mem, "2026-10-05", "binh_thuong")
    _msg(mem, "2026-10-07", "vui")
    _msg(mem, "2026-10-07", "met")  # bằng nhau → lấy cái gần nhất
    _msg(mem, "2026-10-01", "buon")  # quá 7 ngày, không tính
    out = mem.moods_by_day(7, date(2026, 10, 10))
    assert [d["ngay"] for d in out] == [f"2026-10-{i:02d}" for i in range(4, 11)]
    assert [d["tam_trang"] for d in out] == ["binh_thuong", "buon", None, "met", None, None, None]


def test_low_mood_can_it_nhat_hai_ngay(tmp_path):
    mem = Memory(tmp_path / "a.db")
    today = date(2026, 10, 10)
    _msg(mem, "2026-10-09", "buon")
    assert mem.low_mood(today) == []
    _msg(mem, "2026-10-10", "met")
    _msg(mem, "2026-10-10", "met")
    assert mem.low_mood(today) == ["buon", "met"]
    _msg(mem, "2026-10-10", "vui")  # vẫn là "met" (2 lần) → vẫn buồn mệt
    assert mem.low_mood(today) == ["buon", "met"]


def test_prompt_nhac_quan_tam_khi_buon():
    p = build_system_prompt("Bơ", [], low_mood=["buon", "met"])
    assert "Tâm trạng gần đây" in p and "buồn, mệt" in p
    assert "Tâm trạng gần đây" not in build_system_prompt("Bơ", [])


def test_brain_gui_tam_trang_gan_day(tmp_path):
    mem = Memory(tmp_path / "a.db")
    today = date.today().isoformat()
    _msg(mem, today, "buon")
    from datetime import timedelta
    _msg(mem, (date.today() - timedelta(days=1)).isoformat(), "lo")
    client = FakeClient([json.dumps({"noi": "Bơ đây"})])
    Brain(mem, client=client).chat("chào")
    assert "Tâm trạng gần đây" in client.calls[0]["system"]


def test_sao_luu_giu_tam_trang(tmp_path):
    mem = Memory(tmp_path / "a.db")
    _msg(mem, "2026-10-09", "vui")
    data = mem.export_all()
    mem2 = Memory(tmp_path / "b.db")
    mem2.import_all(json.loads(json.dumps(data)))
    assert mem2.moods_by_day(1, date(2026, 10, 9))[0]["tam_trang"] == "vui"


def test_api_tam_trang(tmp_path):
    main._brain = Brain(Memory(tmp_path / "api.db"), client=FakeClient([json.dumps({"noi": "Ok", "tam_trang": "vui"})]))
    c = TestClient(main.app, headers={"X-Bo": "1"})
    c.post("/api/chat", json={"text": "vui quá"})
    days = c.get("/api/tam-trang").json()
    assert len(days) == 7 and days[-1] == {"ngay": date.today().isoformat(), "tam_trang": "vui"}
    assert len(c.get("/api/tam-trang?days=999").json()) == 31
