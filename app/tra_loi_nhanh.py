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

# Lời gọi ở đầu và từ đệm ở cuối câu, bỏ đi trước khi so (đã bỏ dấu)
_DAU = r"^(?:(?:bo|be|ban|cau)\s+(?:oi|a)\s+|(?:bo|oi|e|ne|cho\s+(?:minh|to|tui|toi)\s+hoi)\s+)*"
_CUOI = r"(?:\s+(?:vay|the|nhi|nhe|nha|a|ha|ho|ne|day|do|di|khong|ko|k|bo|oi|ban|cau|the nhi|vay ta))*$"

_MAU = {
    "gio": [
        r"(?:bay gio|gio|hien tai|hien gio)?\s*(?:la\s+)?may gio(?:\s+roi)?",
        r"may gio roi",
    ],
    "thu": [
        r"(?:hom nay|nay)\s+(?:la\s+)?thu may",
    ],
    "am": [
        r"(?:hom nay|nay)\s+(?:la\s+)?(?:ngay\s+)?(?:may|bao nhieu)\s+(?:am|am lich)",
        r"(?:hom nay|nay)\s+(?:la\s+)?(?:ngay\s+)?am lich\s+(?:may|bao nhieu|ngay may|ngay bao nhieu)",
        r"am lich\s+(?:hom nay|nay)(?:\s+(?:la\s+)?(?:ngay\s+)?(?:may|bao nhieu))?",
        r"ngay am\s+(?:hom nay|nay)(?:\s+(?:la\s+)?(?:may|bao nhieu))?",
    ],
    "ngay": [
        r"(?:hom nay|nay)\s+(?:la\s+)?ngay\s+(?:may|bao nhieu|gi)(?:\s+(?:roi|thang may))?",
        r"(?:hom nay|nay)\s+(?:la\s+)?mung may",
    ],
    "tet": [
        r"(?:con\s+)?(?:may|bao nhieu)\s+ngay\s+(?:nua\s+)?(?:la\s+|thi\s+|toi\s+|den\s+|moi\s+toi\s+)?tet(?:\s+(?:nua|roi))?",
        r"tet\s+con\s+(?:may|bao nhieu)\s+ngay(?:\s+nua)?",
        r"bao gio\s+(?:thi\s+|moi\s+)?(?:toi\s+|den\s+|la\s+)?tet",
        r"(?:khi nao|bao gio)\s+(?:thi\s+)?tet(?:\s+(?:toi|den|nua))?",
        r"tet\s+(?:la\s+)?(?:ngay nao|ngay may|khi nao|bao gio)",
    ],
    "viec": [
        r"(?:minh|to|tui|toi|em)\s+(?:con\s+)?(?:co\s+)?(?:nhung\s+)?(?:viec\s+)?(?:gi|nao)\s+(?:can|phai|chua)\s+(?:lam|xong)(?:\s+(?:khong|ko|nua|chua))?",
        r"(?:danh sach\s+)?viec can lam(?:\s+(?:cua\s+)?(?:minh|to|tui|toi|em))?(?:\s+(?:co gi|la gi|gom gi|con gi))?",
        r"(?:con\s+)?viec gi\s+(?:can|phai|chua)\s+(?:lam|xong)(?:\s+(?:khong|ko|nua|chua))?",
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


def tra_loi(loai: str, now: datetime, memory=None) -> tuple[str, str]:
    """(câu Bơ nói, cảm xúc). Câu rỗng = không trả lời nhanh được (để AI làm)."""
    if loai == "gio":
        h, m = now.hour, now.minute
        return f"Bây giờ là {h} giờ {m:02d} phút nè ({now.strftime('%H:%M')}).", "vui"
    if loai in ("thu", "ngay"):
        am = _am(now)
        return f"Hôm nay là {_ngay(now)}" + (f", âm lịch {am}" if am else "") + " nha!", "vui"
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
    return "", ""
