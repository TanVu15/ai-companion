"""Test xuất lịch .ics."""
from datetime import date, datetime

from app.am_lich import duong_sang_am
from app.lich_ics import tao_ics
from tests.test_api import make_client


def _events(ics: str) -> list[str]:
    body = ics.replace("\r\n ", "")  # mở các dòng bị gập
    return body.split("BEGIN:VEVENT")[1:]


def test_ngay_duong_va_nhac():
    ics = tao_ics(
        [{"id": 1, "ngay": "05/03", "viec": "Sinh nhật Tân, vui; nhé", "am_lich": False},
         {"id": 2, "ngay": "20/12", "viec": "Kỷ niệm", "am_lich": False}],
        [{"id": 7, "viec": "Đánh răng", "luc": "2026-10-10 21:00", "lap": "ngay"},
         {"id": 8, "viec": "Gọi mẹ", "luc": "2026-10-12 08:30", "lap": ""}],
        today=date(2026, 10, 10), now=datetime(2026, 10, 10, 1, 2, 3))
    assert ics.startswith("BEGIN:VCALENDAR\r\n") and ics.endswith("END:VCALENDAR\r\n")
    ev = _events(ics)
    assert len(ev) == 4
    assert "DTSTART;VALUE=DATE:20270305" in ev[0] and "RRULE:FREQ=YEARLY" in ev[0]
    assert "SUMMARY:Sinh nhật Tân\\, vui\; nhé" in ev[0] and "TRIGGER:-PT4H" in ev[0]
    assert "DTSTART;VALUE=DATE:20261220" in ev[1]
    assert "DTSTART:20261010T210000" in ev[2] and "RRULE:FREQ=DAILY" in ev[2]
    assert "DTSTART:20261012T083000" in ev[3] and "RRULE" not in ev[3]
    assert all(len(line.encode()) <= 75 for line in ics.split("\r\n"))
    assert ics.count("BEGIN:VALARM") == 4 and "DTSTAMP:20261010T010203Z" in ics


def test_29_thang_2():
    ev = _events(tao_ics([{"id": 1, "ngay": "29/02", "viec": "Nhuận", "am_lich": False}], [],
                         today=date(2026, 10, 10)))
    assert "DTSTART;VALUE=DATE:20270228" in ev[0] and "BYMONTHDAY=-1" in ev[0]


def test_ngay_am_lich_ghi_tung_nam():
    ev = _events(tao_ics([{"id": 3, "ngay": "15/07", "viec": "Giỗ ông", "am_lich": True}], [],
                         today=date(2026, 10, 10), so_nam_am=5))
    assert 5 <= len(ev) <= 6
    for e in ev:
        d = e.split("DTSTART;VALUE=DATE:")[1][:8]
        on = date(int(d[:4]), int(d[4:6]), int(d[6:]))
        assert on >= date(2026, 10, 10) and duong_sang_am(on)[:2] == (15, 7)
        assert "RRULE" not in e and "Giỗ ông (âm lịch 15/07)" in e
    assert len({e.split("UID:")[1].split("\r\n")[0] for e in ev}) == len(ev)  # UID không trùng


def test_ngay_30_am_thang_thieu():
    ev = _events(tao_ics([{"id": 4, "ngay": "30/12", "viec": "Tất niên", "am_lich": True}], [],
                         today=date(2026, 1, 1), so_nam_am=6))
    assert len(ev) >= 5
    for e in ev:
        d = e.split("DTSTART;VALUE=DATE:")[1][:8]
        dd, mm, _, _ = duong_sang_am(date(int(d[:4]), int(d[4:6]), int(d[6:])))
        assert mm == 12 and dd in (29, 30)


def test_api_lich(tmp_path):
    c = make_client(tmp_path, [])
    from app import main

    main._brain.memory.add_special_days([{"ngay": "20/11", "viec": "Sinh nhật mẹ"}])
    r = c.get("/api/lich.ics")
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/calendar")
    assert "Sinh nhật mẹ" in r.text and "bo-lich.ics" in r.headers["content-disposition"]


def test_api_lich_rong(tmp_path):
    c = make_client(tmp_path, [])
    r = c.get("/api/lich.ics")
    assert r.status_code == 404 and "Chưa có" in r.json()["detail"]
