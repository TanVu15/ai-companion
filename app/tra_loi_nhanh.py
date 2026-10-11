"""Trả lời nhanh không tốn API: câu hỏi ngắn, rõ ràng như "mấy giờ rồi?", "hôm nay ngày mấy âm?",
"còn mấy ngày nữa Tết?", "việc cần làm của mình?" thì Bơ tự trả lời bằng câu soạn sẵn.

Chỉ khớp KHI CẢ TIN NHẮN là câu hỏi đó (thêm "Bơ ơi", "vậy", "nhỉ"... vẫn được). Tin dài hơn
("mấy giờ rồi mà mình chưa ngủ được") vẫn gửi cho AI như thường, để Bơ không trả lời máy móc.
Tắt bằng TRA_LOI_NHANH=0 trong .env.
"""
import re
from datetime import datetime

from .memory import khong_dau

THU = ["thứ Hai", "thứ Ba", "thứ Tư", "thứ Năm", "thứ Sáu", "thứ Bảy", "Chủ nhật"]

# Lời gọi ở đầu và từ đệm ở cuối câu, bỏ đi trước khi so (đã bỏ dấu). Cố ý KHÔNG có "đi", "nha", "nhé", "đó":
# "mấy giờ đi?", "mấy giờ nhé" là hỏi hẹn giờ, không phải hỏi giờ hiện tại.
_DAU = r"^(?:(?:bo|be|ban|cau)\s+(?:oi|a)\s+|(?:bo|oi|e|ne|cho\s+(?:minh|to|tui|toi)\s+hoi)\s+)*"
_CUOI = r"(?:\s+(?:vay|the|nhi|a|ha|ho|ne|ta|bo|oi|ban|cau|vay ta|the nhi))*$"
_GIO = r"(?:gio|h)"
_ROI = r"(?:roi|r)"
_NAY = r"(?:hom nay|nay)\s+(?:la\s+)?"

_MAU = {
    "gio": [  # phải có "rồi" hoặc "bây giờ/hiện tại": "mấy giờ?" trơn có thể là hỏi giờ hẹn
        rf"(?:bay gio|hien tai|hien gio|gio)\s+(?:la\s+)?may {_GIO}(?:\s+{_ROI})?",
        rf"may {_GIO}\s+{_ROI}",
    ],
    "thu": [
        rf"{_NAY}thu may(?:\s+roi)?",
        rf"thu may\s+{_ROI}",
    ],
    "am": [
        rf"{_NAY}(?:ngay\s+|mung\s+)?(?:may|bao nhieu)\s+(?:am|am lich)",
        rf"{_NAY}(?:ngay\s+)?am lich\s+(?:may|bao nhieu|ngay may|ngay bao nhieu|mung may)",
        r"am lich\s+(?:hom nay|nay)(?:\s+(?:la\s+)?(?:ngay\s+)?(?:may|bao nhieu))?",
        r"ngay am\s+(?:hom nay|nay)(?:\s+(?:la\s+)?(?:may|bao nhieu))?",
    ],
    "ngay": [  # "ngày gì" thường hỏi dịp lễ → để AI trả lời
        rf"{_NAY}ngay\s+(?:may|bao nhieu)(?:\s+(?:roi|thang may))?",
        rf"{_NAY}mung may",
        rf"{_NAY}thu may\s+ngay\s+(?:may|bao nhieu)",
    ],
    "tet": [
        r"(?:con\s+)?(?:may|bao nhieu)\s+ngay\s+(?:nua\s+)?(?:la\s+|thi\s+|toi\s+|den\s+|moi\s+toi\s+)?tet(?:\s+(?:nua|roi))?",
        r"(?:con\s+)?bao lau\s+(?:nua\s+)?(?:la\s+|thi\s+|toi\s+|den\s+)?tet(?:\s+nua)?",
        r"tet\s+con\s+(?:may|bao nhieu)\s+ngay(?:\s+nua)?",
        r"bao gio\s+(?:thi\s+|moi\s+)?(?:toi\s+|den\s+|la\s+)?tet",
        r"(?:khi nao|bao gio)\s+(?:thi\s+)?tet(?:\s+(?:toi|den|nua))?",
        r"tet\s+(?:la\s+)?(?:ngay nao|ngay may|khi nao|bao gio)",
    ],
    "viec": [  # phải có "còn/có ... việc": "việc gì phải làm" trơn là câu than ("việc gì phải làm thế")
        r"(?:(?:minh|to|tui|toi|em)\s+)?(?:con|co)\s+(?:con\s+)?(?:nhung\s+)?viec\s+(?:gi|nao)\s+(?:can|phai|chua)\s+(?:lam|xong)(?:\s+(?:khong|ko|k|nua|chua|hom nay|nua khong))?",
        r"(?:danh sach\s+)?viec can lam(?:\s+(?:hom nay|cua\s+(?:minh|to|tui|toi|em)|(?:minh|to|tui|toi|em)))?(?:\s+(?:co gi|la gi|gom gi|con gi))?",
    ],
    "thoi_tiet": [
        r"(?:thoi tiet|troi)\s+(?:hom nay|bay gio|nay|ngay mai|mai)\s+(?:the nao|ra sao|sao|nhu the nao|co mua khong|co mua ko|co mua k|mua khong|nong khong|lanh khong)",
        r"(?:hom nay|bay gio|nay|ngay mai|mai)\s+(?:troi|thoi tiet)\s+(?:the nao|ra sao|sao|nhu the nao|co mua khong|co mua ko|co mua k|nong khong|lanh khong)",
        r"(?:hom nay|bay gio|nay|ngay mai|mai)\s+(?:troi\s+)?co mua\s+(?:khong|ko|k)",
        r"thoi tiet(?:\s+(?:hom nay|ngay mai|mai|bay gio))?",
        r"(?:bay gio|ngoai troi|hom nay|troi)\s+(?:dang\s+)?(?:may|bao nhieu)\s+do(?:\s+(?:c|roi))?",
    ],
    "thoi_quen": [
        r"(?:(?:danh sach|cac)\s+)?thoi quen(?:\s+(?:hom nay|cua\s+(?:minh|to|tui|toi|em)|(?:minh|to|tui|toi|em)))?(?:\s+(?:sao roi|the nao|co gi|toi dau roi))?",
        r"(?:hom nay\s+)?(?:(?:minh|to|tui|toi|em)\s+)?(?:con|co)\s+thoi quen\s+(?:nao|gi)\s+(?:chua lam|chua)(?:\s+(?:khong|ko|k|hom nay))?",
    ],
}
_RE = {k: [re.compile(_DAU + m + _CUOI) for m in v] for k, v in _MAU.items()}


def _chuan(text: str) -> str:
    t = khong_dau(text)
    t = re.sub(r"[^\w\s]", " ", t)  # bỏ ?, !, dấu phẩy, emoji
    return " ".join(t.split())


def nhan_dien(text: str) -> str:
    """Loại câu hỏi nhanh ("gio", "thu", "ngay", "am", "tet", "viec") hoặc "" nếu không phải."""
    if len(text) > 60:  # câu dài thường có ý khác → để AI trả lời
        return ""
    t = _chuan(text)
    if not t:
        return ""
    for loai, mau in _RE.items():
        if any(m.fullmatch(t) for m in mau):
            return loai
    return ""


def _ngay(now: datetime) -> str:
    return f"{THU[now.weekday()]}, {now.strftime('%d/%m/%Y')}"


def _am(now: datetime) -> str:
    try:
        from .am_lich import mo_ta_am

        return mo_ta_am(now.date())
    except Exception:
        return ""


def tra_loi(loai: str, now: datetime, memory=None, thoi_tiet: str | None = None, co_thanh_pho: bool = False) -> tuple[str, str]:
    """(câu Bơ nói, cảm xúc). Câu rỗng = không trả lời nhanh được (để AI làm).
    thoi_tiet: dòng thời tiết đã lấy sẵn (thoi_tiet.py), co_thanh_pho: đã đặt thành phố chưa."""
    if loai == "thoi_tiet":
        if thoi_tiet:
            return f"{thoi_tiet} Ra ngoài nhớ để ý nha!", "vui"
        if not co_thanh_pho:
            return ('Bơ chưa biết bạn ở thành phố nào nên chưa xem thời tiết được. Bấm nút "?" → Cài đặt → '
                    'gõ thành phố (ví dụ Da Nang) là Bơ xem được nè!'), "suy_nghi"
        return "Bơ chưa lấy được thời tiết (chắc mạng chập chờn), lát hỏi lại Bơ nha!", "buon"
    if loai == "gio":
        h, m = now.hour, now.minute
        return f"Bây giờ là {h} giờ {m:02d} phút nè ({now.strftime('%H:%M')}).", "vui"
    if loai in ("thu", "ngay"):
        am = _am(now)
        try:
            from .am_lich import ngay_le

            le = ngay_le(now.date())
        except Exception:
            le = []
        return (f"Hôm nay là {_ngay(now)}" + (f", âm lịch {am}" if am else "")
                + (f". Hôm nay còn là {', '.join(le)} nữa đó!" if le else " nha!")), "vui"
    if loai == "am":
        am = _am(now)
        return (f"Hôm nay âm lịch là {am} ({_ngay(now)}) nè!", "vui") if am else ("", "")
    if loai == "tet":
        try:
            from .am_lich import tet_sap_toi

            tet = tet_sap_toi(now.date())
        except Exception:
            tet = None
        if not tet:
            return "", ""
        try:
            from .am_lich import duong_sang_am

            d_am, t_am, _, nhuan = duong_sang_am(now.date())
        except Exception:
            d_am = t_am = 0
            nhuan = True
        if t_am == 1 and not nhuan and 2 <= d_am <= 10:
            return (f"Đang mùng {d_am} Tết mà, vẫn còn không khí Tết nè! Còn {tet['con_ngay']} ngày nữa mới tới Tết năm sau.",
                    "hao_hung")
        n, ngay = tet["con_ngay"], tet["ngay"].strftime("%d/%m/%Y")
        if n == 0:
            return "Hôm nay là mùng 1 Tết rồi đó! Chúc mừng năm mới, năm nay thật nhiều niềm vui nha!", "hao_hung"
        if n == 1:
            return f"Mai là mùng 1 Tết rồi ({ngay})! Tối nay giao thừa đó, háo hức quá đi!", "hao_hung"
        return f"Còn {n} ngày nữa là Tết (mùng 1 Tết rơi vào {THU[tet['ngay'].weekday()]}, {ngay}). Hóng ghê!", "hao_hung"
    if loai == "viec":
        if memory is None:
            return "", ""
        todos = memory.todos(include_done=False)
        if not todos:
            return "Danh sách việc cần làm đang trống trơn nè. Có gì cần nhớ cứ nhắn Bơ ghi lại nha!", "vui"
        ten = [x["viec"] for x in todos]
        ds = "; ".join(ten[:5]) + (f"; và {len(ten) - 5} việc nữa" if len(ten) > 5 else "")
        return f"Bạn còn {len(ten)} việc: {ds}. Xong việc nào thì kể Bơ để Bơ gạch nha!", "binh_thuong"
    if loai == "thoi_quen":
        if memory is None:
            return "", ""
        hs = memory.habits(now.date())
        if not hs:
            return 'Bạn chưa nhờ Bơ theo dõi thói quen nào. Nhắn "theo dõi giúp mình thói quen đọc sách" là được nè!', "vui"
        xong = [h["ten"] for h in hs if h["hom_nay"]]
        chua = [h for h in hs if not h["hom_nay"]]
        if not chua:
            return f"Hôm nay bạn làm đủ hết {len(hs)} thói quen rồi ({', '.join(xong)}). Giỏi quá trời!", "hao_hung"
        ds = "; ".join(h["ten"] + (f" (đang chuỗi {h['chuoi']} ngày)" if h["chuoi"] >= 2 else "") for h in chua)
        dau = f"Hôm nay xong {', '.join(xong)} rồi. " if xong else ""
        return f"{dau}Còn chưa làm: {ds}. Làm xong nhắn Bơ tích cho nha!", "vui"
    return "", ""
