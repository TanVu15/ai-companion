"""Test ngày đặc biệt: Bơ nhớ sinh nhật/kỷ niệm và chúc đúng ngày (một lần mỗi năm)."""
import json
from datetime import date, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app import config, main
from app.brain import Brain, build_system_prompt, parse_reply
from app.memory import Memory
from tests.test_brain import FakeClient


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "t.db")


def reply(noi="Ok", **extra):
    return json.dumps({"noi": noi, "cam_xuc": "vui", "hanh_dong": "khong", **extra})


def today_ddmm(delta=0):
    return (date.today() + timedelta(days=delta)).strftime("%d/%m")


def test_parse_and_save(memory):
    r = parse_reply(reply(ngay_dac_biet=[{"ngay": "5/3", "viec": "Sinh nhật Tân"}, "rác"]))
    assert r.ngay_dac_biet == [{"ngay": "5/3", "viec": "Sinh nhật Tân"}]
    assert "ngay_dac_biet" not in r.to_dict()
    added = memory.add_special_days(r.ngay_dac_biet + [
        {"ngay": "05/03", "viec": "sinh nhật tân"},  # trùng
        {"ngay": "31/02", "viec": "Ngày sai"},
        {"ngay": "", "viec": "Không ngày"},
        {"ngay": "29/02", "viec": "Sinh nhật bạn Nhuận"},
        {"ngay": "1-12", "viec": "Kỷ niệm"},
    ])
    assert added == 3
    assert [(d["ngay"], d["viec"]) for d in memory.special_days()] == [
        ("29/02", "Sinh nhật bạn Nhuận"), ("05/03", "Sinh nhật Tân"), ("01/12", "Kỷ niệm")]


def test_today_and_leap_day(memory):
    memory.add_special_days([{"ngay": "29/02", "viec": "Nhuận"}, {"ngay": "28/02", "viec": "Hai tám"}])
    assert [d["viec"] for d in memory.special_days_today(date(2027, 2, 28))] == ["Nhuận", "Hai tám"]
    assert [d["viec"] for d in memory.special_days_today(date(2028, 2, 28))] == ["Hai tám"]
    assert [d["viec"] for d in memory.special_days_today(date(2028, 2, 29))] == ["Nhuận"]


def test_prompt_has_special_section():
    p = build_system_prompt("Bơ", [], special=[{"id": 1, "viec": "Sinh nhật Tân"}], now=datetime(2026, 3, 5, 9))
    assert "## Hôm nay là ngày đặc biệt\n- Sinh nhật Tân" in p
    assert "ngày đặc biệt\n" not in build_system_prompt("Bơ", [], now=datetime(2026, 3, 5, 9))


def test_chat_wishes_once_per_year(memory):
    memory.add_special_days([{"ngay": today_ddmm(), "viec": "Sinh nhật Tân"}, {"ngay": today_ddmm(1), "viec": "Mai"}])
    client = FakeClient([reply("Chúc mừng sinh nhật!"), reply("Ừ")])
    brain = Brain(memory, client=client)
    brain.chat("hi")
    assert "Sinh nhật Tân" in client.calls[0]["system"] and "- Mai" not in client.calls[0]["system"]
    brain.chat("hi nữa")
    assert "ngày đặc biệt\n" not in client.calls[1]["system"]  # đã chúc rồi
    assert memory.special_days_today() == []
    assert len(memory.special_days_today(only_unwished=False)) == 1


def test_chat_saves_new_special_day(memory):
    brain = Brain(memory, client=FakeClient([reply(ngay_dac_biet=[{"ngay": "20/11", "viec": "Sinh nhật mẹ"}])]))
    brain.chat("sinh nhật mẹ mình 20/11")
    assert memory.special_days()[0]["viec"] == "Sinh nhật mẹ"


def test_greet_on_special_day_even_if_recent(memory):
    memory.add_message("user", "hi")  # vừa nói chuyện xong
    memory.add_special_days([{"ngay": today_ddmm(), "viec": "Kỷ niệm 1 năm quen Bơ"}])
    client = FakeClient([reply("Chúc mừng kỷ niệm!")])
    brain = Brain(memory, client=client)
    assert brain.greet().noi == "Chúc mừng kỷ niệm!"
    assert "ngày đặc biệt" in client.calls[0]["messages"][-1]["content"]
    assert brain.greet() is None  # đã chúc rồi, lại vừa nói chuyện → im


def test_api_list_delete_and_backup(tmp_path):
    main._brain = Brain(Memory(tmp_path / "a.db"), client=FakeClient([]))
    c = TestClient(main.app, headers={"X-Bo": "1"})
    main._brain.memory.add_special_days([{"ngay": "20/11", "viec": "Sinh nhật mẹ"}])
    lst = c.get("/api/ngay-dac-biet").json()
    assert [d["viec"] for d in lst] == ["Sinh nhật mẹ"]
    backup = c.get("/api/sao-luu").json()
    assert backup["special_days"][0]["day"] == "11-20"
    assert c.delete(f"/api/ngay-dac-biet/{lst[0]['id']}").status_code == 200
    assert c.get("/api/ngay-dac-biet").json() == []
    assert c.post("/api/khoi-phuc", json=backup).status_code == 200
    assert [d["viec"] for d in c.get("/api/ngay-dac-biet").json()] == ["Sinh nhật mẹ"]


def test_told_today_not_wished_again(memory):
    brain = Brain(memory, client=FakeClient([reply("Ôi chúc mừng!", ngay_dac_biet=[{"ngay": today_ddmm(), "viec": "Sinh nhật Tân"}])]))
    brain.chat("hôm nay sinh nhật mình")
    assert memory.special_days_today() == []  # vừa chúc trong câu trả lời rồi


def test_special_days_tomorrow(memory):
    memory.add_special_days([{"ngay": "11/10", "viec": "Sinh nhật mẹ"}, {"ngay": "12/10", "viec": "Kỷ niệm"}])
    t = date(2026, 10, 10)
    assert [d["viec"] for d in memory.special_days_tomorrow(t)] == ["Sinh nhật mẹ"]
    memory.mark_eve_reminded([d["id"] for d in memory.special_days_tomorrow(t)], date(2026, 10, 11))
    assert memory.special_days_tomorrow(t) == []
    assert memory.special_days_tomorrow(date(2027, 10, 10)) != []  # năm sau nhắc lại
    # 31/12 → mai là 1/1 năm sau
    memory.add_special_days([{"ngay": "1/1", "viec": "Năm mới"}])
    assert [d["viec"] for d in memory.special_days_tomorrow(date(2026, 12, 31))] == ["Năm mới"]
    # 29/02: năm không nhuận nhắc vào 27/02
    memory.add_special_days([{"ngay": "29/2", "viec": "Sinh nhật bạn"}])
    assert [d["viec"] for d in memory.special_days_tomorrow(date(2027, 2, 27))] == ["Sinh nhật bạn"]


def _fixed_morning(monkeypatch, hour=10):
    import app.brain as b

    real = datetime.now()

    class Fixed(datetime):
        @classmethod
        def now(cls, tz=None):
            return real.replace(hour=hour, minute=0)

    monkeypatch.setattr(b, "datetime", Fixed)


def test_greet_nhac_truoc_mot_ngay_mot_lan(memory, monkeypatch):
    _fixed_morning(monkeypatch)
    memory.add_special_days([{"ngay": today_ddmm(1), "viec": "Sinh nhật mẹ"}])
    memory.add_message("user", "hi")  # vừa nói chuyện xong vẫn nhắc
    client = FakeClient([reply("Mai sinh nhật mẹ đó nha!")])
    brain = Brain(memory, client=client)
    r = brain.greet(only_occasion=True)
    assert r and r.noi == "Mai sinh nhật mẹ đó nha!"
    assert "NGÀY MAI" in client.calls[0]["messages"][-1]["content"]
    assert "Sinh nhật mẹ" in client.calls[0]["messages"][-1]["content"]
    assert brain.greet(only_occasion=True) is None  # không nhắc lại
    assert len(client.calls) == 1


def test_greet_khong_nhac_truoc_luc_nua_dem(memory, monkeypatch):
    _fixed_morning(monkeypatch, hour=2)
    memory.add_special_days([{"ngay": today_ddmm(1), "viec": "Sinh nhật mẹ"}])
    client = FakeClient([])
    assert Brain(memory, client=client).greet(only_occasion=True) is None


def test_vua_ke_ngay_mai_thi_khong_nhac_truoc(memory, monkeypatch):
    _fixed_morning(monkeypatch)
    client = FakeClient([reply("Ghi nhớ rồi!", ngay_dac_biet=[{"ngay": today_ddmm(1), "viec": "Sinh nhật mẹ"}])])
    brain = Brain(memory, client=client)
    brain.chat("mai sinh nhật mẹ mình")
    assert brain.greet(only_occasion=True) is None
    assert len(client.calls) == 1


def test_tro_chuyen_binh_thuong_khong_lam_mat_loi_nhac_truoc(memory, monkeypatch):
    _fixed_morning(monkeypatch)
    memory.add_special_days([{"ngay": today_ddmm(1), "viec": "Sinh nhật mẹ"}])
    client = FakeClient([reply("Ừa"), reply("Mai sinh nhật mẹ đó!")])
    brain = Brain(memory, client=client)
    brain.chat("chào")
    assert brain.greet(only_occasion=True).noi == "Mai sinh nhật mẹ đó!"


def test_ngay_am_lich(memory):
    assert memory.add_special_days([{"ngay": "15/7", "viec": "Giỗ ông", "am_lich": True},
                                    {"ngay": "31/7", "viec": "Sai", "am_lich": True}]) == 1
    assert memory.special_days() == [{"id": 1, "ngay": "15/07", "viec": "Giỗ ông", "am_lich": True}]
    # 15/7 âm năm 2025 là 6/9/2025, năm 2026 là 27/8/2026
    assert [d["viec"] for d in memory.special_days_today(date(2025, 9, 6))] == ["Giỗ ông"]
    assert memory.special_days_today(date(2025, 7, 15)) == []  # 15/7 dương không phải
    assert [d["viec"] for d in memory.special_days_tomorrow(date(2026, 8, 26))] == ["Giỗ ông"]
    memory.mark_wished([1], on=date(2025, 9, 6))
    assert memory.special_days_today(date(2025, 9, 6)) == []
    assert memory.special_days_today(date(2026, 8, 27)) != []  # năm âm sau vẫn chúc


def test_ngay_30_am_thang_thieu_tinh_vao_29(memory):
    from app.am_lich import am_sang_duong, duong_sang_am

    memory.add_special_days([{"ngay": "30/12", "viec": "Giỗ bà", "am_lich": True}])
    # tìm một năm tháng Chạp thiếu (29 ngày): ngày 29/12 âm mà hôm sau là mùng 1 Tết
    for nam in range(2020, 2035):
        d29 = am_sang_duong(29, 12, nam)
        if duong_sang_am(date.fromordinal(d29.toordinal() + 1))[:2] == (1, 1):
            assert [d["viec"] for d in memory.special_days_today(d29)] == ["Giỗ bà"]
            break
    else:
        raise AssertionError("không tìm thấy tháng Chạp thiếu")


def test_chat_ghi_ngay_am(memory):
    client = FakeClient([reply("Bơ nhớ rồi", ngay_dac_biet=[{"ngay": "10/3", "viec": "Giỗ cụ", "am_lich": True}])])
    Brain(memory, client=client).chat("giỗ cụ mình 10/3 âm lịch")
    assert memory.special_days()[0]["am_lich"] is True
    assert '"am_lich": true' in client.calls[0]["system"]


def _fixed_day(monkeypatch, day: datetime):
    import app.brain as b

    class Fixed(datetime):
        @classmethod
        def now(cls, tz=None):
            return day

    monkeypatch.setattr(b, "datetime", Fixed)


def test_chuc_ngay_le_mot_lan(memory, monkeypatch):
    monkeypatch.setattr(config, "CHUC_LE", True)
    _fixed_day(monkeypatch, datetime(2026, 10, 20, 9, 0))
    client = FakeClient([reply("Chúc mừng 20/10 nha!")])
    brain = Brain(memory, client=client)
    assert brain.greet(only_occasion=True).noi == "Chúc mừng 20/10 nha!"
    assert "Phụ nữ Việt Nam" in client.calls[0]["messages"][-1]["content"]
    assert brain.greet(only_occasion=True) is None


def test_khong_chuc_le_ngay_thuong_hoac_qua_som(memory, monkeypatch):
    monkeypatch.setattr(config, "CHUC_LE", True)
    _fixed_day(monkeypatch, datetime(2026, 10, 20, 5, 0))
    assert Brain(memory, client=FakeClient([])).greet(only_occasion=True) is None
    _fixed_day(monkeypatch, datetime(2026, 10, 21, 9, 0))
    assert Brain(memory, client=FakeClient([])).greet(only_occasion=True) is None
