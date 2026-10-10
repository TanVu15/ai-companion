"""Đọc cấu hình từ file .env (API key, tên model, đường dẫn dữ liệu)."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = os.getenv("MODEL", "claude-haiku-5-5")
DEMO = os.getenv("DEMO", "0") == "1"
DB_PATH = Path(os.getenv("DB_PATH", ROOT / "data" / "companion.db"))
PERSONA_PATH = ROOT / "persona.md"
# Tính cách Tân tự sửa trên web (nằm trong data/ nên git pull không đè, không bị đưa lên GitHub)
# (tính theo thư mục dự án, và tên khác persona.md, để không bao giờ đè lên file gốc)
PERSONA_CUSTOM_PATH = (ROOT / DB_PATH).resolve().parent / "persona_tu_sua.md"

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

# Giá API (đô la Mỹ cho 1 triệu token) để ước tính chi phí. Kiểm tra giá mới ở trang giá của Anthropic.
PRICE_INPUT_PER_MTOK = float(os.getenv("PRICE_INPUT_PER_MTOK", "1"))
PRICE_OUTPUT_PER_MTOK = float(os.getenv("PRICE_OUTPUT_PER_MTOK", "5"))

# Ngân sách mỗi tháng (đô la Mỹ, ước tính theo giá ở trên). Tiêu tới mức này thì Bơ nghỉ tới tháng sau. 0 = không giới hạn.
MONTHLY_USD_LIMIT = float(os.getenv("MONTHLY_USD_LIMIT", "0"))

EMOTIONS = ["vui", "hao_hung", "binh_thuong", "suy_nghi", "ngac_nhien", "buon", "thuong"]
ACTIONS = ["khong", "gat_dau", "lac_dau", "nghieng_dau", "nhay", "vay_tay"]
# Tâm trạng của NGƯỜI DÙNG mà Bơ đoán từ tin nhắn (khác cảm xúc khuôn mặt của Bơ)
MOODS = ["vui", "binh_thuong", "buon", "met", "lo", "gian"]
