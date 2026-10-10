"""Cài đặt chỉnh trên web: lưu ở data/cai_dat.json, ưu tiên hơn giá trị trong .env.

Chỉ gồm vài cài đặt không bí mật (không có API key, mật khẩu). Xóa file = về như .env.
"""
import json
import os
import re

from . import config
from .nhat_ky import log

# Giá trị lấy từ .env lúc khởi động (để "Về mặc định" quay lại đúng như .env)
MAC_DINH = {
    "thanh_pho": config.THANH_PHO,
    "gio_yen_lang": config.GIO_YEN_LANG,
    "tong_ket_tuan": config.WEEKLY_RECAP,
}
_THUOC_TINH = {"thanh_pho": "THANH_PHO", "gio_yen_lang": "GIO_YEN_LANG", "tong_ket_tuan": "WEEKLY_RECAP"}


def kiem_tra(key: str, value):
    """Chuẩn hóa một giá trị; sai thì báo ValueError bằng câu dễ hiểu."""
    if key == "thanh_pho":
        if not isinstance(value, str):
            raise ValueError("Tên thành phố phải là chữ")
        value = " ".join(value.split())
        if len(value) > 60:
            raise ValueError("Tên thành phố dài quá")
        return value
    if key == "gio_yen_lang":
        if not isinstance(value, str):
            raise ValueError("Giờ yên lặng phải dạng 23-6")
        value = value.replace(" ", "").replace("h", "")
        if value == "":
            return ""
        m = re.fullmatch(r"(\d{1,2})-(\d{1,2})", value)
        if not m or int(m.group(1)) > 23 or int(m.group(2)) > 23 or m.group(1) == m.group(2):
            raise ValueError("Giờ yên lặng phải dạng 23-6 (từ 23h đến 6h), giờ từ 0 đến 23")
        return f"{int(m.group(1))}-{int(m.group(2))}"
    if key == "tong_ket_tuan":
        if not isinstance(value, bool):
            raise ValueError("Tổng kết tuần chỉ bật hoặc tắt")
        return value
    raise ValueError(f"Không có cài đặt '{key}'")


def doc() -> dict:
    """Những cài đặt đã chỉnh trên web (bỏ qua mục lạ/sai)."""
    try:
        data = json.loads(config.CAI_DAT_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as e:
        log.warning("Đọc cai_dat.json lỗi, dùng .env: %s", e)
        return {}
    out = {}
    if isinstance(data, dict):
        for k, v in data.items():
            try:
                out[k] = kiem_tra(k, v)
            except ValueError:
                pass
    return out


def hien_tai() -> dict:
    """Giá trị đang dùng (web chỉnh > .env), chỉ đọc, không đổi config."""
    da_chinh = doc()
    return {k: da_chinh.get(k, v) for k, v in MAC_DINH.items()}


def ap_dung() -> dict:
    """Đặt giá trị đang dùng vào config (web chỉnh > .env). Trả về các giá trị đang dùng."""
    da_chinh = doc()
    hien_tai = {k: da_chinh.get(k, v) for k, v in MAC_DINH.items()}
    for k, v in hien_tai.items():
        setattr(config, _THUOC_TINH[k], v)
    return hien_tai


def luu(thay_doi: dict) -> dict:
    """Lưu các mục thay đổi (đã kiểm tra hết trước khi ghi) rồi áp dụng ngay."""
    if not isinstance(thay_doi, dict):
        raise ValueError("Dữ liệu cài đặt không hợp lệ")
    moi = {k: kiem_tra(k, v) for k, v in thay_doi.items()}
    data = {**doc(), **moi}
    # Giống hệt .env thì khỏi lưu, để sau này Tân sửa .env vẫn có tác dụng
    data = {k: v for k, v in data.items() if v != MAC_DINH.get(k)}
    path = config.CAI_DAT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)  # ghi xong mới thay, mất điện giữa chừng không hỏng file
    return ap_dung()


def ve_mac_dinh() -> dict:
    config.CAI_DAT_PATH.unlink(missing_ok=True)
    return ap_dung()
