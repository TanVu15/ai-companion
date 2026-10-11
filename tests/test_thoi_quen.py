"""Test thói quen hằng ngày: theo dõi, đánh dấu, chuỗi ngày."""
import json
from datetime import date, timedelta

import pytest

from app.brain import Brain, build_system_prompt, parse_reply
from app.memory import Memory
from tests.test_api import make_client
from tests.test_brain import FakeClient


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "t.db")


def reply(noi="Ok", **extra):
    return json.dumps({"noi": noi, "cam_xuc": "vui", "hanh_dong": "khong", **extra})


def test_them_danh_dau_chuoi(memory):
    assert memory.add_habits(["Đọc sách", "đọc sách.", " "]) == 1
    (h,) = memory.habits()
    today = date(2026, 10, 10)
    for k in (1, 2, 3, 6):
        memory.set_habit_done(h["id"], True, today - timedelta(days=k))
    (h,) = memory.habits(today)
    assert h["hom_nay"] is False and h["chuoi"] == 3 and h["tuan"] == 4
    memory.done_habits(["Đọc sách (chuỗi 3 ngày)"], today)
    (h,) = memory.habits(today)
    assert h["hom_nay"] and h["chuoi"] == 4 and h["tuan"] == 5
    memory.set_habit_done(h["id"], False, today)
    assert memory.habits(today)[0]["chuoi"] == 3
    assert not memory.set_habit_done(999, True)
    memory.add_habits([f"T{i}" for i in range(20)])
    assert len(memory.habits()) == Memory.HABIT_MAX
    memory.delete_habit(h["id"])
    assert "Đọc sách" not in [x["ten"] for x in memory.habits()]
    assert memory.conn.execute("SELECT COUNT(*) FROM habit_log WHERE habit_id = ?", (h["id"],)).fetchone()[0] == 0


def test_prompt_va_chat(memory):
    p = build_system_prompt("P", [], habits=[{"ten": "Chạy bộ", "hom_nay": False, "chuoi": 5, "tuan": 6}])
    assert "## Thói quen hằng ngày" in p and "- Chạy bộ (hôm nay chưa làm; chuỗi 5 ngày liền; 6/7 ngày qua)" in p
    r = parse_reply(reply(thoi_quen_moi=["Chạy bộ"], thoi_quen_xong=["x"]))
    assert r.thoi_quen_moi == ["Chạy bộ"] and "thoi_quen_moi" not in r.to_dict()
    client = FakeClient([reply(thoi_quen_moi=["Chạy bộ"]), reply(thoi_quen_xong=["Chạy bộ"])])
    brain = Brain(memory, client=client)
    brain.chat("theo dõi giúp mình thói quen chạy bộ")
    brain.chat("chạy bộ xong rồi nè")
    assert "- Chạy bộ (hôm nay chưa làm" in client.calls[1]["system"]
    assert memory.habits()[0]["hom_nay"] is True


def test_api_va_sao_luu(tmp_path):
    c = make_client(tmp_path, [])
    assert c.post("/api/thoi-quen", json={"ten": "Uống nước"}).status_code == 200
    assert c.post("/api/thoi-quen", json={"ten": "uống nước"}).status_code == 400
    assert c.post("/api/thoi-quen", json={"ten": " "}).status_code == 400
    (h,) = c.get("/api/thoi-quen").json()
    assert c.put(f"/api/thoi-quen/{h['id']}", json={"xong": True}).status_code == 200
    assert c.put("/api/thoi-quen/999", json={"xong": True}).status_code == 404
    assert c.get("/api/thoi-quen").json()[0]["hom_nay"] is True
    backup = c.get("/api/sao-luu").json()
    assert backup["habits"][0]["id"] == h["id"] and backup["habit_log"][0]["habit_id"] == h["id"]
    assert c.delete(f"/api/thoi-quen/{h['id']}").status_code == 200
    assert c.get("/api/thoi-quen").json() == []
    assert c.post("/api/khoi-phuc", json=backup).status_code == 200
    assert c.get("/api/thoi-quen").json()[0]["hom_nay"] is True


def test_ten_co_ngoac(memory):
    memory.add_habits(["Uống nước (2 lít)", "Chạy bộ"])
    memory.done_habits(["Uống nước (2 lít) (hôm nay chưa làm; chuỗi 0 ngày liền; 0/7 ngày qua)", "Chạy bộ (2 lít)"])
    hs = {h["ten"]: h["hom_nay"] for h in memory.habits()}
    assert hs == {"Uống nước (2 lít)": True, "Chạy bộ": True}
    memory.add_habits(["Đọc sách"])
    memory.done_habits(["Uống nước"])  # tên khác thì không đánh nhầm
    assert {h["ten"]: h["hom_nay"] for h in memory.habits()}["Đọc sách"] is False


def test_cong_thiet_bi(tmp_path, monkeypatch):
    from app import config, main

    c = make_client(tmp_path, [])
    main._brain.memory.add_habits(["Đọc sách"])
    monkeypatch.setattr(config, "DEVICE_KEY", "k")
    r = c.get("/api/thiet-bi/thoi-quen?khong_dau=1", headers={"X-Device-Key": "k"}).json()
    assert r == [{"ten": "Doc sach", "hom_nay": False, "chuoi": 0}]
    assert c.get("/api/thiet-bi/thoi-quen", headers={"X-Device-Key": "sai"}).status_code == 401
