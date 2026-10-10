"""Test lời nhắc theo giờ (bộ não giả)."""
import json
from datetime import datetime, timedelta

import pytest

from app import config
from app.brain import Brain, parse_reply
from app.memory import Memory
from tests.test_api import make_client
from tests.test_brain import FakeClient


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "n.db")


def fmt(dt):
    return dt.strftime("%Y-%m-%d %H:%M")


def test_parse_reminders_ignores_junk():
    r = parse_reply(json.dumps({"noi": "Ok", "nhac": [{"luc": "2026-10-10 20:00", "viec": "Gọi mẹ"}, "rác", 3]}))
    assert r.nhac == [{"luc": "2026-10-10 20:00", "viec": "Gọi mẹ"}]
    assert parse_reply(json.dumps({"noi": "Ok", "nhac": "sai"})).nhac == []
    assert "nhac" not in r.to_dict()


def test_add_reminders_validates(memory):
    now = datetime(2026, 10, 10, 18, 0)
    n = memory.add_reminders([
        {"luc": "2026-10-10 20:00", "viec": "Gọi mẹ"},
        {"luc": "2026-10-10 20:00", "viec": "gọi mẹ"},     # trùng
        {"luc": "2026-10-09 20:00", "viec": "Đã qua"},     # giờ đã qua
        {"luc": "tối nay", "viec": "Sai giờ"},
        {"luc": "2026-10-10 21:00", "viec": "  "},
    ], now=now)
    assert n == 1 and [r["viec"] for r in memory.upcoming_reminders()] == ["Gọi mẹ"]


def test_due_reminder_fires_once(memory):
    now = datetime.now()
    memory.add_reminders([{"luc": fmt(now + timedelta(minutes=30)), "viec": "Gọi mẹ"}])
    assert memory.pop_due_reminders(now) == []
    assert [r["viec"] for r in memory.pop_due_reminders(now + timedelta(minutes=31))] == ["Gọi mẹ"]
    assert memory.pop_due_reminders(now + timedelta(minutes=32)) == []


def test_chat_creates_reminder_and_brain_announces(memory):
    soon = fmt(datetime.now())  # tới giờ ngay
    client = FakeClient([json.dumps({"noi": "Ok, 8h Bơ nhắc nha!", "nhac": [{"luc": soon, "viec": "Gọi điện cho mẹ"}]})])
    brain = Brain(memory, client=client)
    brain.chat("8h tối nhắc mình gọi mẹ")
    assert "Bây giờ là" in client.calls[0]["system"]
    [r] = brain.due_reminders()
    assert r.noi == "Tới giờ rồi nè: gọi điện cho mẹ!" and r.cam_xuc == "hao_hung"
    assert memory.recent_messages(5)[-1]["content"] == r.noi  # lưu vào lịch sử
    assert brain.due_reminders() == [] and len(client.calls) == 1  # nhắc không tốn câu API


def test_reminder_endpoints(tmp_path, monkeypatch):
    c = make_client(tmp_path, [])
    from app import main

    mem = main._brain.memory
    mem.add_reminders([{"luc": fmt(datetime.now() + timedelta(hours=2)), "viec": "Đi ngủ sớm"},
                       {"luc": fmt(datetime.now()), "viec": "Uống nước"}])
    assert len(c.get("/api/nhac/sap-toi").json()) == 2
    assert [x["noi"] for x in c.get("/api/nhac").json()] == ["Tới giờ rồi nè: uống nước!"]
    [later] = c.get("/api/nhac/sap-toi").json()
    c.delete(f"/api/nhac/{later['id']}")
    assert c.get("/api/nhac/sap-toi").json() == []
    monkeypatch.setattr(config, "DEVICE_KEY", "k")
    assert c.get("/api/thiet-bi/nhac", headers={"X-Device-Key": "k"}).json() == []


def test_late_reminder_says_it_is_late():
    from app.brain import reminder_text

    now = datetime(2026, 10, 11, 7, 0)
    assert reminder_text("Gọi mẹ", "2026-10-11 06:55", now) == "Tới giờ rồi nè: gọi mẹ!"
    late = reminder_text("Gọi mẹ", "2026-10-10 20:00", now)
    assert "20:00 10/10" in late and "Trễ rồi" in late


def test_reminder_does_not_block_greeting(memory):
    from tests.test_hoi_tham import set_age

    memory.add_message("user", "mai thi")
    memory.add_followups(["Đi thi"])
    set_age(memory, "messages", 20)
    set_age(memory, "followups", 20)
    memory.add_reminders([{"luc": fmt(datetime.now()), "viec": "Uống nước"}])
    brain = Brain(memory, client=FakeClient([json.dumps({"noi": "Thi sao rồi?"})]))
    brain.due_reminders()  # lời nhắc tự động không tính là "vừa nói chuyện"
    assert brain.greet().noi == "Thi sao rồi?"


def test_restore_missing_created_at_uses_default(memory):
    memory.import_all({"phien_ban": 1, "messages": [{"role": "user", "content": "a"}],
                       "reminders": [{"content": "Gọi mẹ", "due_at": "2099-01-01 08:00"}]})
    assert memory.last_message_time() is not None
    assert memory.upcoming_reminders()[0]["viec"] == "Gọi mẹ"


def test_nhac_lap_lai_moi_ngay(memory):
    now = datetime(2026, 10, 10, 9, 0)
    # "7h sáng mỗi ngày" nói lúc 9h: lần đầu là 7h sáng mai
    assert memory.add_reminders([{"luc": "2026-10-10 07:00", "viec": "Uống nước", "lap": "ngay"},
                                 {"luc": "2026-10-10 07:00", "viec": "Một lần, đã qua"}], now) == 1
    [r] = memory.upcoming_reminders()
    assert (r["luc"], r["lap"]) == ("2026-10-11 07:00", "ngay")
    assert [x["viec"] for x in memory.pop_due_reminders(datetime(2026, 10, 11, 7, 0))] == ["Uống nước"]
    assert memory.upcoming_reminders()[0]["luc"] == "2026-10-12 07:00"  # dời sang mai, không mất
    # Tắt máy 3 ngày: chỉ nhắc 1 lần rồi dời tới lần kế tiếp trong tương lai
    assert len(memory.pop_due_reminders(datetime(2026, 10, 15, 8, 0))) == 1
    assert memory.upcoming_reminders()[0]["luc"] == "2026-10-16 07:00"


def test_nhac_lap_lai_moi_tuan_va_rac(memory):
    now = datetime(2026, 10, 10, 9, 0)
    memory.add_reminders([{"luc": "2026-10-12 20:00", "viec": "Họp nhóm", "lap": "tuan"},
                          {"luc": "2026-10-12 21:00", "viec": "Lặp lạ", "lap": "nam"}], now)
    a, b = memory.upcoming_reminders()
    assert (a["lap"], b["lap"]) == ("tuan", "")  # kiểu lặp lạ → coi như một lần
    memory.pop_due_reminders(datetime(2026, 10, 12, 20, 0))
    assert memory.upcoming_reminders()[0]["luc"] == "2026-10-12 21:00"
    assert memory.upcoming_reminders()[1]["luc"] == "2026-10-19 20:00"


def test_nhac_lap_lai_sao_luu(memory, tmp_path):
    memory.add_reminders([{"luc": fmt(datetime.now() + timedelta(hours=1)), "viec": "Thuốc", "lap": "ngay"}])
    data = memory.export_all()
    m2 = Memory(tmp_path / "n2.db")
    m2.import_all(data)
    assert m2.upcoming_reminders()[0]["lap"] == "ngay"


def test_nhac_lai_sau_10_phut(tmp_path):
    c = make_client(tmp_path, [])
    mem = main_memory()
    mem.add_reminders([{"luc": fmt(datetime.now()), "viec": "Uống nước"}])
    [x] = c.get("/api/nhac").json()
    assert x["viec"] == "Uống nước" and x["noi"] == "Tới giờ rồi nè: uống nước!"
    r = c.post("/api/nhac/hoan", json={"viec": "Uống nước"})
    assert r.status_code == 200
    [up] = c.get("/api/nhac/sap-toi").json()
    assert up["viec"] == "Uống nước" and up["luc"] == r.json()["luc"] and up["lap"] == ""
    assert up["luc"] > fmt(datetime.now() + timedelta(minutes=8))
    assert c.post("/api/nhac/hoan", json={"viec": " "}).status_code == 400
    assert c.post("/api/nhac/hoan", json={"viec": "x", "phut": 0}).status_code == 400


def main_memory():
    from app import main

    return main._brain.memory


def test_nhac_lap_lai_khong_ghi_trung_khac_ngay(memory):
    now = datetime(2026, 10, 10, 7, 0)
    memory.add_reminders([{"luc": "2026-10-10 08:00", "viec": "Uống nước", "lap": "ngay"}], now)
    # AI ghi lại cùng lời nhắc nhưng từ ngày mai → vẫn là một
    assert memory.add_reminders([{"luc": "2026-10-11 08:00", "viec": "uống nước", "lap": "ngay"}], now) == 0
    memory.add_reminders([{"luc": "2026-10-12 20:00", "viec": "Họp", "lap": "tuan"}], now)
    assert memory.add_reminders([{"luc": "2026-10-19 20:00", "viec": "Họp", "lap": "tuan"}], now) == 0
    assert memory.add_reminders([{"luc": "2026-10-13 20:00", "viec": "Họp", "lap": "tuan"}], now) == 1  # khác thứ
    assert len(memory.upcoming_reminders()) == 3


def test_nhac_lai_du_10_phut(memory):
    brain = Brain(memory, client=FakeClient([]))
    assert brain.snooze("X", 10, now=datetime(2026, 10, 10, 9, 0, 40)) == "2026-10-10 09:11"


def test_loi_nhac_khong_tinh_vao_gioi_han_ngay(memory):
    memory.add_reminders([{"luc": fmt(datetime.now()), "viec": "Uống nước"}])
    Brain(memory, client=FakeClient([])).due_reminders()
    assert memory.replies_today() == 0


def test_thiet_bi_nhac_khong_dau(tmp_path, monkeypatch):
    c = make_client(tmp_path, [])
    monkeypatch.setattr(config, "DEVICE_KEY", "k")
    main_memory().add_reminders([{"luc": fmt(datetime.now()), "viec": "Uống nước"}])
    [x] = c.get("/api/thiet-bi/nhac?khong_dau=1", headers={"X-Device-Key": "k"}).json()
    assert x["viec"] == "Uong nuoc" and x["noi"] == "Toi gio roi ne: uong nuoc!"


def test_loi_nhac_co_id_de_ghim_nhung_thiet_bi_khong_nhan(tmp_path, monkeypatch):
    c = make_client(tmp_path, [])
    monkeypatch.setattr(config, "DEVICE_KEY", "k")
    main_memory().add_reminders([{"luc": fmt(datetime.now()), "viec": "A"}])
    [x] = c.get("/api/nhac").json()
    assert x["id"] > 0 and c.post(f"/api/ghim/{x['id']}", json={"ghim": True}).status_code == 200
    main_memory().add_reminders([{"luc": fmt(datetime.now()), "viec": "B"}])
    [y] = c.get("/api/thiet-bi/nhac", headers={"X-Device-Key": "k"}).json()
    assert "id" not in y and y["viec"] == "B"


def test_sua_loi_nhac(tmp_path):
    from datetime import datetime as _dt

    import pytest as _pt

    from app.memory import Memory as _M

    mem = _M(tmp_path / "s.db")
    now = _dt(2026, 10, 10, 9, 0)
    mem.add_reminders([{"luc": "2026-10-10 20:00", "viec": "Gọi mẹ"}], now=now)
    [r] = mem.upcoming_reminders()
    assert mem.update_reminder(r["id"], "Gọi  bố", "2026-10-11T21:30", "", now=now)
    assert mem.upcoming_reminders() == [{"id": r["id"], "viec": "Gọi bố", "luc": "2026-10-11 21:30", "lap": ""}]
    # lặp lại mỗi ngày: giờ đã qua thì dời tới lần sau
    assert mem.update_reminder(r["id"], "Uống nước", "2026-10-01 07:00", "ngay", now=now)
    assert mem.upcoming_reminders()[0]["luc"] == "2026-10-11 07:00"
    for viec, luc in [("", "2026-10-11 07:00"), ("x", "hôm nay"), ("x", "2026-10-09 07:00")]:
        with _pt.raises(ValueError):
            mem.update_reminder(r["id"], viec, luc, "", now=now)
    assert mem.update_reminder(999, "x", "2026-10-11 07:00", "", now=now) is False


def test_api_sua_loi_nhac(tmp_path):
    from tests.test_api import make_client

    c = make_client(tmp_path, [])
    from app import main as _main

    _main.get_brain().memory.add_reminders([{"luc": "2099-01-01 08:00", "viec": "Gọi mẹ"}])
    [r] = c.get("/api/nhac/sap-toi").json()
    assert c.put(f"/api/nhac/{r['id']}", json={"viec": "Gọi bố", "luc": "2099-01-02T09:15"}).status_code == 200
    assert c.get("/api/nhac/sap-toi").json()[0]["luc"] == "2099-01-02 09:15"
    assert c.put(f"/api/nhac/{r['id']}", json={"viec": "x", "luc": "2000-01-01 09:00"}).status_code == 400
    assert c.put("/api/nhac/999", json={"viec": "x", "luc": "2099-01-01 09:00"}).status_code == 404


def test_sua_loi_nhac_khong_tao_trung(tmp_path):
    from datetime import datetime as _dt

    import pytest as _pt

    from app.memory import Memory as _M

    mem = _M(tmp_path / "d.db")
    now = _dt(2026, 10, 10, 9, 0)
    mem.add_reminders([{"luc": "2026-10-11 08:00", "viec": "A"}, {"luc": "2026-10-12 08:00", "viec": "A"}], now=now)
    second = mem.upcoming_reminders()[1]
    with _pt.raises(ValueError):
        mem.update_reminder(second["id"], "a", "2026-10-11 08:00", "", now=now)
    assert mem.update_reminder(second["id"], "A", "2026-10-12 08:00", "", now=now)  # sửa chính nó vẫn được


def test_nhac_ngay_thuong(tmp_path):
    from datetime import datetime

    from app.memory import Memory

    mem = Memory(tmp_path / "n.db")
    fri = datetime(2026, 10, 9, 10, 0)  # thứ Sáu
    mem.add_reminders([{"luc": "2026-10-09 08:00", "viec": "Đi làm", "lap": "ngay_thuong"}], now=fri)
    (r,) = mem.upcoming_reminders()
    assert r["luc"] == "2026-10-12 08:00" and r["lap"] == "ngay_thuong"  # qua cuối tuần → thứ Hai
    assert mem.pop_due_reminders(datetime(2026, 10, 12, 8, 0))
    assert mem.upcoming_reminders()[0]["luc"] == "2026-10-13 08:00"
    # trùng giờ, khác ngày → không thêm
    assert mem.add_reminders([{"luc": "2026-10-14 08:00", "viec": "đi làm", "lap": "ngay_thuong"}], now=fri) == 0
    # đặt vào thứ Bảy (chưa tới) → dời sang thứ Hai
    mem.add_reminders([{"luc": "2026-10-10 07:00", "viec": "Tập", "lap": "ngay_thuong"}], now=fri)
    assert [x["luc"] for x in mem.upcoming_reminders() if x["viec"] == "Tập"] == ["2026-10-12 07:00"]


def test_nhac_moi_thang(tmp_path):
    from datetime import datetime

    from app.memory import Memory

    mem = Memory(tmp_path / "m.db")
    now = datetime(2026, 10, 10, 9, 0)
    mem.add_reminders([{"luc": "2026-10-05 09:00", "viec": "Đóng tiền nhà", "lap": "thang"}], now=now)
    assert mem.upcoming_reminders()[0]["luc"] == "2026-11-05 09:00"
    mem.add_reminders([{"luc": "2027-01-31 20:00", "viec": "Tổng kết", "lap": "thang"}], now=now)
    assert Memory._next_time(datetime(2027, 1, 31, 20), "thang", datetime(2027, 1, 31, 21)) == datetime(2027, 2, 28, 20)
    assert Memory._next_time(datetime(2026, 12, 15, 8), "thang", datetime(2026, 12, 20)) == datetime(2027, 1, 15, 8)
    assert mem.add_reminders([{"luc": "2026-12-05 09:00", "viec": "đóng tiền nhà", "lap": "thang"}], now=now) == 0
    mem.pop_due_reminders(datetime(2026, 11, 5, 9, 0))
    assert [x["luc"] for x in mem.upcoming_reminders() if x["viec"] == "Đóng tiền nhà"] == ["2026-12-05 09:00"]


def test_ics_lap_moi():
    from datetime import date

    from app.lich_ics import tao_ics

    ics = tao_ics([], [{"id": 1, "viec": "A", "luc": "2026-10-12 08:00", "lap": "ngay_thuong"},
                       {"id": 2, "viec": "B", "luc": "2026-11-05 09:00", "lap": "thang"}], today=date(2026, 10, 10))
    assert "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR" in ics and "RRULE:FREQ=MONTHLY" in ics
