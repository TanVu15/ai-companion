"""Việc cần làm: Bơ ghi việc Tân nhờ, gạch khi Tân kể đã làm; web xem/thêm/xong/xóa."""
import json

from fastapi.testclient import TestClient

from app import main
from app.brain import Brain, build_system_prompt, parse_reply
from app.memory import Memory
from tests.test_brain import FakeClient


def reply(noi="Ok", **extra):
    return json.dumps({"noi": noi, "cam_xuc": "vui", "hanh_dong": "khong", **extra})


def test_parse_viec():
    r = parse_reply(reply(viec_can_lam=["Mua sữa", {"x": 1}], xong_viec="sai kiểu"))
    assert r.viec_can_lam == ["Mua sữa"] and r.xong_viec == []
    assert "viec_can_lam" not in r.to_dict()


def test_them_khong_trung_va_danh_dau_xong(tmp_path):
    mem = Memory(tmp_path / "a.db")
    assert mem.add_todos(["Mua sữa", "mua  sữa.", "", "Trả sách"]) == 2
    assert [t["viec"] for t in mem.todos()] == ["Mua sữa", "Trả sách"]
    mem.done_todos(["mua sữa"])
    out = mem.todos()
    assert [(t["viec"], t["xong"]) for t in out] == [("Trả sách", False), ("Mua sữa", True)]
    assert [t["viec"] for t in mem.todos(include_done=False)] == ["Trả sách"]
    # việc đã xong thì thêm lại được (lần mua sữa sau)
    assert mem.add_todos(["Mua sữa"]) == 1


def test_viec_xong_lau_thi_tu_don(tmp_path):
    mem = Memory(tmp_path / "a.db")
    mem.add_todos(["Mua sữa"])
    mem.done_todos(["Mua sữa"])
    mem.conn.execute("UPDATE todos SET done_at = '2020-01-01 00:00:00'")
    assert mem.todos() == []


def test_gioi_han_50_viec(tmp_path):
    mem = Memory(tmp_path / "a.db")
    assert mem.add_todos([f"Việc {i}" for i in range(60)]) == 50


def test_chat_ghi_va_gach_viec(tmp_path):
    mem = Memory(tmp_path / "a.db")
    client = FakeClient([
        reply("Ghi rồi nha!", viec_can_lam=["Mua sữa"]),
        reply("Giỏi quá!", xong_viec=["Mua sữa"]),
    ])
    brain = Brain(mem, client=client)
    brain.chat("nhớ giúp mình mua sữa")
    assert [t["viec"] for t in mem.todos(include_done=False)] == ["Mua sữa"]
    brain.chat("mua sữa rồi nè")
    assert "Việc cần làm" in client.calls[1]["system"] and "- Mua sữa" in client.calls[1]["system"]
    assert mem.todos(include_done=False) == []


def test_prompt_khong_co_muc_khi_trong():
    assert "## Việc cần làm" not in build_system_prompt("Bơ", [])
    assert "## Việc cần làm" in build_system_prompt("Bơ", [], todos=["Mua sữa"])


def test_sao_luu_giu_viec(tmp_path):
    mem = Memory(tmp_path / "a.db")
    mem.add_todos(["Mua sữa"])
    mem2 = Memory(tmp_path / "b.db")
    mem2.import_all(json.loads(json.dumps(mem.export_all())))
    assert [t["viec"] for t in mem2.todos()] == ["Mua sữa"]
    old = mem.export_all()
    del old["todos"]  # bản sao lưu cũ chưa có việc cần làm vẫn nạp được
    mem2.import_all(old)
    assert mem2.todos() == []


def test_api_viec(tmp_path):
    main._brain = Brain(Memory(tmp_path / "api.db"), client=FakeClient([]))
    c = TestClient(main.app, headers={"X-Bo": "1"})
    assert c.post("/api/viec", json={"viec": "  "}).status_code == 400
    assert c.post("/api/viec", json={"viec": "Mua sữa"}).status_code == 200
    assert c.post("/api/viec", json={"viec": "mua sữa"}).status_code == 400
    [t] = c.get("/api/viec").json()
    assert t["viec"] == "Mua sữa" and t["xong"] is False
    assert c.put(f"/api/viec/{t['id']}", json={"xong": True}).status_code == 200
    assert c.get("/api/viec").json()[0]["xong"] is True
    assert c.put("/api/viec/999", json={"xong": True}).status_code == 404
    assert c.delete(f"/api/viec/{t['id']}").status_code == 200
    assert c.get("/api/viec").json() == []


def test_viec_de_lau_duoc_nhac_kheo():
    from datetime import datetime

    now = datetime(2026, 10, 10, 9, 0)
    todos = [
        {"viec": "Trả sách", "created_at": "2026-10-05 08:00:00"},
        {"viec": "Mua sữa", "created_at": "2026-10-09 20:00:00"},
        {"viec": "Lỗi giờ", "created_at": "abc"},
    ]
    p = build_system_prompt("Bơ", [], now=now, todos=todos)
    assert "- Trả sách (ghi 5 ngày trước)" in p and "- Mua sữa\n" in p and "- Lỗi giờ\n" in p
    assert "nhắc khéo" in p
    assert "nhắc khéo" not in build_system_prompt("Bơ", [], now=now, todos=todos[1:])


def test_xong_viec_co_ghi_chu_tuoi_van_gach_duoc(tmp_path):
    mem = Memory(tmp_path / "a.db")
    mem.add_todos(["Mua sữa"])
    mem.done_todos(["Mua sữa (ghi 4 ngày trước)"])
    assert mem.todos(include_done=False) == []


def test_bo_danh_dau_khong_tao_viec_trung(tmp_path):
    import pytest

    mem = Memory(tmp_path / "a.db")
    mem.add_todos(["Mua sữa"])
    [old] = mem.todos()
    mem.set_todo_done(old["id"], True)
    mem.add_todos(["Mua sữa"])
    with pytest.raises(ValueError):
        mem.set_todo_done(old["id"], False)
    assert len(mem.todos(include_done=False)) == 1


def test_viec_xong_thieu_gio_xong_cung_duoc_don(tmp_path):
    mem = Memory(tmp_path / "a.db")
    mem.conn.execute("INSERT INTO todos (content, done) VALUES ('Cũ', 1)")
    assert mem.todos() == []


def test_api_bo_danh_dau_trung_bao_409(tmp_path):
    main._brain = Brain(Memory(tmp_path / "api.db"), client=FakeClient([]))
    c = TestClient(main.app, headers={"X-Bo": "1"})
    c.post("/api/viec", json={"viec": "Mua sữa"})
    [t] = c.get("/api/viec").json()
    c.put(f"/api/viec/{t['id']}", json={"xong": True})
    c.post("/api/viec", json={"viec": "Mua sữa"})
    assert c.put(f"/api/viec/{t['id']}", json={"xong": False}).status_code == 409


def test_brain_gui_ca_50_viec(tmp_path):
    mem = Memory(tmp_path / "a.db")
    mem.add_todos([f"Việc số {i}" for i in range(45)])
    client = FakeClient([reply()])
    Brain(mem, client=client).chat("còn gì không")
    assert "Việc số 44" in client.calls[0]["system"]
