"""Nhật ký lỗi: ghi lỗi ra data/loi.log để Tân gửi cho Claude khi gặp sự cố.

Chỉ ghi loại lỗi và vị trí trong code, không ghi nội dung tin nhắn hay API key.
File tự xoay vòng (tối đa 3 file × 1 MB) nên không bao giờ đầy ổ cứng.
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

log = logging.getLogger("bo")
log.setLevel(logging.INFO)


def bat_ghi_file(path: Path) -> None:
    """Bật ghi ra file (gọi một lần khi máy chủ khởi động). Gọi lại với cùng file thì bỏ qua."""
    path = Path(path)
    for h in log.handlers:
        if isinstance(h, RotatingFileHandler) and Path(h.baseFilename) == path.resolve():
            return
    path.parent.mkdir(parents=True, exist_ok=True)
    h = RotatingFileHandler(path, maxBytes=1_000_000, backupCount=2, encoding="utf-8")
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    log.addHandler(h)
