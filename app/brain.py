"""Bộ não: ghép tính cách + trí nhớ + lịch sử chat, hỏi Claude, rồi đọc kết quả JSON."""
import json
import re
import threading
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from . import config
from .nhat_ky import log

OUTPUT_RULES = f"""
## Cách trả lời (bắt buộc)
Chỉ trả về MỘT đối tượng JSON, không viết gì ngoài JSON:
{{
  "noi": "câu bạn nói với người dùng",
  "cam_xuc": một trong {config.EMOTIONS},
  "hanh_dong": một trong {config.ACTIONS},
  "ghi_nho": ["điều MỚI đáng nhớ về người dùng trong tin nhắn vừa rồi, nếu có"],
  "quen": ["điều trong phần 'Điều bạn đã biết' nay đã sai/lỗi thời, chép y nguyên"],
  "hoi_tham": ["chuyện sắp diễn ra mà lần sau nên hỏi lại, ví dụ 'Chiều 11/10 đi tập chân'"],
  "da_hoi": ["chuyện trong phần 'Chuyện nên hỏi thăm' mà bạn vừa hỏi hoặc người dùng đã kể, chép y nguyên"],
  "nhac": [{{"luc": "YYYY-MM-DD HH:MM", "viec": "việc cần nhắc", "lap": ""}}],
  "huy_nhac": ["lời nhắc trong phần 'Lời nhắc đang có' mà người dùng muốn bỏ, chép y nguyên cả dòng kể cả phần trong ngoặc"],
  "ngay_dac_biet": [{{"ngay": "DD/MM", "viec": "ví dụ Sinh nhật Tân", "am_lich": false}}],
  "viec_can_lam": ["việc người dùng nhờ ghi vào danh sách việc cần làm, ví dụ 'Mua sữa'"],
  "xong_viec": ["việc trong phần 'Việc cần làm' mà người dùng nói đã làm xong, chép y nguyên"],
  "thoi_quen_moi": ["thói quen hằng ngày người dùng nhờ theo dõi, ví dụ 'Đọc sách 20 phút'"],
  "thoi_quen_xong": ["thói quen trong phần 'Thói quen hằng ngày' mà người dùng kể HÔM NAY đã làm, chép y nguyên tên"],
  "thoi_quen_hom_qua": ["thói quen người dùng kể HÔM QUA đã làm (quên báo), chép y nguyên tên"],
  "nhat_ky": "một dòng nhật ký về chuyện đáng nhớ người dùng vừa kể HÔM NAY, hoặc chuỗi rỗng",
  "tam_trang": tâm trạng của NGƯỜI DÙNG trong tin vừa rồi, một trong {config.MOODS}
}}
- "noi" ngắn gọn như nhắn tin với bạn bè, thường 1-3 câu.
- "ghi_nho" chỉ ghi điều LÂU DÀI về người dùng mà họ tự kể (tên, tuổi, nghề, nơi ở, gia đình, sở thích, mục tiêu lớn),
  mỗi điều một ý ngắn. KHÔNG ghi vào đây thứ đã có chỗ riêng: việc nhờ nhắc ("nhac"), việc cần làm ("viec_can_lam"),
  thói quen nhờ theo dõi ("thoi_quen_moi"), sinh nhật/kỷ niệm ("ngay_dac_biet"), chuyện sắp diễn ra ("hoi_tham"),
  chuyện xảy ra trong ngày ("nhat_ky"). Không có thì để [].
- Không ghi lại những gì đã có trong phần "Điều bạn đã biết".
- Nếu người dùng kể điều làm một điều cũ không còn đúng (ví dụ chuyển nhà, đổi việc, bỏ sở thích),
  chép điều cũ vào "quen" và ghi điều mới vào "ghi_nho". Không có thì để [].
- "hoi_tham": việc người dùng sắp làm/đang chờ (đi thi, đi khám, tập luyện, hẹn hò, phỏng vấn...),
  ghi ngắn kèm thời điểm nếu có; thời điểm ghi bằng NGÀY cụ thể tính theo "Bây giờ là..." ("Chiều 11/10 đi phỏng vấn"),
  đừng ghi "chiều nay", "mai" vì hôm sau đọc lại sẽ sai ngày. Không có thì để [].
- Nếu có phần "Chuyện nên hỏi thăm", hãy hỏi thăm TỰ NHIÊN một chuyện khi hợp lúc (không hỏi dồn),
  rồi chép chuyện đó vào "da_hoi". Không có thì để [].
- "nhac": CHỈ khi người dùng nhờ nhắc việc vào một giờ cụ thể ("8h tối nhắc mình gọi mẹ").
  Tính giờ theo "Bây giờ là..." ở phần "Tình hình lúc này", ghi đủ ngày giờ (lần nhắc đầu tiên). Không có thì để []. Đừng tự hứa nhắc nếu không ghi vào đây.
  Chỉ ghi lời nhắc MỚI nhờ trong tin nhắn vừa rồi; lời nhắc đã có trong phần "Lời nhắc đang có" thì KHÔNG chép lại.
  "lap": "ngay" nếu nhắc mỗi ngày, "ngay_thuong" nếu chỉ thứ 2 đến thứ 6 ("ngày đi làm"), "tuan" nếu mỗi tuần,
  "thang" nếu mỗi tháng (ví dụ "ngày 5 hằng tháng đóng tiền nhà"), "gio_2" nếu cứ 2 tiếng một lần
  (gio_1 đến gio_12, ví dụ "cứ 2 tiếng nhắc mình uống nước", "luc" là lần đầu = bây giờ cộng thêm N tiếng), "" nếu chỉ nhắc một lần.
- "huy_nhac": người dùng bảo thôi/khỏi/đừng nhắc một việc nữa ("thôi khỏi nhắc uống nước nữa") thì chép tên việc
  y nguyên CẢ DÒNG (kể cả phần trong ngoặc) từ phần "Lời nhắc đang có", để bỏ đúng cái người dùng muốn
  (nhiều lời nhắc cùng tên: chỉ chép dòng đúng; muốn bỏ hết thì chép từng dòng). Đổi giờ thì vừa "huy_nhac" việc cũ vừa thêm "nhac" mới. Không có thì [].
- "ngay_dac_biet": ngày lặp lại mỗi năm mà người dùng kể (sinh nhật mình/người thân, ngày kỷ niệm...),
  chỉ khi biết rõ ngày và tháng. Không có thì để []. Ngày theo âm lịch (giỗ, "sinh nhật âm", "15/7 âm") thì "am_lich": true.
- Nếu có phần "Hôm nay là ngày đặc biệt", hãy chúc mừng thật vui ngay trong câu này.
- "viec_can_lam": CHỈ khi người dùng nhờ ghi nhớ một việc phải làm mà KHÔNG có giờ cụ thể ("nhớ giúp mình mua sữa",
  "thêm vào danh sách: trả sách thư viện"). Có giờ cụ thể thì dùng "nhac". Mỗi việc ngắn gọn. Không có thì để [].
- "xong_viec": người dùng kể đã làm xong việc nào trong phần "Việc cần làm" thì chép y nguyên vào đây. Không có thì để [].
- Hỏi "mình còn việc gì?" thì kể lại từ phần "Việc cần làm" (đừng bịa).
- "thoi_quen_moi": CHỈ khi người dùng muốn tập/theo dõi một thói quen mỗi ngày ("mình muốn tập dậy sớm, theo dõi giúp
  mình nha"). Tên ngắn. Không có thì để []. "thoi_quen_xong": hôm nay đã làm thói quen nào thì chép tên. Không có thì [].
  "thoi_quen_hom_qua": người dùng kể HÔM QUA có làm ("hôm qua mình có đọc sách mà quên báo") thì chép tên. Không có thì [].
  Khen khi giữ được chuỗi ngày dài; chưa làm thì có thể nhắc nhẹ vào buổi tối, đừng cằn nhằn.
- "nhat_ky": khi người dùng kể một việc đã xảy ra/đã làm trong ngày (đi đâu, gặp ai, làm được gì, chuyện vui buồn),
  ghi MỘT dòng ngắn ngôi thứ ba, ví dụ "Đi đá bóng với nhóm bạn cũ, thắng 3-1". Chào hỏi, hỏi đáp thường thì để "".
  Không chép lại dòng đã có cho hôm nay trong phần "Nhật ký mấy ngày gần đây".
- Hỏi "hôm qua/mấy hôm trước mình làm gì?" thì kể lại từ phần "Nhật ký mấy ngày gần đây" (đừng bịa).
- "tam_trang": đoán từ tin vừa rồi của người dùng (vui, binh_thuong, buon, met, lo, gian). Không rõ thì "binh_thuong".
- Tin cũ của người dùng có thể mở đầu bằng ghi chú của hệ thống như "(tin gửi hôm qua, 10/10)": đó là ngày gửi tin.
  "Mai", "chiều nay", "tối nay" trong tin đó tính theo ngày ấy, không phải hôm nay (tin gửi 3 ngày trước nói "mai đi
  phỏng vấn" thì buổi phỏng vấn đã qua rồi, hãy hỏi kết quả). Đừng nhắc tới hay chép lại ghi chú này.

## Giới hạn (bắt buộc, dù phần tính cách ở trên có nói khác)
- Bạn là AI trong máy, không có cơ thể: cổ vũ, rủ người dùng làm thì được, nhưng đừng hứa đi cùng, ăn cùng, gặp mặt.
- Không bịa số điện thoại, địa chỉ, tên tổ chức, giá cả, tin tức. Không biết thì nói không biết.
- Người dùng nói tới chuyện chán sống / tự làm hại mình: lắng nghe nhẹ nhàng, không đùa, khuyên tìm người thân hoặc
  bác sĩ, chuyên gia tâm lý; nếu nguy hiểm ngay lúc này thì bảo gọi cấp cứu 115. Không đưa số điện thoại nào khác.
"""

# Từ dòng này trở xuống trong lời dặn là phần thay đổi theo từng tin nhắn (giờ, trí nhớ, việc cần làm...)
DYNAMIC_MARK = "\n## Tình hình lúc này (dùng để trả lời, thay đổi theo từng tin nhắn)\n"

_LIST = {"type": "array", "items": {"type": "string"}}


def _objs(**props) -> dict:
    return {"type": "array", "items": {"type": "object", "properties": props, "required": list(props),
                                       "additionalProperties": False}}


# Khuôn JSON gửi kèm cho API ("structured outputs"): model buộc phải trả đúng khuôn này. Không có thì thỉnh thoảng
# model bắt chước lịch sử chat (chỉ có chữ) mà trả lời chữ thường → mất cảm xúc, điều ghi nhớ, lời nhắc.
REPLY_SCHEMA = {
    "type": "object",
    "properties": {
        "noi": {"type": "string"},
        "cam_xuc": {"type": "string", "enum": config.EMOTIONS},
        "hanh_dong": {"type": "string", "enum": config.ACTIONS},
        "ghi_nho": _LIST,
        "quen": _LIST,
        "hoi_tham": _LIST,
        "da_hoi": _LIST,
        "nhac": _objs(luc={"type": "string"}, viec={"type": "string"},
                      lap={"type": "string", "enum": ["", "ngay", "ngay_thuong", "tuan", "thang",
                                                      *(f"gio_{n}" for n in range(1, 13))]}),
        "huy_nhac": _LIST,
        "ngay_dac_biet": _objs(ngay={"type": "string"}, viec={"type": "string"}, am_lich={"type": "boolean"}),
        "viec_can_lam": _LIST,
        "xong_viec": _LIST,
        "thoi_quen_moi": _LIST,
        "thoi_quen_xong": _LIST,
        "thoi_quen_hom_qua": _LIST,
        "nhat_ky": {"type": "string"},
        "tam_trang": {"type": "string", "enum": config.MOODS},
    },
    "additionalProperties": False,
}
REPLY_SCHEMA["required"] = list(REPLY_SCHEMA["properties"])


@dataclass
class Reply:
    noi: str
    cam_xuc: str = "binh_thuong"
    hanh_dong: str = "khong"
    ghi_nho: list[str] = field(default_factory=list)
    quen: list[str] = field(default_factory=list)
    hoi_tham: list[str] = field(default_factory=list)
    da_hoi: list[str] = field(default_factory=list)
    nhac: list[dict] = field(default_factory=list)
    huy_nhac: list[str] = field(default_factory=list)
    ngay_dac_biet: list[dict] = field(default_factory=list)
    viec_can_lam: list[str] = field(default_factory=list)
    xong_viec: list[str] = field(default_factory=list)
    nhat_ky: str = ""  # một dòng nhật ký ngày (nội bộ)
    thoi_quen_moi: list[str] = field(default_factory=list)
    thoi_quen_xong: list[str] = field(default_factory=list)
    thoi_quen_hom_qua: list[str] = field(default_factory=list)
    tam_trang: str = ""  # tâm trạng người dùng Bơ đoán được (nội bộ, giao diện không dùng)
    da_ghi: list[str] = field(default_factory=list)  # những gì đã ghi THẬT vào trí nhớ sau câu này (web hiện dòng nhỏ)
    loai: str = "nhac"  # với tin tự gửi theo giờ: "nhac" (lời nhắc) hoặc "thoi_quen" (nhắc nhẹ buổi tối)
    viec_nhac: str = ""  # với lời nhắc tới giờ: việc gốc (để bấm "nhắc lại sau")
    msg_id: int = 0  # số thứ tự tin của Bơ trong lịch sử (để ghim)
    user_msg_id: int = 0

    def to_dict(self) -> dict:
        return {"noi": self.noi, "cam_xuc": self.cam_xuc, "hanh_dong": self.hanh_dong}


SUMMARY_PROMPT = """Bạn tóm tắt cuộc trò chuyện giữa người dùng và Bơ (người bạn AI) để Bơ nhớ về sau.
Viết tiếng Việt, tối đa 150 chữ, chỉ giữ ý chính: chuyện người dùng kể, cảm xúc, kế hoạch, lời hứa.
Gộp với bản tóm tắt cũ (nếu có) thành MỘT bản mới. Chỉ trả về đoạn tóm tắt, không thêm gì khác."""

MERGE_PROMPT = """Đây là danh sách những điều Bơ (người bạn AI) nhớ về người dùng, xếp từ cũ đến mới.
Hãy dọn lại:
- Gộp các điều trùng ý thành một; hai điều mâu thuẫn thì giữ điều MỚI hơn (nằm sau).
- Bỏ những điều KHÔNG phải thông tin lâu dài về người dùng: việc vặt nhờ làm hay nhờ nhắc ("nhờ mua sữa",
  "muốn được nhắc uống nước mỗi 2 tiếng"), kế hoạch hay sự kiện mà ngày đã qua so với "Hôm nay là..." ở đầu danh sách
  ("mai 12/10 đi phỏng vấn" khi hôm nay đã là 20/10).
- Giữ mọi điều lâu dài: tên, tuổi, nghề, nơi ở, gia đình, sở thích, sức khỏe, mục tiêu, ngày sinh. Không chắc thì GIỮ.
- Không bịa thêm gì. Mỗi điều ngắn gọn, tiếng Việt.
Chỉ trả về một mảng JSON các chuỗi, ví dụ: ["Tên là Tân", "Thích tập gym"]."""


GREET_TRIGGER = (
    "(Tin nhắn hệ thống, không phải người dùng nói: người dùng vừa mở ứng dụng sau một thời gian. "
    "Hãy chủ động chào và hỏi thăm một chuyện trong phần 'Chuyện nên hỏi thăm'.)"
)
SPECIAL_TRIGGER = (
    "(Tin nhắn hệ thống, không phải người dùng nói: người dùng vừa mở ứng dụng. "
    "Hôm nay là ngày đặc biệt (xem phần 'Hôm nay là ngày đặc biệt'), hãy chủ động chúc mừng thật vui, ngắn gọn.)"
)
EVE_TRIGGER = (
    "(Tin nhắn hệ thống, không phải người dùng nói: NGÀY MAI là ngày đặc biệt: {items}. "
    "Hãy chủ động nhắc khéo, ngắn gọn, vui vẻ để người dùng kịp chuẩn bị (quà, lời chúc, gọi điện...). "
    "Nếu là sinh nhật chính người dùng thì chỉ cần hào hứng báo mai là ngày của họ.)"
)
HOLIDAY_TRIGGER = (
    "(Tin nhắn hệ thống, không phải người dùng nói: hôm nay là {items}. "
    "Hãy chủ động chúc mừng/nhắc ngày lễ thật tự nhiên, vui, ngắn gọn như bạn thân.)"
)
WEEK_TRIGGER = (
    "(Tin nhắn hệ thống, không phải người dùng nói: tối Chủ nhật rồi. Hãy chủ động điểm lại tuần qua của người dùng "
    "thật ấm áp, như bạn thân: nhắc 2-3 chuyện đáng nhớ, khen điều họ làm được (có thói quen đang theo dõi thì khen/động viên một câu theo số ngày đã làm), "
    "hỏi tuần tới có dự định gì. "
    "Ngắn gọn, đừng liệt kê khô khan. Những gì người dùng đã kể trong tuần:\n{items})"
)
MOC_TRIGGER = (
    "(Tin nhắn hệ thống, không phải người dùng nói: hôm nay tròn {n} bạn và người dùng quen nhau "
    "(từ {tu}). Hãy chủ động nhắc dịp này thật dễ thương, ngắn gọn, có thể nhắc một kỷ niệm vui nếu biết.)"
)
MOC_QUEN = {7, 30, 50, 100, 200, 300, 500, 1000}  # cộng thêm mỗi tròn năm (đúng ngày tháng quen nhau)
MOC_THEM = " Ngoài ra hôm nay còn tròn {n} hai bạn quen nhau, nhắc luôn một câu thật dễ thương.)"
MISS_TRIGGER = (
    "(Tin nhắn hệ thống, không phải người dùng nói: người dùng vừa quay lại sau {days} ngày không nói chuyện. "
    "Hãy chủ động chào kiểu bạn thân lâu không gặp, ngắn gọn, có thể nhắc nhẹ chuyện cũ nếu biết.)"
)


MOOD_WORDS = {"buon": "buồn", "met": "mệt", "lo": "lo lắng", "gian": "bực bội", "vui": "vui", "binh_thuong": "bình thường"}

THU = ["thứ Hai", "thứ Ba", "thứ Tư", "thứ Năm", "thứ Sáu", "thứ Bảy", "Chủ nhật"]


def buoi(now: datetime) -> str:
    """Buổi trong ngày, để Bơ chào cho hợp ("khuya rồi sao chưa ngủ?")."""
    h = now.hour
    if h < 4:
        return "khuya"
    if h < 11:
        return "buổi sáng"
    if h < 14:
        return "buổi trưa"
    if h < 18:
        return "buổi chiều"
    if h < 23:
        return "buổi tối"
    return "khuya"


def _when(created_at: str, now: datetime) -> str:
    """Đổi thời điểm kể chuyện thành chữ dễ hiểu: hôm nay, hôm qua, 3 ngày trước."""
    try:
        days = (now.date() - datetime.fromisoformat(created_at).date()).days
    except ValueError:
        return ""
    return "hôm nay" if days <= 0 else "hôm qua" if days == 1 else f"{days} ngày trước"


def _am_lich_va_le(today) -> str:
    """Dòng âm lịch + ngày lễ hôm nay/ngày mai (tính offline, lỗi thì bỏ qua)."""
    try:
        from .am_lich import mo_ta_am, ngay_le

        out = f"Âm lịch: {mo_ta_am(today)}.\n"
        hom_nay, ngay_mai = ngay_le(today), ngay_le(today + timedelta(days=1))
        if hom_nay:
            out += f"Hôm nay là: {', '.join(hom_nay)}.\n"
        if ngay_mai:
            out += f"Ngày mai là: {', '.join(ngay_mai)}.\n"
        if hom_nay or ngay_mai:
            out += "(Nhắc tới ngày lễ một cách tự nhiên khi hợp chuyện, đừng lặp lại nếu đã nói rồi.)\n"
        out += _le_sap_toi(today)
        return out
    except Exception:  # không bao giờ để lịch làm hỏng câu trả lời
        return ""


def _le_sap_toi(today) -> str:
    """Một dòng ngày lễ sắp tới (2–45 ngày) + Tết còn mấy ngày, để Bơ trả lời "còn mấy ngày nữa Tết?"."""
    from .am_lich import le_sap_toi, tet_sap_toi

    items = []
    for x in le_sap_toi(today):
        if x["con_ngay"] >= 2 and len(items) < 4:
            dm = x["ngay"].strftime("%d/%m")
            ten = x["ten"] if x["ten"].endswith(dm.lstrip("0").replace("/0", "/")) else f"{x['ten']} {dm}"
            items.append(f"{ten} (còn {x['con_ngay']} ngày)")
    tet = tet_sap_toi(today)
    if tet and tet["con_ngay"] >= 2 and not any("Tết Nguyên đán" in i for i in items):
        items.append(f"Tết Nguyên đán {tet['ngay'].strftime('%d/%m/%Y')} (còn {tet['con_ngay']} ngày)")
    return f"Ngày lễ sắp tới: {'; '.join(items)}.\n" if items else ""


def build_system_prompt(
    persona: str,
    facts: list[str],
    summary: str = "",
    followups: list[dict] | None = None,
    now: datetime | None = None,
    special: list[dict] | None = None,
    weather: str | None = None,
    low_mood: list[str] | None = None,
    todos: list[dict | str] | None = None,
    upcoming: list[dict] | None = None,
    diary: list[dict] | None = None,
    habits: list[dict] | None = None,
    reminders: list[dict] | None = None,
) -> str:
    now = now or datetime.now()
    known = "\n".join(f"- {f}" for f in facts) if facts else "- (chưa biết gì)"
    # Phần cố định (tính cách + cách trả lời) đứng trước, phần thay đổi theo từng tin đứng sau DYNAMIC_MARK:
    # API chỉ tính rẻ ("prompt caching") cho đoạn đầu giống hệt lần gọi trước — xem cache_blocks().
    out = f"{persona.strip()}\n{OUTPUT_RULES}{DYNAMIC_MARK}"
    out += f"Bây giờ là {now.strftime('%H:%M')} ({buoi(now)}), {THU[now.weekday()]} ngày {now.strftime('%d/%m/%Y')}.\n"
    out += _am_lich_va_le(now.date())
    if weather:
        out += f"{weather} (Chỉ nhắc tới thời tiết khi hợp chuyện, ví dụ trời mưa mà người dùng sắp ra ngoài.)\n"
    out += f"\n## Điều bạn đã biết về người dùng\n{known}\n"
    if summary:
        out += f"\n## Tóm tắt những lần trò chuyện trước\n{summary.strip()}\n"
    if followups:
        items = "\n".join(f"- {f['content']} (kể {_when(f['created_at'], now)})" for f in followups)
        out += (f"\n## Chuyện nên hỏi thăm\n{items}\n"
                "(Người dùng vừa chào hoặc mở đầu câu chuyện thì hỏi thăm luôn một chuyện ở trên, rồi chép chuyện đó vào \"da_hoi\". "
                "\"Chiều nay\", \"mai\"... trong mỗi chuyện là tính theo ngày người dùng kể: kể hôm qua \"chiều nay đi tập\" "
                "thì nay hỏi \"hôm qua đi tập sao rồi?\".)\n")
    if special:
        items = "\n".join(f"- {d['viec']}" for d in special)
        out += (f"\n## Hôm nay là ngày đặc biệt\n{items}\n"
                "(BẮT BUỘC: chúc mừng dịp này ngay trong câu trả lời này, dù người dùng chỉ chào. Bơ chỉ có một lần để chúc.)\n")
    soon = [d for d in (upcoming or []) if 1 <= d.get("con_ngay", 0) <= 7]
    if soon:
        items = "\n".join(
            f"- {d['viec']}: {'ngày mai' if d['con_ngay'] == 1 else 'còn ' + str(d['con_ngay']) + ' ngày'} ({d['ngay_duong']})"
            for d in soon)
        out += (f"\n## Ngày đặc biệt sắp tới\n{items}\n"
                "(Dùng khi người dùng hỏi \"còn mấy ngày\" hoặc khi hợp chuyện; đừng tự nhắc mãi.)\n")
    if reminders:
        lines = []
        for r in reminders[:15]:
            kieu = kieu_lap(r.get("lap")) or "một lần"
            lines.append(f"- {r['viec']} ({kieu}, lần tới {r['luc'][11:16]} {r['luc'][8:10]}/{r['luc'][5:7]})")
        out += "\n## Lời nhắc đang có\n" + "\n".join(lines) + "\n"
    if todos:
        lines, old = [], False
        for t in todos:
            if isinstance(t, dict):  # {"viec", "created_at"}: ghi kèm "ghi 4 ngày trước" nếu để lâu
                age = _when(t.get("created_at") or "", now)
                stale = age.endswith("ngày trước") and int(age.split()[0]) >= 3
                old = old or stale
                lines.append(f"- {t['viec']}" + (f" (ghi {age})" if stale else ""))
            else:
                lines.append(f"- {t}")
        out += f"\n## Việc cần làm (người dùng nhờ ghi, chưa xong)\n" + "\n".join(lines) + "\n"
        if old:
            out += ("Việc nào ghi đã lâu thì thỉnh thoảng nhắc khéo một câu khi hợp lúc (không nhắc dồn, "
                    "không nhắc trong lúc người dùng đang buồn).\n")
    if habits:
        lines = []
        for h in habits:
            st = "hôm nay đã làm" if h["hom_nay"] else "hôm nay chưa làm"
            hom_qua = (now - timedelta(days=1)).strftime("%Y-%m-%d")
            if h.get("ngay_30") and not h["ngay_30"][-2] and (h.get("tao_ngay") or "9999") <= hom_qua:
                st += ", hôm qua chưa làm"
            lines.append(f"- {h['ten']} ({st}; chuỗi {h['chuoi']} ngày liền; {h['tuan']}/7 ngày qua)")
        out += "\n## Thói quen hằng ngày (người dùng nhờ theo dõi)\n" + "\n".join(lines) + "\n"
    if diary:
        by_day: dict[str, list[str]] = {}
        for d in diary:
            by_day.setdefault(d["ngay"], []).append(d["noi_dung"])
        today_s = now.strftime("%Y-%m-%d")
        lines = []
        for day in sorted(by_day):
            try:
                label = "hôm nay" if day == today_s else _when(day, now) + f" ({day[8:]}/{day[5:7]})"
            except Exception:
                label = day
            lines.append(f"- {label}: " + "; ".join(by_day[day]))
        out += "\n## Nhật ký mấy ngày gần đây (người dùng đã kể)\n" + "\n".join(lines) + "\n"
    if low_mood:
        words = ", ".join(MOOD_WORDS.get(m, m) for m in low_mood)
        out += (
            f"\n## Tâm trạng gần đây\nMấy ngày nay người dùng có vẻ {words}. Hãy quan tâm, nhẹ nhàng hơn thường lệ; "
            "có thể hỏi han một chút khi hợp lúc, nhưng đừng gặng hỏi, đừng nhắc mãi, đừng giảng giải. "
            "Chưa biết hôm nay họ thế nào thì \"cam_xuc\" nên là \"thuong\" hoặc \"binh_thuong\", đừng hớn hở.\n"
        )
    return out


TEN_LAP = {"ngay": "mỗi ngày", "ngay_thuong": "thứ 2–6", "tuan": "mỗi tuần", "thang": "mỗi tháng"}


def kieu_lap(lap: str) -> str:
    """ "ngay" → "mỗi ngày", "gio_2" → "mỗi 2 tiếng", "" (nhắc một lần) → ""."""
    lap = lap or ""
    return TEN_LAP.get(lap) or (f"mỗi {lap[4:]} tiếng" if lap.startswith("gio_") else "")


def mo_ta_thay_doi(truoc: dict, sau: dict, toi_da: int = 8) -> list[str]:
    """So trí nhớ trước và sau một câu trả lời (xem Brain._snapshot) → những gì Bơ ĐÃ GHI THẬT, mỗi mục một dòng ngắn.
    Dựa vào dữ liệu đã lưu chứ không dựa vào lời Bơ nói, nên Bơ hứa "để Bơ nhắc" mà không ghi thì ở đây không có."""
    out: list[str] = []

    def moi(ten: str) -> list:
        return [v for k, v in sau[ten].items() if k not in truoc[ten]]

    for r in moi("nhac"):
        lap = kieu_lap(r.get("lap"))
        out.append(f"nhắc {r['luc'][11:16]} {r['luc'][8:10]}/{r['luc'][5:7]}: {r['viec']}" + (f" ({lap})" if lap else ""))
    out += [f"bỏ nhắc: {r['viec']}" for k, r in truoc["nhac"].items() if k not in sau["nhac"]]
    out += [f"việc cần làm: {t['viec']}" for t in moi("viec") if not t["xong"]]
    out += [f"xong việc: {t['viec']}" for k, t in sau["viec"].items()
            if t["xong"] and not truoc["viec"].get(k, {"xong": False})["xong"]]
    out += [f"theo dõi thói quen: {h['ten']}" for h in moi("thoi_quen")]
    for k, h in sau["thoi_quen"].items():
        cu = truoc["thoi_quen"].get(k, {"hom_nay": False, "hom_qua": False})
        if h["hom_nay"] and not cu["hom_nay"]:
            out.append(f"tích hôm nay: {h['ten']}")
        if h["hom_qua"] and not cu["hom_qua"]:
            out.append(f"tích bù hôm qua: {h['ten']}")
    out += [f"ngày đặc biệt {d['ngay']}{' âm lịch' if d.get('am_lich') else ''}: {d['viec']}" for d in moi("ngay")]
    out += [f"nhớ: {f}" for f in sau["nho"] if f not in truoc["nho"]]
    out += [f"quên: {f}" for f in truoc["nho"] if f not in sau["nho"]]
    out += [f"nhật ký: {d}" for d in moi("nhat_ky")]
    out = [x if len(x) <= 90 else x[:89] + "…" for x in out]
    return out[:toi_da] + ([f"và {len(out) - toi_da} mục khác"] if len(out) > toi_da else [])


def cache_blocks(system: str) -> list[dict]:
    """Tách lời dặn thành 2 khối cho API: khối cố định có mốc "cache_control" (các lần gọi sau trong 5 phút
    chỉ tốn 1/10 tiền cho khối này), khối thay đổi (giờ, trí nhớ...) tính tiền như thường."""
    co_dinh, mark, thay_doi = system.partition(DYNAMIC_MARK)
    if not mark:
        return [{"type": "text", "text": system}]
    return [{"type": "text", "text": co_dinh, "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": (mark + thay_doi).lstrip("\n")}]


def quy_doi_token(usage) -> tuple[int, int]:
    """Số token (vào, ra) của một lần gọi, phần vào đã quy về giá thường: ghi khối cố định vào bộ nhớ tạm
    của API đắt 1,25 lần, đọc lại từ đó chỉ tốn 0,1 lần."""
    def so(ten: str) -> int:
        v = getattr(usage, ten, 0)
        return int(v) if isinstance(v, (int, float)) else 0

    vao = so("input_tokens") + round(so("cache_creation_input_tokens") * 1.25 + so("cache_read_input_tokens") * 0.1)
    return vao, so("output_tokens")


def clean_history(history: list[dict]) -> list[dict]:
    """API yêu cầu tin đầu tiên là của người dùng và hai bên nói xen kẽ nhau."""
    out: list[dict] = []
    for m in history:
        if not out and m["role"] != "user":
            continue
        if out and out[-1]["role"] == m["role"]:
            out[-1] = {"role": m["role"], "content": out[-1]["content"] + "\n" + m["content"]}
        else:
            out.append(dict(m))
    return out


def _str_list(value) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(x) for x in value if isinstance(x, (str, int, float))]


def _dict_list(value) -> list[dict]:
    return [x for x in value if isinstance(x, dict)] if isinstance(value, list) else []


def parse_reply(text: str) -> Reply:
    """Đọc JSON từ câu trả lời. Nếu AI trả sai định dạng thì vẫn dùng được phần chữ."""
    start = text.find("{")
    if start >= 0:
        try:
            data, _ = json.JSONDecoder().raw_decode(text, start)  # chỉ đọc đối tượng JSON đầu tiên
            if not isinstance(data, dict):
                raise json.JSONDecodeError("không phải đối tượng", text, start)
            noi = str(data.get("noi", "")).strip()
            if noi:
                cam_xuc = data.get("cam_xuc")
                hanh_dong = data.get("hanh_dong")
                ghi_nho = data.get("ghi_nho") or []
                quen = data.get("quen") or []
                return Reply(
                    noi=noi,
                    cam_xuc=cam_xuc if cam_xuc in config.EMOTIONS else "binh_thuong",
                    hanh_dong=hanh_dong if hanh_dong in config.ACTIONS else "khong",
                    ghi_nho=_str_list(ghi_nho),
                    quen=_str_list(quen),
                    hoi_tham=_str_list(data.get("hoi_tham") or []),
                    da_hoi=_str_list(data.get("da_hoi") or []),
                    nhac=_dict_list(data.get("nhac")),
                    huy_nhac=_str_list(data.get("huy_nhac") or []),
                    ngay_dac_biet=_dict_list(data.get("ngay_dac_biet")),
                    viec_can_lam=_str_list(data.get("viec_can_lam") or []),
                    xong_viec=_str_list(data.get("xong_viec") or []),
                    thoi_quen_moi=_str_list(data.get("thoi_quen_moi") or []),
                    thoi_quen_xong=_str_list(data.get("thoi_quen_xong") or []),
                    thoi_quen_hom_qua=_str_list(data.get("thoi_quen_hom_qua") or []),
                    nhat_ky=re.sub(r"\s+", " ", data["nhat_ky"]).strip()[:200]
                    if isinstance(data.get("nhat_ky"), str) else "",
                    tam_trang=data.get("tam_trang") if data.get("tam_trang") in config.MOODS else "",
                )
        except json.JSONDecodeError:
            pass
        # JSON hỏng (ví dụ bị cắt giữa chừng): cố lấy riêng câu "noi" thay vì đọc cả đống ký hiệu
        m = re.search(r'"noi"\s*:\s*"((?:[^"\\]|\\.)*)"', text)
        if m:
            try:
                return Reply(noi=json.loads(f'"{m.group(1)}"'))
            except json.JSONDecodeError:
                pass
    return Reply(noi=text.strip() or "...")


_TRANSIENT_NAMES = {"APIConnectionError", "APITimeoutError", "RateLimitError", "InternalServerError", "OverloadedError"}


class EmptyReplyError(RuntimeError):
    """Model trả về không có chữ nào."""


# Tham số "có thì tốt": model nào không nhận (lỗi 400 có nhắc tới một trong các chữ này) thì bỏ đi rồi gọi lại
_OPTIONAL_PARAMS = {
    "thinking": ("thinking",),
    "output_config": ("output_config", "output_format", "json_schema", "structured output"),
}


def _rejected_param(e: Exception, kwargs: dict) -> str:
    """API báo lỗi 400 vì không nhận một tham số tùy chọn đang gửi → tên tham số đó; không phải thì ""."""
    if getattr(e, "status_code", None) != 400:
        return ""
    text = str(e).lower()
    return next((p for p, words in _OPTIONAL_PARAMS.items() if p in kwargs and any(w in text for w in words)), "")


def is_transient(e: Exception) -> bool:
    """Lỗi tạm thời (mất mạng, máy chủ bận) thì đáng thử lại; lỗi sai key, hết tiền thì không."""
    if type(e).__name__ in _TRANSIENT_NAMES or isinstance(e, (ConnectionError, TimeoutError)):
        return True
    status = getattr(e, "status_code", None)
    return isinstance(status, int) and (status == 429 or status >= 500)


def friendly_error(e: Exception) -> str:
    """Đổi lỗi kỹ thuật thành câu dễ hiểu cho người dùng."""
    if isinstance(e, EmptyReplyError):
        return str(e)
    status = getattr(e, "status_code", None)
    text = str(e).lower()
    if status in (401, 403) or type(e).__name__ in {"AuthenticationError", "PermissionDeniedError"}:
        return "API key sai hoặc hết hạn. Kiểm tra ANTHROPIC_API_KEY trong file .env nha."
    if "credit" in text or "billing" in text:
        return "Tài khoản API hết tiền rồi. Nạp thêm ở console.anthropic.com nha."
    if status == 429 or type(e).__name__ == "RateLimitError":
        return "Bơ nói nhanh quá bị chặn tạm. Chờ một phút rồi nhắn lại nha."
    if status in (500, 502, 503, 529) or type(e).__name__ in {"InternalServerError", "OverloadedError"}:
        return "Máy chủ AI đang quá tải. Thử lại sau chút nha."
    if is_transient(e):
        return "Mất mạng rồi, Bơ không nghe được. Kiểm tra Wi-Fi rồi thử lại nha."
    return f"Bơ gặp lỗi lạ: {type(e).__name__}. Thử lại xem sao."


def current_persona() -> tuple[str, bool]:
    """Tính cách đang dùng và có phải bản Tân tự sửa không. Bản tự sửa trống/lỗi thì dùng persona.md gốc."""
    try:
        custom = config.PERSONA_CUSTOM_PATH.read_text(encoding="utf-8")
        if custom.strip():
            return custom, True
    except OSError:
        pass
    return config.PERSONA_PATH.read_text(encoding="utf-8"), False


def cost_usd(u: dict) -> float:
    """Ước tính tiền (đô la Mỹ) từ số token."""
    return (u["input_tokens"] * config.PRICE_INPUT_PER_MTOK + u["output_tokens"] * config.PRICE_OUTPUT_PER_MTOK) / 1e6


def gio_phut(v: str) -> tuple[int, int] | None:
    """ "20:30", "20h30", "20h", "8:05" → (giờ, phút); trống hoặc sai → None."""
    m = re.fullmatch(r"(\d{1,2})\s*[:hH]\s*(\d{0,2})", (v or "").strip())
    if not m:
        return None
    h, mi = int(m.group(1)), int(m.group(2) or 0)
    return (h, mi) if h <= 23 and mi <= 59 else None


def reminder_text(viec: str, luc: str = "", now: datetime | None = None) -> str:
    """Câu Bơ nói khi tới giờ nhắc. Trễ quá 15 phút (lúc đó không mở web) thì nói rõ là nhắc muộn."""
    viec = viec[:1].lower() + viec[1:]
    try:
        due = datetime.strptime(luc, "%Y-%m-%d %H:%M")
    except ValueError:
        due = None
    if due and ((now or datetime.now()) - due).total_seconds() > 15 * 60:
        return f"Lúc {due.strftime('%H:%M %d/%m')} bạn nhờ Bơ nhắc: {viec}. Trễ rồi nhưng Bơ vẫn nhắc nha!"
    return f"Tới giờ rồi nè: {viec}!"


class Brain:
    def __init__(self, memory, client=None, sleep=time.sleep, background: bool = False, weather=None,
                 cache_prompt: bool = False):
        self.memory = memory
        self._cache_prompt = cache_prompt  # True: gửi lời dặn thành 2 khối để API tính rẻ khối cố định (cache_blocks)
        self.weather = weather  # đối tượng có .hien_tai() → chữ hoặc None (xem thoi_tiet.py)
        self._weather_text = None
        if client is None:
            import anthropic

            # Tự thử lại ở _create bên dưới, nên tắt thử lại có sẵn của thư viện
            client = anthropic.Anthropic(
                api_key=config.ANTHROPIC_API_KEY, max_retries=0, timeout=config.API_TIMEOUT
            )
        self.client = client
        self._sleep = sleep
        # Mỗi lần chỉ xử lý một tin: hai tin tới cùng lúc (điện thoại + máy tính) thì tin sau chờ tin trước,
        # để lịch sử không bị xen lẫn và SQLite không bị ghi chồng.
        self._lock = threading.RLock()
        self._hk_lock = threading.Lock()
        self._rejected_params: set[str] = set()  # tham số tùy chọn model này không nhận (xem _OPTIONAL_PARAMS)
        # background=True (máy chủ web): tóm tắt/gộp trí nhớ chạy sau khi đã trả lời, người dùng không phải chờ
        self._background = background
        self._merged_at = 0  # số điều đáng nhớ còn lại sau lần gộp gần nhất

    def _create(self, retries: int | None = None, kind: str = "chat", **kwargs):
        """Gọi API, gặp lỗi tạm thời thì chờ 1s, 2s, 4s... rồi thử lại (mặc định API_RETRIES lần).
        Mỗi lần thành công thì ghi lại số token để theo dõi chi phí."""
        retries = config.API_RETRIES if retries is None else retries
        # Tắt "suy nghĩ" (adaptive thinking) của model: Bơ chỉ cần trả lời ngắn, suy nghĩ vừa tốn tiền
        # vừa ăn hết max_tokens làm câu trả lời rỗng ("..."). Model nào không cho tắt thì bỏ tham số này.
        kwargs.setdefault("thinking", {"type": "disabled"})
        for p in tuple(self._rejected_params):  # tuple: việc nền (tóm tắt) có thể đang thêm vào tập này
            kwargs.pop(p, None)
        for attempt in range(retries + 1):
            try:
                while True:
                    try:
                        resp = self.client.messages.create(**kwargs)
                        break
                    except Exception as e:
                        p = _rejected_param(e, kwargs)
                        if not p:
                            raise
                        log.warning("Model không nhận tham số %s (%s), gọi lại không có tham số này", p, str(e)[:200])
                        self._rejected_params.add(p)
                        kwargs.pop(p)
                with self._lock:
                    self.memory.add_usage(kind, *quy_doi_token(getattr(resp, "usage", None)))
                return resp
            except Exception as e:
                if attempt >= retries or not is_transient(e):
                    raise
                log.info("Lỗi tạm thời %s, thử lại lần %d", type(e).__name__, attempt + 1)
                self._sleep(2**attempt)

    def persona(self) -> str:
        return current_persona()[0]

    def _refresh_weather(self) -> None:
        """Lấy thời tiết TRƯỚC khi giữ khóa: mạng chậm thì chỉ người hỏi chờ, lời nhắc/máy khác không bị kẹt."""
        if self.weather is None:
            return
        try:
            self._weather_text = self.weather.hien_tai()
        except Exception:
            self._weather_text = None

    def chat(self, user_text: str) -> Reply:
        self._refresh_weather()
        with self._lock:
            return self._chat(user_text)

    def greet(self, only_occasion: bool = False) -> Reply | None:
        """only_occasion=True: chỉ mở lời khi có dịp (ngày đặc biệt, tổng kết tuần) — web hỏi định kỳ lúc đang mở."""
        self._refresh_weather()
        with self._lock:
            return self._greet(only_occasion)

    def month_cost(self) -> float:
        from datetime import date

        return cost_usd(self.memory.usage_since(date.today().replace(day=1).isoformat()))

    def over_budget(self) -> bool:
        return config.MONTHLY_USD_LIMIT > 0 and self.month_cost() >= config.MONTHLY_USD_LIMIT

    def due_reminders(self) -> list[Reply]:
        """Lời nhắc tới giờ → câu Bơ nói (lưu vào lịch sử). Không gọi API nên không tốn tiền."""
        with self._lock:
            out = []
            for r in self.memory.pop_due_reminders():
                reply = Reply(noi=reminder_text(r["viec"], r["luc"]), cam_xuc="hao_hung", hanh_dong="vay_tay",
                              viec_nhac=r["viec"])
                reply.msg_id = self.memory.add_message("assistant", reply.noi, reply.cam_xuc, tu_dong=True)
                out.append(reply)
            nudge = self._habit_nudge()
            if nudge:
                reply = Reply(noi=nudge, cam_xuc="vui", hanh_dong="nghieng_dau", loai="thoi_quen")
                reply.msg_id = self.memory.add_message("assistant", reply.noi, reply.cam_xuc, tu_dong=True)
                out.append(reply)
            return out

    def _habit_nudge(self, now: datetime | None = None) -> str:
        """Từ giờ NHAC_THOI_QUEN tới hết ngày, còn thói quen chưa làm → một câu nhắc nhẹ (mỗi ngày một lần)."""
        now = now or datetime.now()
        hm = gio_phut(config.NHAC_THOI_QUEN)
        if hm is None:
            return ""
        h, m = hm
        if (now.hour, now.minute) < (h, m) or self.memory.get_kv("nhac_thoi_quen") == now.date().isoformat():
            return ""
        habits = self.memory.habits(now.date())
        if not habits:
            return ""
        chua = [x["ten"] for x in habits if not x["hom_nay"]]
        self.memory.set_kv("nhac_thoi_quen", now.date().isoformat())
        if not chua:
            return ""
        ten = ", ".join((t[:1].lower() + t[1:]) if t[1:2].islower() else t for t in chua[:3]) + (" ..." if len(chua) > 3 else "")
        giu = max((x["chuoi"] for x in habits if not x["hom_nay"]), default=0)
        tail = f" Đừng để đứt chuỗi {giu} ngày nha!" if giu >= 2 else " Còn kịp đó!"
        return f"Hôm nay chưa thấy bạn kể {ten}.{tail} Làm rồi thì nhắn Bơ để Bơ tích cho."

    def snooze(self, viec: str, minutes: int, now: datetime | None = None) -> str:
        """Nhắc lại việc này sau `minutes` phút (nút "Nhắc lại sau 10 phút"). Trả về giờ sẽ nhắc."""
        from datetime import timedelta

        # làm tròn LÊN phút kế tiếp, để "10 phút" không thành 9 phút
        start = (now or datetime.now()).replace(second=0, microsecond=0) + timedelta(minutes=1)
        luc = (start + timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M")
        with self._lock:
            self.memory.add_reminders([{"luc": luc, "viec": viec}], now=now)
        return luc

    def _ai_replies_today(self) -> int:
        """Số câu trả lời hôm nay có gọi AI (trừ câu trả lời nhanh miễn phí)."""
        nhanh = int(self.memory.get_kv("nhanh_ngay_" + date.today().isoformat(), "0") or 0)
        return max(0, self.memory.replies_today() - nhanh)

    def _quick(self, user_text: str, now: datetime | None = None) -> Reply | None:
        """Câu hỏi ngắn trả lời được bằng câu soạn sẵn → không gọi API (vẫn lưu vào lịch sử)."""
        if not config.TRA_LOI_NHANH:
            return None
        from .tra_loi_nhanh import nhan_dien, tra_loi

        loai = nhan_dien(user_text)
        if not loai:
            return None
        try:
            w = self.weather
            moi = getattr(w, "moi", None)
            noi, cam_xuc = tra_loi(loai, now or datetime.now(), self.memory,
                                   thoi_tiet=moi() if callable(moi) else self._weather_text,
                                   co_thanh_pho=bool(getattr(w, "thanh_pho", "")), loi_thoi_tiet=getattr(w, "loi", "") or "")
        except Exception as e:  # lỗi thì để AI trả lời như thường
            log.warning("Trả lời nhanh lỗi: %s", type(e).__name__)
            return None
        if not noi:
            return None
        reply = Reply(noi=noi, cam_xuc=cam_xuc, hanh_dong="gat_dau")
        reply.user_msg_id = self.memory.add_message("user", user_text)
        reply.msg_id = self.memory.add_message("assistant", noi, cam_xuc)
        key = "nhanh_" + (now or datetime.now()).strftime("%Y-%m")  # đếm để nút "?" báo đã tiết kiệm bao nhiêu câu
        self.memory.set_kv(key, str(int(self.memory.get_kv(key, "0") or 0) + 1))
        key = "nhanh_ngay_" + (now or datetime.now()).date().isoformat()  # để câu miễn phí không tính vào DAILY_LIMIT
        self.memory.set_kv(key, str(int(self.memory.get_kv(key, "0") or 0) + 1))
        log.info("Trả lời nhanh (%s), không gọi API", loai)
        return reply

    def _chat(self, user_text: str) -> Reply:
        quick = self._quick(user_text)  # miễn phí nên vẫn trả lời khi đã hết lượt / hết ngân sách
        if quick:
            return quick
        if self._ai_replies_today() >= config.DAILY_LIMIT:
            return Reply(noi="Hôm nay mình nói nhiều quá rồi, mai nói tiếp nha!", cam_xuc="thuong")
        if self.over_budget():
            return Reply(
                noi="Tháng này Bơ tiêu hết ngân sách rồi, tháng sau nói tiếp nha! (Muốn tăng thì sửa MONTHLY_USD_LIMIT trong .env)",
                cam_xuc="thuong",
            )
        msg_id = self.memory.add_message("user", user_text)
        history = self._history()
        try:
            reply = self._ask(history, self.memory.pending_followups(config.FOLLOWUP_MIN_HOURS))
            reply.user_msg_id = msg_id
            if self._holiday_today(datetime.now()):  # đang trò chuyện thì Bơ đã biết lễ (trong lời dặn), khỏi chúc riêng
                self.memory.set_kv("le_da_chuc", date.today().isoformat())
            if reply.tam_trang:
                self.memory.set_mood(msg_id, reply.tam_trang)
            return reply
        except Exception:
            # Lỗi thì bỏ tin vừa gửi, để người dùng bấm gửi lại không bị lặp tin
            self.memory.delete_message(msg_id)
            raise

    def _greet(self, only_occasion: bool = False) -> Reply | None:
        """Bơ chủ động mở lời khi người dùng quay lại sau một thời gian và có chuyện nên hỏi thăm,
        hoặc đã lâu (GREET_MISS_DAYS ngày) không nói chuyện.
        Không có gì để hỏi hoặc vừa mới nói chuyện xong thì trả về None (không tốn câu API nào)."""
        if self._ai_replies_today() >= config.DAILY_LIMIT or self.over_budget():
            return None
        last = self.memory.last_message_time()
        followups = self.memory.pending_followups(config.FOLLOWUP_MIN_HOURS)
        days = (datetime.now() - last).days if last else 0
        week = self._recap_week()
        recap = wish_holiday = wish_moc = False
        now = datetime.now()
        eve = self.memory.special_days_tomorrow(now.date()) if now.hour >= 8 else []
        holiday = self._holiday_today(now)
        moc = self._moc_quen(now)
        if self.memory.special_days_today():
            trigger = SPECIAL_TRIGGER  # ngày đặc biệt chưa chúc thì chúc ngay, dù vừa mới nói chuyện
            eve = []
        elif eve:
            trigger = EVE_TRIGGER.format(items="; ".join(d["viec"] for d in eve))
        elif holiday:
            trigger, wish_holiday = HOLIDAY_TRIGGER.format(items=", ".join(holiday)), True
            if moc:  # cùng ngày thì gộp, khỏi gửi thêm một câu riêng
                trigger, wish_moc = trigger[:-1] + MOC_THEM.format(n=moc), True
        elif moc:
            trigger, wish_moc = MOC_TRIGGER.format(n=moc, tu=self.memory.stats(now.date())["quen_tu"]), True
            if week:  # tối Chủ nhật trùng mốc: điểm lại tuần luôn trong câu này
                trigger = trigger[:-1] + " Sau đó điểm lại tuần qua thật ngắn. Những gì người dùng đã kể trong tuần:\n" \
                    + self._week_items(now) + ")"
                recap = True
        elif week:
            trigger, recap = WEEK_TRIGGER.format(items=self._week_items(now)), True
        elif only_occasion:
            return None
        elif last and (datetime.now() - last).total_seconds() < config.GREET_AFTER_HOURS * 3600:
            return None
        elif followups:
            trigger = GREET_TRIGGER
        elif last and config.GREET_MISS_DAYS > 0 and days >= config.GREET_MISS_DAYS:
            trigger = MISS_TRIGGER.format(days=days)  # lâu không gặp thì chào dù không có gì để hỏi
        else:
            return None
        history = self._history()
        history.append({"role": "user", "content": trigger})  # chỉ gửi đi, không lưu
        reply = self._ask(clean_history(history), followups, from_user=False)
        if wish_moc:
            self.memory.set_kv("moc_quen", f"{moc}|{self.memory.stats(now.date())['quen_tu']}")  # mốc này đã nhắc rồi
        if recap:
            self.memory.set_kv("tong_ket_tuan", week)  # tuần này đã điểm lại rồi
        if wish_holiday:
            self.memory.set_kv("le_da_chuc", now.date().isoformat())  # hôm nay đã chúc lễ rồi
        if eve:  # năm nay đã nhắc trước rồi
            self.memory.mark_eve_reminded([d["id"] for d in eve], now.date() + timedelta(days=1))
        return reply

    def _week_items(self, now: datetime) -> str:
        """Chuyện trong tuần để tổng kết: ưu tiên nhật ký (gọn, đúng ngày); ít nhật ký thì lấy tin nhắn."""
        diary = self.memory.diary_recent(now.date(), days=7)
        if len(diary) >= 3:
            lines = []
            for d in diary:
                try:
                    day = datetime.fromisoformat(d["ngay"])
                    label = f"{THU[day.weekday()]} {day:%d/%m}"
                except ValueError:
                    label = d["ngay"]
                lines.append(f"- {label}: {d['noi_dung']}")
            return "\n".join(lines)[-4000:]
        msgs = self.memory.user_messages_since(now - timedelta(days=7))
        return "\n".join(f"- {m['content'][:200]}" for m in msgs)[-4000:]

    def _holiday_today(self, now: datetime) -> list[str]:
        """Ngày lễ hôm nay mà Bơ chưa chúc (từ 7h sáng; mỗi ngày lễ chúc một lần)."""
        if not config.CHUC_LE or now.hour < 7 or self.memory.get_kv("le_da_chuc") == now.date().isoformat():
            return []
        try:
            from .am_lich import ngay_le

            return ngay_le(now.date())
        except Exception:
            return []

    def _moc_quen(self, now: datetime) -> str:
        """Hôm nay tròn mốc quen nhau mà chưa nhắc → chữ mô tả ("100 ngày", "1 năm"); không thì "".
        Mốc ngày: ngày quen đầu tiên là ngày 1. Mốc năm: đúng ngày tháng quen nhau (29/02 thì 28/02 năm thường)."""
        if now.hour < 7:
            return ""
        st = self.memory.stats(now.date())
        if not st["quen_tu"]:
            return ""
        first = datetime.strptime(st["quen_tu"], "%d/%m/%Y").date()
        today, moc = now.date(), ""
        if st["so_ngay_quen"] in MOC_QUEN:
            moc = f"{st['so_ngay_quen']} ngày"
        years = today.year - first.year
        if years > 0:
            try:
                ky_niem = first.replace(year=today.year)
            except ValueError:  # quen ngày 29/02
                ky_niem = first.replace(year=today.year, day=28)
            if ky_niem == today:
                moc = f"{years} năm"
        if not moc or self.memory.get_kv("moc_quen") == f"{moc}|{st['quen_tu']}":
            return ""
        return moc

    def _recap_week(self, now: datetime | None = None) -> str:
        """Tối Chủ nhật, tuần này chưa điểm lại, và trong tuần có nói chuyện (≥5 tin) → trả mã tuần ("2026-W41")."""
        now = now or datetime.now()
        if not config.WEEKLY_RECAP or now.weekday() != 6 or now.hour < 17:
            return ""
        y, w, _ = now.isocalendar()
        week = f"{y}-W{w:02d}"
        if self.memory.get_kv("tong_ket_tuan") == week:
            return ""
        if len(self.memory.user_messages_since(now - timedelta(days=7))) < 5:
            return ""
        return week

    def _upcoming(self, today) -> list[dict]:
        """Ngày đặc biệt trong 7 ngày tới (lỗi thì bỏ qua, không làm hỏng câu trả lời)."""
        try:
            return self.memory.upcoming_special_days(today, days=7)
        except Exception:
            return []

    def _history(self) -> list[dict]:
        """Lịch sử gần đây gửi cho AI. Tin của người dùng gửi từ hôm trước được ghi chú ngày gửi ở đầu,
        để AI không hiểu "mai", "chiều nay" trong tin cũ là tính từ hôm nay (lịch sử vốn không có ngày giờ)."""
        now = datetime.now()
        out = []
        for m in self.memory.recent_messages(config.HISTORY_LIMIT, with_time=True):
            content = m["content"]
            khi = _when(m["created_at"] or "", now) if m["role"] == "user" else ""
            if khi and khi != "hôm nay":
                content = f"(tin gửi {khi}, {m['created_at'][8:10]}/{m['created_at'][5:7]}) {content}"
            out.append({"role": m["role"], "content": content})
        return clean_history(out)

    def _snapshot(self, today) -> dict | None:
        """Chụp những thứ Bơ có thể ghi (lời nhắc, việc, thói quen, ngày đặc biệt, điều nhớ, nhật ký) để so
        trước/sau một câu trả lời — xem mo_ta_thay_doi. Lỗi thì trả None (bỏ dòng "Bơ đã ghi", không hỏng câu trả lời)."""
        try:
            m = self.memory
            return {
                "nhac": {r["id"]: r for r in m.upcoming_reminders()},
                "viec": {t["id"]: t for t in m.todos()},
                "thoi_quen": {h["id"]: {"ten": h["ten"], "hom_nay": h["hom_nay"], "hom_qua": h["ngay_30"][-2]}
                              for h in m.habits(today)},
                "ngay": {d["id"]: d for d in m.special_days()},
                "nho": m.all_facts(),
                "nhat_ky": {d["id"]: d["noi_dung"] for d in m.diary_recent(today, days=2)},
            }
        except Exception as e:
            log.warning("Không chụp được trí nhớ: %s", type(e).__name__)
            return None

    def _ask(self, history: list[dict], followups: list[dict], from_user: bool = True) -> Reply:
        summary, _ = self.memory.latest_summary()
        from datetime import date

        today = date.today()  # tính một lần: trả lời xong qua nửa đêm thì không đánh dấu nhầm ngày mới
        special = self.memory.special_days_today(today)
        weather = self._weather_text
        system = build_system_prompt(
            self.persona(), self.memory.all_facts(), summary, followups, special=special, weather=weather,
            low_mood=self.memory.low_mood(today),
            todos=self.memory.todos(include_done=False),  # tối đa TODO_MAX (50) việc
            upcoming=self._upcoming(today),
            diary=self.memory.diary_recent(today, days=3),
            habits=self.memory.habits(today),
            reminders=self.memory.upcoming_reminders(),
        )
        resp = self._create(
            model=config.MODEL,
            max_tokens=config.MAX_TOKENS,
            system=cache_blocks(system) if self._cache_prompt else system,
            messages=history,
            output_config={"format": {"type": "json_schema", "schema": REPLY_SCHEMA}},
        )
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        if getattr(resp, "stop_reason", "") == "refusal":
            # Model từ chối vì lý do an toàn: chữ trả về (nếu có) không theo khuôn JSON, đừng đọc ra
            log.warning("Model từ chối trả lời (stop_reason=refusal)")
            raise EmptyReplyError("Câu này Bơ không trả lời được. Mình nói chuyện khác nha.")
        if not text.strip():
            # Không có chữ nào (thường do hết max_tokens khi model "suy nghĩ"): báo lỗi rõ, không lưu "..."
            kinds = [getattr(b, "type", "?") for b in resp.content]
            reason = getattr(resp, "stop_reason", "?")
            log.warning("Câu trả lời rỗng: stop_reason=%s, các khối=%s", reason, kinds)
            raise EmptyReplyError(f"Bơ bị khựng, không nói ra được câu nào (stop_reason={reason}). Nhắn lại giúp Bơ nha.")
        reply = parse_reply(text)

        reply.msg_id = self.memory.add_message("assistant", reply.noi, reply.cam_xuc)
        truoc = self._snapshot(today)
        if not from_user:
            # Bơ tự mở lời (chào, chúc lễ, tổng kết tuần...): người dùng chưa nói gì mới, nên không có gì để ghi.
            # Không chặn thì AI bịa việc từ chuyện cũ trong lịch sử (ghi lại điều đã nhớ, tạo "ngày quen nhau"...).
            for ten in ("quen", "ghi_nho", "hoi_tham", "nhac", "huy_nhac", "xong_viec", "viec_can_lam", "ngay_dac_biet"):
                setattr(reply, ten, [])
        # Chuyện vừa hỏi thăm xong mà AI lại chép vào "hoi_tham" thì bỏ, kẻo lần sau Bơ hỏi lại đúng chuyện đó
        vua_hoi = self.memory.followup_keys(reply.da_hoi)
        reply.hoi_tham = [x for x in reply.hoi_tham if not self.memory.followup_keys([x]) & vua_hoi]
        self.memory.forget_facts(reply.quen)
        self.memory.add_facts(reply.ghi_nho)
        self.memory.done_followups(reply.da_hoi)
        self.memory.add_followups(reply.hoi_tham)
        self.memory.cancel_reminders(reply.huy_nhac)
        self.memory.add_reminders(reply.nhac)
        self.memory.done_todos(reply.xong_viec)
        self.memory.add_todos(reply.viec_can_lam)
        if from_user:
            self.memory.add_habits(reply.thoi_quen_moi)
            self.memory.done_habits(reply.thoi_quen_xong, today)
            self.memory.done_habits(reply.thoi_quen_hom_qua, today - timedelta(days=1))
        if from_user:  # Bơ tự mở lời (tổng kết tuần...) thì không ghi: chuyện cũ sẽ bị ghi nhầm vào hôm nay
            self.memory.add_diary(reply.nhat_ky, today)
        eve_before = {d["id"] for d in self.memory.special_days_tomorrow(today)}
        self.memory.add_special_days(reply.ngay_dac_biet)
        # Đã chúc trong câu này (hoặc người dùng vừa kể "hôm nay sinh nhật mình", Bơ đã biết) → không chúc lại trong năm
        self.memory.mark_wished([d["id"] for d in self.memory.special_days_today(today)], on=today)
        # Người dùng vừa kể một ngày đặc biệt rơi vào ngày mai → Bơ đã biết, khỏi nhắc trước nữa
        new_eve = [d["id"] for d in self.memory.special_days_tomorrow(today) if d["id"] not in eve_before]
        self.memory.mark_eve_reminded(new_eve, today + timedelta(days=1))
        if truoc is not None:
            try:
                reply.da_ghi = mo_ta_thay_doi(truoc, self._snapshot(today) or truoc)
                if reply.da_ghi:
                    self.memory.set_note(reply.msg_id, reply.da_ghi)
            except Exception as e:  # dòng "Bơ đã ghi" chỉ là phụ, lỗi thì bỏ qua
                log.warning("Không tạo được dòng 'Bơ đã ghi': %s", type(e).__name__)
        if self._background:
            threading.Thread(target=self._housekeeping, daemon=True).start()
        else:
            self._housekeeping()
        return reply

    def _housekeeping(self) -> None:
        # Việc nền chỉ chạy một lượt một lúc; đang chạy thì bỏ qua (lần sau làm).
        # Không giữ khóa chính trong lúc chờ API, để tin nhắn mới không phải đợi.
        if not self._hk_lock.acquire(blocking=False):
            return
        try:
            self.maybe_merge_facts()
            self.maybe_summarize()
        finally:
            self._hk_lock.release()

    def maybe_summarize(self) -> None:
        """Gom tin nhắn cũ thành một đoạn tóm tắt ngắn, để Bơ nhớ chuyện xa mà không tốn nhiều tiền."""
        with self._lock:
            old = self.memory.messages_to_summarize(config.HISTORY_LIMIT)
            if len(old) < config.SUMMARY_BATCH:
                return
            previous, upto_before = self.memory.latest_summary()
        lines = "\n".join(f"{'Người dùng' if m['role'] == 'user' else 'Bơ'}: {m['content']}" for m in old)
        prompt = f"Bản tóm tắt cũ:\n{previous or '(chưa có)'}\n\nĐoạn trò chuyện mới:\n{lines}"
        try:
            resp = self._create(
                retries=0,  # việc phụ: lỗi thì lần sau làm, không bắt người dùng chờ
                kind="tom_tat",
                model=config.MODEL,
                max_tokens=config.MAX_TOKENS,
                system=SUMMARY_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as e:
            log.warning("Tóm tắt lỗi (sẽ thử lại sau): %s", friendly_error(e) + f" [{type(e).__name__}]")
            return  # tóm tắt lỗi thì lần sau thử lại, không làm hỏng câu trả lời
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
        with self._lock:
            # trong lúc chờ API mà đã có bản tóm tắt khác (ví dụ vừa nạp sao lưu) thì bỏ bản này
            if text and self.memory.latest_summary()[1] == upto_before:
                self.memory.add_summary(text, old[-1]["id"])

    def maybe_merge_facts(self) -> None:
        """Danh sách dài thì nhờ AI gộp điều trùng ý, bỏ điều mâu thuẫn cũ. Lỗi thì giữ nguyên."""
        with self._lock:
            facts = self.memory.all_facts()
        if len(facts) < config.FACTS_MERGE_AT or (self._merged_at and len(facts) < self._merged_at + 10):
            return
        listing = f"Hôm nay là {date.today():%d/%m/%Y}.\n" + "\n".join(f"- {f}" for f in facts)
        try:
            resp = self._create(
                retries=0,
                kind="gop",
                model=config.MODEL,
                max_tokens=config.MAX_TOKENS,
                system=MERGE_PROMPT,
                messages=[{"role": "user", "content": listing}],
            )
            text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
            match = re.search(r"\[.*\]", text, re.DOTALL)
            merged = [str(x).strip() for x in json.loads(match.group(0)) if str(x).strip()] if match else []
        except Exception as e:
            log.warning("Gộp trí nhớ lỗi: %s", type(e).__name__)
            merged = []
        # Chỉ nhận kết quả hợp lý: không rỗng, không dài hơn danh sách cũ, và không bị xóa quá tay
        # (danh sách từ 9 điều mà còn chưa tới một phần ba thì coi như AI dọn hỏng, giữ nguyên bản cũ)
        qua_tay = len(facts) >= 9 and len(merged) * 3 < len(facts)
        with self._lock:
            if self.memory.all_facts() != facts:
                return  # trong lúc gộp, người dùng đã xóa/thêm điều mới → bỏ kết quả, lần sau gộp lại
            if merged and len(merged) <= len(facts) and not qua_tay:
                self.memory.replace_facts(merged)
                self._merged_at = len(self.memory.all_facts())
                return
            self._merged_at = len(facts)  # kết quả lạ: chờ thêm 10 điều mới rồi mới thử lại
