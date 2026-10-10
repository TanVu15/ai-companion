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

# Số tin nhắn gần nhất gửi kèm mỗi lần hỏi bộ não (giữ chi phí thấp)
HISTORY_LIMIT = int(os.getenv("HISTORY_LIMIT", "20"))
# Số câu trả lời tối đa mỗi ngày, để không lỡ tiêu quá nhiều tiền API
DAILY_LIMIT = int(os.getenv("DAILY_LIMIT", "300"))

EMOTIONS = ["vui", "hao_hung", "binh_thuong", "suy_nghi", "ngac_nhien", "buon", "thuong"]
ACTIONS = ["khong", "gat_dau", "lac_dau", "nghieng_dau", "nhay", "vay_tay"]
