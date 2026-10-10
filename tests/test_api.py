"""Test máy chủ web với bộ não giả."""
import json

from fastapi.testclient import TestClient

from app import main
from app.brain import Brain
from app.memory import Memory
from tests.test_brain import FakeClient


def make_client(tmp_path, replies):
    main._brain = Brain(Memory(tmp_path / "api.db"), client=FakeClient(replies))
    return TestClient(main.app, headers={"X-Bo": "1"})


def test_index_served(tmp_path):
    c = make_client(tmp_path, [])
    r = c.get("/")
    assert r.status_code == 200 and "Nhắn gì đó" in r.text


def test_chat_endpoint(tmp_path):
    c = make_client(tmp_path, [json.dumps({"noi": "Hello!", "cam_xuc": "vui", "hanh_dong": "gat_dau"})])
    r = c.post("/api/chat", json={"text": "hi"})
    assert r.status_code == 200
    assert r.json() == {"noi": "Hello!", "cam_xuc": "vui", "hanh_dong": "gat_dau"}
    assert len(c.get("/api/history").json()) == 2


def test_empty_message_rejected(tmp_path):
    c = make_client(tmp_path, [])
    assert c.post("/api/chat", json={"text": "   "}).status_code == 400


def test_brain_error_returns_502(tmp_path):
    c = make_client(tmp_path, [])  # không có câu trả lời nào -> FakeClient báo lỗi
    r = c.post("/api/chat", json={"text": "hi"})
    assert r.status_code == 502


def test_xem_va_xoa_dieu_da_nho(tmp_path):
    c = make_client(tmp_path, [])
    main._brain.memory.add_facts(["Tên là Tân", "Thích gym", "Sai"])
    assert c.get("/api/facts").json() == ["Tên là Tân", "Thích gym", "Sai"]
    assert c.request("DELETE", "/api/facts", json={"content": "Sai"}).status_code == 200
    assert c.get("/api/facts").json() == ["Tên là Tân", "Thích gym"]
    assert c.delete("/api/facts/all").status_code == 200
    assert c.get("/api/facts").json() == []


def test_trang_chu_co_nut_xem_tri_nho(tmp_path):
    c = make_client(tmp_path, [])
    assert "Bơ nhớ gì về mình?" in c.get("/").text


def test_password_required_when_set(tmp_path, monkeypatch):
    import base64

    from app import config

    monkeypatch.setattr(config, "APP_PASSWORD", "bo123")
    c = make_client(tmp_path, [])
    r = c.get("/")
    assert r.status_code == 401 and "Basic" in r.headers["www-authenticate"]
    bad = base64.b64encode(b"tan:sai").decode()
    assert c.get("/", headers={"Authorization": f"Basic {bad}"}).status_code == 401
    good = base64.b64encode(b"tan:bo123").decode()
    assert c.get("/api/facts", headers={"Authorization": f"Basic {good}"}).status_code == 200


def test_no_password_by_default(tmp_path):
    c = make_client(tmp_path, [])
    assert c.get("/api/facts").status_code == 200


def test_index_has_voice_controls(tmp_path):
    c = make_client(tmp_path, [])
    html = c.get("/").text
    assert 'id="mic"' in html and 'id="voiceBtn"' in html and "/web/app.js" in html
    js = c.get("/web/app.js")
    assert "vi-VN" in js.text and js.headers["cache-control"] == "no-cache"


def test_cost_endpoint(tmp_path):
    c = make_client(tmp_path, [json.dumps({"noi": "Hello!"})])
    c.post("/api/chat", json={"text": "hi"})
    d = c.get("/api/chi-phi").json()
    assert d["hom_nay"]["calls"] == 1 and d["thang_nay"]["calls"] == 1 and d["da_tra_loi_hom_nay"] == 1
    assert 'id="openCost"' in c.get("/").text


def test_backup_and_restore(tmp_path):
    c = make_client(tmp_path, [json.dumps({"noi": "Chào Tân!", "ghi_nho": ["Tên là Tân"], "hoi_tham": ["Mai thi"]})])
    c.post("/api/chat", json={"text": "mình là Tân, mai thi"})
    r = c.get("/api/sao-luu")
    assert r.status_code == 200 and "attachment" in r.headers["content-disposition"]
    backup = r.content
    assert "Tên là Tân" in backup.decode("utf-8")  # chữ có dấu giữ nguyên, dễ đọc

    c2 = make_client(tmp_path / "moi", [])
    assert c2.get("/api/facts").json() == []
    assert c2.post("/api/khoi-phuc", content=backup, headers={"Content-Type": "application/json"}).json() == {"ok": True}
    assert c2.get("/api/facts").json() == ["Tên là Tân"]
    assert [m["content"] for m in c2.get("/api/history").json()] == ["mình là Tân, mai thi", "Chào Tân!"]
    assert main._brain.memory.export_all()["followups"][0]["content"] == "Mai thi"


def test_restore_rejects_bad_file(tmp_path):
    c = make_client(tmp_path, [json.dumps({"noi": "x", "ghi_nho": ["Giữ lại"]})])
    c.post("/api/chat", json={"text": "hi"})
    h = {"Content-Type": "application/json"}
    assert c.post("/api/khoi-phuc", content=b"khong phai json", headers=h).status_code in (400, 422)
    assert c.post("/api/khoi-phuc", content=b'{"facts": []}', headers=h).status_code == 400
    bad = json.dumps({"phien_ban": 1, "facts": [{"content": None}]}).encode()
    assert c.post("/api/khoi-phuc", content=bad, headers=h).status_code == 400
    # gửi kiểu text/plain (cách trang lạ hay dùng để lén gửi) bị từ chối
    wipe = c.post("/api/khoi-phuc", content=b'{"phien_ban": 1}', headers={"Content-Type": "text/plain"})
    assert wipe.status_code == 422
    assert c.get("/api/facts").json() == ["Giữ lại"]  # lỗi thì trí nhớ cũ còn nguyên


def test_history_paging(tmp_path):
    c = make_client(tmp_path, [])
    mem = main._brain.memory
    for i in range(7):
        mem.add_message("user", f"tin {i}")
    page = c.get("/api/history?limit=3").json()
    assert [m["content"] for m in page] == ["tin 4", "tin 5", "tin 6"] and "created_at" in page[0]
    older = c.get(f"/api/history?limit=3&before_id={page[0]['id']}").json()
    assert [m["content"] for m in older] == ["tin 1", "tin 2", "tin 3"]


def test_health_reports_missing_key(tmp_path, monkeypatch):
    from app import config

    monkeypatch.setattr(config, "DEMO", False)
    monkeypatch.setattr(config, "ANTHROPIC_API_KEY", "")
    monkeypatch.setattr(config, "DB_PATH", tmp_path / "data" / "x.db")
    c = make_client(tmp_path, [])
    d = c.get("/api/suc-khoe").json()
    assert d["ok"] is False
    [key] = [k for k in d["kiem_tra"] if k["ten"] == "API key"]
    assert key["muc"] == "loi" and "ANTHROPIC_API_KEY" in key["ghi_chu"]


def test_health_ok_with_key(tmp_path, monkeypatch):
    from app import config

    monkeypatch.setattr(config, "DEMO", False)
    monkeypatch.setattr(config, "ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setattr(config, "DB_PATH", tmp_path / "data" / "x.db")
    d = make_client(tmp_path, []).get("/api/suc-khoe").json()
    assert d["ok"] is True  # thiếu mật khẩu/ngân sách chỉ là cảnh báo
    assert {k["ten"] for k in d["kiem_tra"]} >= {"API key", "Tính cách", "Dữ liệu"}


def test_home_screen_files(tmp_path):
    c = make_client(tmp_path, [])
    html = c.get("/").text
    assert 'rel="manifest"' in html and 'apple-touch-icon' in html
    m = c.get("/web/manifest.json").json()
    assert m["short_name"] == "Bơ" and m["display"] == "standalone"
    for icon in m["icons"]:
        r = c.get(icon["src"])
        assert r.status_code == 200 and r.content[:4] == b"\x89PNG"



def test_changes_need_x_bo_header(tmp_path):
    from fastapi.testclient import TestClient

    make_client(tmp_path, [])
    bare = TestClient(main.app)  # giống một trang web lạ: không gắn được header X-Bo
    assert bare.post("/api/chat", json={"text": "hi"}).status_code == 403
    assert bare.delete("/api/facts/all").status_code == 403
    assert bare.get("/api/nhac").status_code == 403
    assert bare.get("/api/facts").status_code == 200  # chỉ đọc thì không cần


def test_errors_written_to_log_without_message_text(tmp_path):
    import logging

    from app.nhat_ky import bat_ghi_file, log

    path = tmp_path / "loi.log"
    bat_ghi_file(path)
    bat_ghi_file(path)  # gọi lại không bị ghi 2 lần
    try:
        c = make_client(tmp_path, [])  # FakeClient hết câu trả lời → lỗi
        c.post("/api/chat", json={"text": "bí mật của Tân"})
        for h in log.handlers:
            h.flush()
        text = path.read_text(encoding="utf-8")
        assert text.count("Trả lời lỗi") == 1 and "IndexError" in text
        assert "bí mật của Tân" not in text
    finally:
        for h in list(log.handlers):
            if isinstance(h, logging.FileHandler):
                log.removeHandler(h)
                h.close()


def test_history_keeps_emotion(tmp_path):
    c = make_client(tmp_path, [json.dumps({"noi": "Hihi", "cam_xuc": "hao_hung"})])
    c.post("/api/chat", json={"text": "hi"})
    h = c.get("/api/history").json()
    assert h[0]["cam_xuc"] is None and h[1]["cam_xuc"] == "hao_hung"


def test_old_database_gets_emotion_column(tmp_path):
    import sqlite3

    db = tmp_path / "cu.db"
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT NOT NULL,"
                " content TEXT NOT NULL, created_at TEXT DEFAULT (datetime('now', 'localtime')))")
    con.execute("INSERT INTO messages (role, content) VALUES ('user', 'tin cũ')")
    con.commit()
    con.close()
    mem = Memory(db)  # mở bằng bản mới: tự thêm cột, tin cũ còn nguyên
    assert mem.history_page()[0]["content"] == "tin cũ"
    mem.add_message("assistant", "mới", "vui")
    assert mem.history_page()[-1]["cam_xuc"] == "vui"


def test_tim_trong_lich_su(tmp_path):
    c = make_client(tmp_path, [])
    m = main._brain.memory
    m.add_message("user", "Tối nay mình đi Đá Bóng")
    m.add_message("assistant", "Chúc đá vui nha!")
    m.add_message("user", "Mai đi bơi")
    r = c.get("/api/tim", params={"q": "da bong"}).json()
    assert [x["content"] for x in r] == ["Tối nay mình đi Đá Bóng"]
    r = c.get("/api/tim", params={"q": "đá"}).json()
    assert [x["content"] for x in r] == ["Chúc đá vui nha!", "Tối nay mình đi Đá Bóng"]  # mới nhất trước
    assert c.get("/api/tim", params={"q": " a "}).json() == []  # quá ngắn
    assert c.get("/api/tim", params={"q": "xyz"}).json() == []
    assert len(c.get("/api/tim", params={"q": "đi", "limit": 1}).json()) == 1


def test_tai_tro_chuyen_txt(tmp_path):
    c = make_client(tmp_path, [])
    m = main._brain.memory
    assert "Chưa có tin nhắn" in c.get("/api/tai-chat").text
    m.add_message("user", "Chào Bơ")
    m.add_message("assistant", "Chào Tân!")
    m.add_message("user", "Mai gặp")
    m.conn.execute("UPDATE messages SET created_at = '2026-10-09 20:05:00' WHERE id <= 2")
    m.conn.execute("UPDATE messages SET created_at = '2026-10-10 08:30:00' WHERE id = 3")
    m.conn.commit()
    r = c.get("/api/tai-chat")
    assert r.status_code == 200 and "attachment" in r.headers["content-disposition"]
    assert r.text.lstrip("﻿") == (
        "===== 09/10/2026 =====\n[20:05] Bạn: Chào Bơ\n[20:05] Bơ: Chào Tân!\n\n"
        "===== 10/10/2026 =====\n[08:30] Bạn: Mai gặp\n"
    )
