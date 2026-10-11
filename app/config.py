"""Đọc cấu hình từ file .env (API key, tên model, đường dẫn dữ liệu)."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = os.getenv("MODEL", "claude-haiku-5-5")
DEMO = os.getenv("DEMO", "0") == "1"
# Giới hạn độ dài mỗi lần gọi API. Câu trả lời JSON của Bơ có nhiều mục, đặt thấp quá sẽ bị cắt mất chữ.
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))
DB_PATH = Path(os.getenv("DB_PATH", ROOT / "data" / "companion.db"))
PERSONA_PATH = ROOT / "persona.md"
# Tính cách Tân tự sửa trên web (nằm trong data/ nên git pull không đè, không bị đưa lên GitHub)
# (tính theo thư mục dự án, và tên khác persona.md, để không bao giờ đè lên file gốc)
PERSONA_CUSTOM_PATH = (ROOT / DB_PATH).resolve().parent / "persona_tu_sua.md"
# Cài đặt Tân chỉnh trên web (thành phố, giờ yên lặng...), ưu tiên hơn .env. Xem app/cai_dat.py
CAI_DAT_PATH = (ROOT / DB_PATH).resolve().parent / "cai_dat.json"

# Số tin nhắn gần nhất gửi kèm mỗi lần hỏi bộ não (giữ chi phí thấp)
HISTORY_LIMIT = int(os.getenv("HISTORY_LIMIT", "20"))
# Số câu trả lời tối đa mỗi ngày, để không lỡ tiêu quá nhiều tiền API
DAILY_LIMIT = int(os.getenv("DAILY_LIMIT", "300"))

# Khi có đủ ngần này tin nhắn cũ (ngoài lịch sử gần nhất) thì tóm tắt lại một lần
SUMMARY_BATCH = int(os.getenv("SUMMARY_BATCH", "20"))
# Khi danh sách điều đáng nhớ dài tới ngần này thì nhờ AI gộp/dọn lại (mỗi lần thêm 10 điều mới thử lại)
FACTS_MERGE_AT = int(os.getenv("FACTS_MERGE_AT", "30"))

# Chuyện cần hỏi thăm chỉ được nhắc sau ngần này giờ (để Bơ không hỏi lại ngay lúc vừa nghe kể)
FOLLOWUP_MIN_HOURS = float(os.getenv("FOLLOWUP_MIN_HOURS", "3"))
# Mở web sau ngần này giờ không nói chuyện thì Bơ chủ động chào + hỏi thăm (nếu có chuyện để hỏi)
GREET_AFTER_HOURS = float(os.getenv("GREET_AFTER_HOURS", "3"))
# Lâu ngần này ngày không nói chuyện thì Bơ chào "lâu quá không gặp" dù không có chuyện để hỏi. 0 = tắt.
GREET_MISS_DAYS = int(os.getenv("GREET_MISS_DAYS", "2"))
# Tối Chủ nhật (từ 17h) mở web thì Bơ điểm lại tuần qua (1 câu API mỗi tuần). 0 = tắt.
WEEKLY_RECAP = os.getenv("WEEKLY_RECAP", "1") == "1"

# Ngày lễ (Tết, Trung thu, 20/10...) mở web thì Bơ chủ động chúc (1 câu API mỗi ngày lễ). 0 = tắt.
CHUC_LE = os.getenv("CHUC_LE", "1") == "1"

# Mỗi ngày tự sao lưu trí nhớ vào data/sao_luu/ (giữ SAO_LUU_GIU bản gần nhất). 0 = tắt.
TU_SAO_LUU = os.getenv("TU_SAO_LUU", "1") == "1"
SAO_LUU_GIU = int(os.getenv("SAO_LUU_GIU", "7"))
SAO_LUU_DIR = (ROOT / DB_PATH).resolve().parent / "sao_luu"

# Tối mà còn thói quen chưa làm thì Bơ nhắc nhẹ một lần lúc giờ này (miễn phí, không gọi API). Để trống = tắt.
NHAC_THOI_QUEN = os.getenv("NHAC_THOI_QUEN", "20:30")
# Giọng AI miễn phí (edge-tts, giọng Microsoft Edge, không cần tài khoản). Chỉnh được trên web (nút "?" → Cài đặt)
GIONG = os.getenv("GIONG", "vi-VN-HoaiMyNeural")
TOC_DO_GIONG = int(os.getenv("TOC_DO_GIONG", "0") or 0)  # phần trăm, -50..50
CAO_DO_GIONG = int(os.getenv("CAO_DO_GIONG", "8") or 0)  # Hz, -30..40; hơi cao cho dễ thương
AM_THANH_DIR = (ROOT / DB_PATH).resolve().parent / "am_thanh"
AM_THANH_GIU = 200  # giữ tối đa bấy nhiêu file mp3 đệm

# Câu hỏi ngắn (mấy giờ rồi, hôm nay ngày mấy âm, còn mấy ngày Tết, việc cần làm) Bơ tự trả lời, không tốn API. 0 = tắt.
TRA_LOI_NHANH = os.getenv("TRA_LOI_NHANH", "1") == "1"

# Giờ yên lặng "23-6": trong khoảng này Bơ không TỰ đọc to (lời nhắc, lời chào); vẫn hiện chữ. Để trống = tắt.
GIO_YEN_LANG = os.getenv("GIO_YEN_LANG", "23-6")

# Thành phố để Bơ biết thời tiết (Open-Meteo, miễn phí). Ví dụ "Da Nang". Để trống = tắt.
THANH_PHO = os.getenv("THANH_PHO", "")

# Gặp lỗi mạng/máy chủ bận thì thử lại tối đa ngần này lần; mỗi lần hỏi chờ tối đa API_TIMEOUT giây
API_RETRIES = int(os.getenv("API_RETRIES", "3"))
API_TIMEOUT = float(os.getenv("API_TIMEOUT", "30"))

# Mật khẩu vào web (bắt buộc nên đặt khi đưa Bơ ra ngoài mạng nhà). Để trống = không hỏi mật khẩu.
APP_PASSWORD = os.getenv("APP_PASSWORD", "")

# Khóa riêng cho thiết bị phần cứng (ESP32) gọi /api/thiet-bi/... Để trống = tắt cổng thiết bị.
DEVICE_KEY = os.getenv("DEVICE_KEY", "")

# Giá API (đô la Mỹ cho 1 triệu token: chiều vào, chiều ra) để ước tính chi phí. Giá Anthropic công bố, xem lại
# ở trang giá khi đổi model. Model lạ thì tính theo giá cao (1 / 5) để ngân sách tháng không bị vượt.
GIA_THEO_MODEL = {
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-haiku-4-5": (1.0, 5.0),
    "claude-sonnet-5": (2.0, 10.0),  # cả claude-sonnet-5-5
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-opus-5-5": (4.0, 20.0),
    "claude-opus-5": (5.0, 25.0),
}


def gia_theo_model(model: str) -> tuple[float, float]:
    """Giá của model (khớp theo tên dài nhất, nên "claude-haiku-5-5-xxx" vẫn ra giá Haiku 5.5)."""
    for ten in sorted(GIA_THEO_MODEL, key=len, reverse=True):
        if model.startswith(ten):
            return GIA_THEO_MODEL[ten]
    return (1.0, 5.0)


def _gia(ten_bien: str, mac_dinh: float) -> float:
    """Giá ghi trong .env; để trống hoặc ghi sai thì lấy theo bảng trên."""
    try:
        return float(os.getenv(ten_bien, "").strip() or mac_dinh)
    except ValueError:
        return mac_dinh


PRICE_INPUT_PER_MTOK = _gia("PRICE_INPUT_PER_MTOK", gia_theo_model(MODEL)[0])
PRICE_OUTPUT_PER_MTOK = _gia("PRICE_OUTPUT_PER_MTOK", gia_theo_model(MODEL)[1])

# Ngân sách mỗi tháng (đô la Mỹ, ước tính theo giá ở trên). Tiêu tới mức này thì Bơ nghỉ tới tháng sau. 0 = không giới hạn.
MONTHLY_USD_LIMIT = float(os.getenv("MONTHLY_USD_LIMIT", "0"))

EMOTIONS = ["vui", "hao_hung", "binh_thuong", "suy_nghi", "ngac_nhien", "buon", "thuong"]
ACTIONS = ["khong", "gat_dau", "lac_dau", "nghieng_dau", "nhay", "vay_tay"]
# Tâm trạng của NGƯỜI DÙNG mà Bơ đoán từ tin nhắn (khác cảm xúc khuôn mặt của Bơ)
MOODS = ["vui", "binh_thuong", "buon", "met", "lo", "gian"]
