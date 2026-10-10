"""Tự sao lưu trí nhớ mỗi ngày vào data/sao_luu/ (giữ vài bản gần nhất).

Lỡ file trí nhớ bị hỏng hay lỡ tay "Xóa hết" thì vẫn còn bản hôm qua:
mở web → "?" → Khôi phục → chọn file trong data/sao_luu/.
"""
import json
import os
import re
from datetime import date
from pathlib import Path

TEN = re.compile(r"^bo-\d{4}-\d{2}-\d{2}\.json$")


def ds_ban_sao(folder: Path) -> list[Path]:
    """Các bản tự sao lưu, mới nhất trước."""
    folder = Path(folder)
    if not folder.is_dir():
        return []
    return sorted((p for p in folder.iterdir() if TEN.match(p.name)), reverse=True)


def tu_sao_luu(memory, folder: Path, today: date | None = None, giu: int = 7, lock=None) -> Path | None:
    """Ghi bản sao lưu hôm nay nếu chưa có, rồi xóa bớt bản cũ (chỉ giữ `giu` bản).
    Trả về đường dẫn file mới, hoặc None nếu hôm nay đã có."""
    folder = Path(folder)
    today = today or date.today()
    path = folder / f"bo-{today.isoformat()}.json"
    if path.exists():
        return None
    folder.mkdir(parents=True, exist_ok=True)
    if lock is not None:
        with lock:
            data = memory.export_all()
    else:
        data = memory.export_all()
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)  # ghi xong mới đổi tên: mất điện giữa chừng không để lại file dở
    for old in ds_ban_sao(folder)[max(giu, 1):]:
        try:
            old.unlink()
        except OSError:
            pass
    return path
