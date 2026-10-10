"""Âm lịch Việt Nam (múi giờ +7), tính offline theo thuật toán của Hồ Ngọc Đức.

duong_sang_am(date) → (ngày, tháng, năm, nhuận); am_sang_duong(ngày, tháng, năm, nhuận) → date.
"""
import math
from datetime import date

TZ = 7.0


def _jd(d: date) -> int:
    return d.toordinal() + 1721425  # số ngày Julius


def _from_jd(jd: int) -> date:
    return date.fromordinal(jd - 1721425)


def _new_moon(k: int) -> int:
    """Ngày Julius của lần trăng mới thứ k (tính từ 1/1/1900), theo giờ Việt Nam."""
    T = k / 1236.85
    T2, T3 = T * T, T * T * T
    dr = math.pi / 180
    Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3
    Jd1 += 0.00033 * math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr)
    M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3
    Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3
    F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3
    C1 = (0.1734 - 0.000393 * T) * math.sin(M * dr) + 0.0021 * math.sin(2 * dr * M)
    C1 -= 0.4068 * math.sin(Mpr * dr) - 0.0161 * math.sin(dr * 2 * Mpr)
    C1 -= 0.0004 * math.sin(dr * 3 * Mpr)
    C1 += 0.0104 * math.sin(dr * 2 * F) - 0.0051 * math.sin(dr * (M + Mpr))
    C1 -= 0.0074 * math.sin(dr * (M - Mpr)) - 0.0004 * math.sin(dr * (2 * F + M))
    C1 -= 0.0004 * math.sin(dr * (2 * F - M)) + 0.0006 * math.sin(dr * (2 * F + Mpr))
    C1 += 0.0010 * math.sin(dr * (2 * F - Mpr)) + 0.0005 * math.sin(dr * (2 * Mpr + M))
    if T < -11:
        deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    else:
        deltat = -0.000278 + 0.000265 * T + 0.000262 * T2
    return int(math.floor(Jd1 + C1 - deltat + 0.5 + TZ / 24))


def _sun_longitude(jdn: int) -> int:
    """Kinh độ mặt trời lúc 0h ngày jdn, chia thành 12 phần (0..11)."""
    T = (jdn - 2451545.5 - TZ / 24) / 36525
    T2 = T * T
    dr = math.pi / 180
    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2
    DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr * M)
    DL += (0.019993 - 0.000101 * T) * math.sin(dr * 2 * M) + 0.000290 * math.sin(dr * 3 * M)
    L = (L0 + DL) * dr
    L -= math.pi * 2 * math.floor(L / (math.pi * 2))
    return int(math.floor(L / math.pi * 6))


def _month11(yy: int) -> int:
    """Ngày bắt đầu tháng 11 âm lịch (tháng chứa Đông chí) của năm dương yy."""
    off = _jd(date(yy, 12, 31)) - 2415021
    k = int(math.floor(off / 29.530588853))
    nm = _new_moon(k)
    if _sun_longitude(nm) >= 9:
        nm = _new_moon(k - 1)
    return nm


def _leap_offset(a11: int) -> int:
    k = int(math.floor((a11 - 2415021.076998695) / 29.530588853 + 0.5))
    i, last = 1, 0
    arc = _sun_longitude(_new_moon(k + i))
    while True:
        last = arc
        i += 1
        arc = _sun_longitude(_new_moon(k + i))
        if arc == last or i >= 14:
            break
    return i - 1


def duong_sang_am(d: date) -> tuple[int, int, int, bool]:
    """Ngày dương → (ngày âm, tháng âm, năm âm, có phải tháng nhuận)."""
    day_number = _jd(d)
    k = int(math.floor((day_number - 2415021.076998695) / 29.530588853))
    month_start = _new_moon(k + 1)
    if month_start > day_number:
        month_start = _new_moon(k)
    if month_start > day_number:  # đoán k cao quá một tuần trăng (vài ngày hiếm, ví dụ 2054-05-07)
        month_start = _new_moon(k - 1)
    a11 = _month11(d.year)
    b11 = a11
    if a11 >= month_start:
        lunar_year = d.year
        a11 = _month11(d.year - 1)
    else:
        lunar_year = d.year + 1
        b11 = _month11(d.year + 1)
    lunar_day = day_number - month_start + 1
    diff = int(math.floor((month_start - a11) / 29))
    leap = False
    lunar_month = diff + 11
    if b11 - a11 > 365:
        leap_diff = _leap_offset(a11)
        if diff >= leap_diff:
            lunar_month = diff + 10
            if diff == leap_diff:
                leap = True
    if lunar_month > 12:
        lunar_month -= 12
    if lunar_month >= 11 and diff < 4:
        lunar_year -= 1
    return lunar_day, lunar_month, lunar_year, leap


def am_sang_duong(ngay: int, thang: int, nam: int, nhuan: bool = False) -> date | None:
    """Ngày âm → ngày dương. Ngày không có (ví dụ tháng nhuận không tồn tại) thì None."""
    if not (1 <= thang <= 12 and 1 <= ngay <= 30):
        return None
    if thang < 11:
        a11, b11 = _month11(nam - 1), _month11(nam)
    else:
        a11, b11 = _month11(nam), _month11(nam + 1)
    k = int(math.floor(0.5 + (a11 - 2415021.076998695) / 29.530588853))
    off = thang - 11
    if off < 0:
        off += 12
    if b11 - a11 > 365:
        leap_off = _leap_offset(a11)
        leap_month = leap_off - 2
        if leap_month < 0:
            leap_month += 12
        if nhuan and thang != leap_month:
            return None
        if nhuan or off >= leap_off:
            off += 1
    elif nhuan:
        return None
    month_start = _new_moon(k + off)
    # tháng thiếu chỉ có 29 ngày
    if ngay == 30 and _new_moon(k + off + 1) - month_start < 30:
        return None
    return _from_jd(month_start + ngay - 1)


# --- Tên năm, ngày lễ ---
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]


def ten_nam(nam: int) -> str:
    """2026 → "Bính Ngọ"."""
    return f"{CAN[(nam + 6) % 10]} {CHI[(nam + 8) % 12]}"


def mo_ta_am(d: date) -> str:
    """"mùng 1 tháng 9 (nhuận) năm Bính Ngọ"."""
    ngay, thang, nam, nhuan = duong_sang_am(d)
    ten_ngay = f"mùng {ngay}" if ngay <= 10 else f"ngày {ngay}"
    return f"{ten_ngay} tháng {thang}{' nhuận' if nhuan else ''} năm {ten_nam(nam)}"


LE_DUONG = {
    (1, 1): "Tết Dương lịch", (14, 2): "Lễ Tình nhân (Valentine)", (8, 3): "Quốc tế Phụ nữ 8/3",
    (30, 4): "Ngày Giải phóng miền Nam 30/4", (1, 5): "Quốc tế Lao động 1/5", (1, 6): "Quốc tế Thiếu nhi 1/6",
    (2, 9): "Quốc khánh 2/9", (20, 10): "Ngày Phụ nữ Việt Nam 20/10", (20, 11): "Ngày Nhà giáo Việt Nam 20/11",
    (24, 12): "Đêm Giáng sinh", (25, 12): "Giáng sinh (Noel)",
}
LE_AM = {
    (1, 1): "mùng 1 Tết Nguyên đán", (2, 1): "mùng 2 Tết", (3, 1): "mùng 3 Tết", (15, 1): "Rằm tháng Giêng",
    (3, 3): "Tết Hàn thực", (10, 3): "Giỗ Tổ Hùng Vương", (15, 4): "Lễ Phật đản", (5, 5): "Tết Đoan ngọ",
    (15, 7): "Lễ Vu Lan (Rằm tháng Bảy)", (15, 8): "Tết Trung thu", (23, 12): "Ông Công Ông Táo về trời",
}


def ngay_le(d: date) -> list[str]:
    """Các ngày lễ rơi vào ngày dương d (cả lễ dương lịch và âm lịch). Tháng nhuận không tính lễ âm."""
    out = []
    if (d.day, d.month) in LE_DUONG:
        out.append(LE_DUONG[(d.day, d.month)])
    ngay, thang, nam, nhuan = duong_sang_am(d)
    if not nhuan:
        if (ngay, thang) in LE_AM:
            out.append(LE_AM[(ngay, thang)])
        if thang == 12 and duong_sang_am(date.fromordinal(d.toordinal() + 1))[:2] == (1, 1):
            out.append("Giao thừa (đêm cuối năm âm lịch)")
    return out


def le_sap_toi(d: date, days: int = 45) -> list[dict]:
    """Ngày lễ trong `days` ngày tới (không tính hôm nay), mỗi lễ một lần, gần nhất trước:
    [{"ten", "con_ngay", "ngay": date}]. Mùng 2, mùng 3 Tết bỏ (đã có mùng 1)."""
    out, seen = [], set()
    for off in range(1, days + 1):
        on = date.fromordinal(d.toordinal() + off)
        for ten in ngay_le(on):
            if ten in seen or ten in ("mùng 2 Tết", "mùng 3 Tết"):
                continue
            seen.add(ten)
            out.append({"ten": ten, "con_ngay": off, "ngay": on})
    return out


def tet_sap_toi(d: date) -> dict | None:
    """Mùng 1 Tết Nguyên đán kế tiếp (tính cả hôm nay): {"con_ngay", "ngay": date}."""
    _, _, nam, _ = duong_sang_am(d)
    for y in (nam, nam + 1):
        tet = am_sang_duong(1, 1, y)
        if tet and tet >= d:
            return {"con_ngay": (tet - d).days, "ngay": tet}
    return None
