"""Test tự sao lưu mỗi ngày."""
import json
from datetime import date

from fastapi.testclient import TestClient

from app import config, main
from app.brain import Brain
from app.memory import Memory
from app.sao_luu import ds_ban_sao, tu_sao_luu
from tests.test_brain import FakeClient


def test_moi_ngay_mot_ban_va_giu_7(tmp_path):
    mem = Memory(tmp_path / "t.db")
    mem.add_facts(["Thích cà phê"])
    folder = tmp_path / "sl"
    p = tu_sao_luu(mem, folder, date(2026, 10, 1))
    assert p.name == "bo-2026-10-01.json"
    assert json.loads(p.read_text(encoding="utf-8"))["facts"][0]["content"] == "Thích cà phê"
    assert tu_sao_luu(mem, folder, date(2026, 10, 1)) is None  # hôm nay có rồi
    for d in range(2, 12):
        tu_sao_luu(mem, folder, date(2026, 10, d), giu=7)
    names = [x.name for x in ds_ban_sao(folder)]
    assert len(names) == 7 and names[0] == "bo-2026-10-11.json" and names[-1] == "bo-2026-10-05.json"
    (folder / "ghi-chu.txt").write_text("x")  # file khác trong thư mục thì không đụng
    tu_sao_luu(mem, folder, date(2026, 10, 12), giu=7)
    assert (folder / "ghi-chu.txt").exists() and not list(folder.glob("*.tmp"))


def test_ban_sao_luu_nap_lai_duoc(tmp_path):
    mem = Memory(tmp_path / "t.db")
    mem.add_message("user", "chào Bơ")
    p = tu_sao_luu(mem, tmp_path / "sl", date(2026, 10, 1))
    mem2 = Memory(tmp_path / "t2.db")
    mem2.import_all(json.loads(p.read_text(encoding="utf-8")))
    assert mem2.recent_messages(5)[0]["content"] == "chào Bơ"


def _client(tmp_path, monkeypatch, replies):
    monkeypatch.setattr(config, "DEMO", False)
    main._brain = Brain(Memory(tmp_path / "a.db"), client=FakeClient(replies))
    return TestClient(main.app, headers={"X-Bo": "1"})


def test_chat_tu_sao_luu(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, ['{"noi": "Ừ", "cam_xuc": "vui", "hanh_dong": "khong"}'] * 2)
    assert c.post("/api/chat", json={"text": "hi"}).status_code == 200
    bans = ds_ban_sao(config.SAO_LUU_DIR)
    assert len(bans) == 1
    assert c.post("/api/chat", json={"text": "hi nữa"}).status_code == 200
    assert len(ds_ban_sao(config.SAO_LUU_DIR)) == 1
    checks = {k["ten"]: k for k in c.get("/api/suc-khoe").json()["kiem_tra"]}
    assert checks["Tự sao lưu"]["ok"] and "1 bản" in checks["Tự sao lưu"]["ghi_chu"]


def test_tat_tu_sao_luu(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, ['{"noi": "Ừ", "cam_xuc": "vui", "hanh_dong": "khong"}'])
    monkeypatch.setattr(config, "TU_SAO_LUU", False)
    c.post("/api/chat", json={"text": "hi"})
    assert ds_ban_sao(config.SAO_LUU_DIR) == []


def test_sao_luu_loi_khong_lam_hong_chat(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, ['{"noi": "Ừ", "cam_xuc": "vui", "hanh_dong": "khong"}'])
    (tmp_path / "chan").write_text("x")
    monkeypatch.setattr(config, "SAO_LUU_DIR", tmp_path / "chan" / "sao_luu")  # cha là file → không tạo được
    r = c.post("/api/chat", json={"text": "hi"})
    assert r.status_code == 200 and r.json()["noi"] == "Ừ"


def test_hai_tin_cung_luc_chi_ghi_mot_lan(tmp_path, monkeypatch):
    import threading

    _client(tmp_path, monkeypatch, [])
    loi = []
    monkeypatch.setattr(main.log, "warning", lambda *a: loi.append(a))
    ts = [threading.Thread(target=main._tu_sao_luu) for _ in range(8)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert len(ds_ban_sao(config.SAO_LUU_DIR)) == 1 and loi == []
