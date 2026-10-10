"""Xuất ngày đặc biệt + lời nhắc thành file lịch .ics để thêm vào lịch điện thoại (iPhone, Google Calendar).

Không cần mạng, không tốn API. Ngày âm lịch không có luật lặp trong .ics nên ghi sẵn từng năm (mặc định 10 năm).
"""
from datetime import date, datetime, timedelta, timezone

from .am_lich import am_sang_duong, duong_sang_am

RRULE = {"ngay": "FREQ=DAILY", "tuan": "FREQ=WEEKLY", "ngay_thuong": "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR",
         "thang": "FREQ=MONTHLY"}


def _esc(text: str) -> str:
    return (text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
            .replace("\r", "").replace("\n", "\\n"))


def _fold(line: str) -> list[str]:
    """Dòng .ics dài quá 75 byte phải gập (dòng sau bắt đầu bằng dấu cách). Không cắt giữa ký tự tiếng Việt."""
    out, cur, size = [], "", 0
    for ch in line:
        n = len(ch.encode("utf-8"))
        if size + n > (75 if not out else 74):
            out.append(cur)
            cur, size = "", 0
        cur += ch
        size += n
    out.append(cur)
    return [out[0]] + [" " + x for x in out[1:]]


def _ngay_am(ngay: int, thang: int, nam: int) -> date | None:
    """Ngày âm → dương; ngày 30 mà tháng đó thiếu thì lấy ngày 29 (giống cách Bơ chúc)."""
    return am_sang_duong(ngay, thang, nam) or (am_sang_duong(29, thang, nam) if ngay == 30 else None)


def tao_ics(special_days: list[dict], reminders: list[dict], today: date | None = None,
            so_nam_am: int = 10, now: datetime | None = None) -> str:
    """special_days: [{"id", "ngay": "DD/MM", "viec", "am_lich"}]; reminders: [{"id", "viec", "luc", "lap"}]."""
    today = today or date.today()
    stamp = (now or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Bo//Ban AI//VI", "CALSCALE:GREGORIAN",
             "X-WR-CALNAME:Bơ nhắc"]

    def event(uid: str, props: list[str], nhac: str) -> None:
        lines.extend(["BEGIN:VEVENT", f"UID:{uid}@bo", f"DTSTAMP:{stamp}", *props,
                      "BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{props[-1].split(':', 1)[1]}",
                      f"TRIGGER:{nhac}", "END:VALARM", "END:VEVENT"])

    def ca_ngay(d: date) -> list[str]:
        return [f"DTSTART;VALUE=DATE:{d:%Y%m%d}", f"DTEND;VALUE=DATE:{d + timedelta(days=1):%Y%m%d}"]

    # Ngày cả ngày: nhắc lúc 20h hôm trước (TRIGGER tính từ 0h ngày đó).
    for x in special_days:
        try:
            d, m = (int(p) for p in x["ngay"].split("/"))
        except (KeyError, ValueError):
            continue
        ten = f"SUMMARY:{_esc(x['viec'])}"
        if not x.get("am_lich"):
            if (d, m) == (29, 2):  # năm không nhuận: ngày cuối tháng 2
                rule = "RRULE:FREQ=YEARLY;BYMONTH=2;BYMONTHDAY=-1"
                cuoi_t2 = lambda y: date(y, 3, 1) - timedelta(days=1)  # noqa: E731
                start = cuoi_t2(today.year) if cuoi_t2(today.year) >= today else cuoi_t2(today.year + 1)
            else:
                rule = "RRULE:FREQ=YEARLY"
                try:
                    start = date(today.year, m, d)
                    if start < today:
                        start = date(today.year + 1, m, d)
                except ValueError:
                    continue
            event(f"ngay-{x.get('id')}", [*ca_ngay(start), rule, ten], "-PT4H")
        else:
            nam = duong_sang_am(today)[2]
            for y in range(nam - 1, nam + so_nam_am + 1):
                on = _ngay_am(d, m, y)
                if on is None or on < today or on > today + timedelta(days=366 * so_nam_am):
                    continue
                event(f"ngay-am-{x.get('id')}-{y}", [*ca_ngay(on), f"SUMMARY:{_esc(x['viec'] + ' (âm lịch ' + x['ngay'] + ')')}"],
                      "-PT4H")
    for r in reminders:
        try:
            luc = datetime.strptime(str(r["luc"])[:16], "%Y-%m-%d %H:%M")
        except (KeyError, ValueError):
            continue
        props = [f"DTSTART:{luc:%Y%m%dT%H%M00}", f"DTEND:{luc + timedelta(minutes=15):%Y%m%dT%H%M00}"]
        if r.get("lap") in RRULE:
            props.append(f"RRULE:{RRULE[r['lap']]}")
        event(f"nhac-{r.get('id')}", [*props, f"SUMMARY:{_esc(r['viec'])}"], "PT0M")
    lines.append("END:VCALENDAR")
    return "\r\n".join(x for line in lines for x in _fold(line)) + "\r\n"
