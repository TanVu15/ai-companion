"""Giọng nói AI miễn phí cho Bơ: edge-tts (giọng tiếng Việt của Microsoft Edge, không cần tài khoản).

Chạy trên máy chủ (máy của Tân), web nhận file mp3 để phát. Mỗi câu tạo một lần rồi lưu đệm trong
data/am_thanh/ (tên file = mã băm của chữ + giọng), quá AM_THANH_GIU file thì xóa bớt file cũ nhất.
Lỗi (không có mạng, Microsoft đổi gì đó) → báo GiongLoi để web tự quay về giọng của trình duyệt.
"""
import asyncio
import hashlib
import os
import re
import tempfile
from pathlib import Path

from . import config
from .nhat_ky import log

GIONG = {"vi-VN-HoaiMyNeural": "Hoài My (nữ)", "vi-VN-NamMinhNeural": "Nam Minh (nam)"}
DAI_TOI_DA = 600  # chữ; câu dài hơn thì web tự tách câu rồi gửi từng đoạn


class GiongLoi(Exception):
    pass


# Lần gần nhất thật sự gọi Microsoft (không tính lấy trong đệm) — để nút "?" → Tình trạng báo.
# Chỉ giữ trong bộ nhớ: chạy lại máy chủ thì về "chưa thử".
trang_thai: dict = {"luc": None, "ok": None, "loi": ""}


def _ghi(ok: bool, loi: str = "") -> None:
    from datetime import datetime

    trang_thai.update(luc=datetime.now(), ok=ok, loi=loi)


def da_cai() -> bool:
    """Máy đã cài thư viện edge-tts chưa (không import thật, không gọi mạng)."""
    import importlib.util

    return importlib.util.find_spec("edge_tts") is not None


def tinh_trang() -> tuple[bool, str]:
    """(ổn?, câu dễ hiểu) cho mục "Giọng AI" trong Tình trạng."""
    luc, ok, loi = trang_thai["luc"], trang_thai["ok"], trang_thai["loi"]
    if luc is None:
        if tong_hop is _edge_tts and not da_cai():
            return False, "Chưa cài edge-tts — chạy lại run.bat (nó tự cài); trong lúc đó Bơ dùng giọng của trình duyệt"
        return True, "Chưa đọc câu nào từ lúc mở máy chủ — bật \"Giọng nói\" rồi nhắn một câu để thử"
    gio = luc.strftime("%H:%M")
    if ok:
        return True, f"Dùng được — đọc thành công lần gần nhất lúc {gio}"
    return False, f"Lỗi lúc {gio}: {loi} — Bơ đang dùng giọng của trình duyệt, sẽ thử lại sau"


async def _edge_tts(text: str, giong: str, toc_do: str, cao_do: str) -> bytes:
    """Gọi edge-tts thật (cần mạng). Test thay hàm này bằng hàm giả, không gọi mạng."""
    import edge_tts

    out = bytearray()
    async for chunk in edge_tts.Communicate(text, giong, rate=toc_do, pitch=cao_do).stream():
        if chunk.get("type") == "audio":
            out += chunk["data"]
    return bytes(out)


tong_hop = _edge_tts  # chỗ để test cắm hàm giả


def chuan_hoa(text: str) -> str:
    """Gọn khoảng trắng, cắt độ dài. Chữ rỗng → ''."""
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[:DAI_TOI_DA]


# Giọng đổi nhẹ theo cảm xúc của câu: (cộng thêm tốc độ %, cộng thêm cao độ Hz). Cảm xúc lạ/không có → giữ nguyên.
THEO_CAM_XUC = {
    "vui": (5, 4), "hao_hung": (10, 8), "ngac_nhien": (5, 6),
    "buon": (-10, -6), "thuong": (-5, 2), "suy_nghi": (-5, 0), "binh_thuong": (0, 0),
}


def tham_so(cam_xuc: str = "") -> tuple[str, str, str]:
    """(giọng, tốc độ "+10%", cao độ "+8Hz") đang dùng — theo cài đặt trên web hoặc .env, chỉnh nhẹ theo cảm xúc."""
    giong = config.GIONG if config.GIONG in GIONG else "vi-VN-HoaiMyNeural"
    them_toc, them_cao = THEO_CAM_XUC.get(cam_xuc or "", (0, 0))
    toc = max(-50, min(60, config.TOC_DO_GIONG + them_toc))
    cao = max(-40, min(50, config.CAO_DO_GIONG + them_cao))
    return giong, f"{toc:+d}%", f"{cao:+d}Hz"


def _ten_file(text: str, giong: str, toc_do: str, cao_do: str) -> str:
    return hashlib.sha1(f"{giong}|{toc_do}|{cao_do}|{text}".encode("utf-8")).hexdigest()[:24] + ".mp3"


def _don_bot(thu_muc: Path, giu: int) -> None:
    """Quá `giu` file thì xóa file lâu không dùng nhất (dùng lại một file sẽ làm mới giờ của nó)."""
    files = sorted(thu_muc.glob("*.mp3"), key=lambda f: f.stat().st_mtime)
    for f in files[: max(0, len(files) - giu)]:
        try:
            f.unlink()
        except OSError:
            pass


async def doc(text: str, thu_muc: Path | None = None, cam_xuc: str = "") -> bytes:
    """Chữ → mp3 (bytes). Có trong đệm thì lấy ra, không gọi mạng. cam_xuc: giọng vui/buồn hơn một chút."""
    text = chuan_hoa(text)
    if not text:
        raise GiongLoi("Không có chữ để đọc")
    giong, toc_do, cao_do = tham_so(cam_xuc)
    thu_muc = Path(thu_muc or config.AM_THANH_DIR)
    f = thu_muc / _ten_file(text, giong, toc_do, cao_do)
    if f.exists() and f.stat().st_size > 0:
        try:
            os.utime(f)
        except OSError:
            pass
        return f.read_bytes()
    try:
        mp3 = await asyncio.wait_for(tong_hop(text, giong, toc_do, cao_do), timeout=20)
    except asyncio.TimeoutError:
        _ghi(False, "máy chủ giọng phản hồi chậm quá 20 giây")
        raise GiongLoi("Giọng AI phản hồi chậm quá") from None
    except ImportError as e:
        _ghi(False, "chưa cài edge-tts (chạy lại run.bat)")
        log.warning("edge-tts chưa cài: %s", e)
        raise GiongLoi("Chưa cài edge-tts") from e
    except Exception as e:  # không có mạng, Microsoft từ chối...
        log.warning("edge-tts lỗi: %s: %s", type(e).__name__, e)
        _ghi(False, f"không gọi được máy chủ giọng ({type(e).__name__}) — kiểm tra mạng")
        raise GiongLoi("Không tạo được giọng AI (cần mạng)") from e
    if not mp3:
        _ghi(False, "máy chủ giọng không trả về âm thanh")
        raise GiongLoi("Giọng AI không trả về âm thanh")
    _ghi(True)
    try:
        thu_muc.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=thu_muc, suffix=".tmp", delete=False) as t:
            t.write(mp3)
        os.replace(t.name, f)  # ghi xong mới đổi tên: hai yêu cầu cùng lúc không làm hỏng file
        _don_bot(thu_muc, config.AM_THANH_GIU)
    except OSError as e:
        log.warning("Không lưu đệm được giọng: %s", e)
    return mp3
