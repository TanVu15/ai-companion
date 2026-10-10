"""Thời tiết miễn phí từ Open-Meteo (không cần tài khoản, không cần key).
Đặt THANH_PHO trong .env (ví dụ "Da Nang") để Bơ biết trời nắng hay mưa. Để trống = tắt.
Lỗi mạng thì trả None — Bơ vẫn nói chuyện bình thường, chỉ không biết thời tiết."""
import threading
import time

from .nhat_ky import log

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Mã thời tiết WMO → chữ tiếng Việt
WMO = {
    0: "trời quang", 1: "ít mây", 2: "có mây", 3: "nhiều mây", 45: "sương mù", 48: "sương mù",
    51: "mưa phùn nhẹ", 53: "mưa phùn", 55: "mưa phùn dày", 56: "mưa phùn lạnh", 57: "mưa phùn lạnh",
    61: "mưa nhẹ", 63: "mưa vừa", 65: "mưa to", 66: "mưa lạnh", 67: "mưa lạnh to",
    71: "tuyết nhẹ", 73: "tuyết", 75: "tuyết dày", 77: "tuyết hạt",
    80: "mưa rào nhẹ", 81: "mưa rào", 82: "mưa rào rất to", 85: "mưa tuyết", 86: "mưa tuyết to",
    95: "dông", 96: "dông kèm mưa đá", 99: "dông kèm mưa đá to",
}


def mo_ta(code) -> str:
    try:
        return WMO.get(int(code), "")
    except (TypeError, ValueError):
        return ""


def _ngay(daily: dict, i: int) -> str:
    try:
        lo, hi = round(daily["temperature_2m_min"][i]), round(daily["temperature_2m_max"][i])
    except (KeyError, IndexError, TypeError, ValueError):
        return ""
    out = f"{lo}–{hi}°C"
    try:
        desc = mo_ta(daily["weather_code"][i])
    except (KeyError, IndexError, TypeError):
        desc = ""
    if desc:
        out += f", {desc}"
    try:
        rain = daily["precipitation_probability_max"][i]
        if rain is not None:
            out += f", khả năng mưa {round(rain)}%"
    except (KeyError, IndexError, TypeError, ValueError):
        pass
    return out


def tom_tat(ten: str, data: dict) -> str | None:
    """Đổi dữ liệu Open-Meteo thành một dòng ngắn cho Bơ đọc."""
    parts = []
    cur = data.get("current") or {}
    if isinstance(cur.get("temperature_2m"), (int, float)):
        now = f"bây giờ {round(cur['temperature_2m'])}°C"
        desc = mo_ta(cur.get("weather_code"))
        parts.append(now + (f", {desc}" if desc else ""))
    daily = data.get("daily") or {}
    for i, label in ((0, "hôm nay"), (1, "ngày mai")):
        d = _ngay(daily, i)
        if d:
            parts.append(f"{label} {d}")
    return f"Thời tiết ở {ten}: " + "; ".join(parts) + "." if parts else None


class ThoiTiet:
    """Lấy thời tiết, nhớ kết quả 1 giờ (không hỏi lại mỗi tin nhắn). Lỗi thì 10 phút sau mới thử lại."""

    def __init__(self, thanh_pho: str, get=None, clock=time.monotonic):
        self.thanh_pho = thanh_pho.strip()
        self._get = get or self._http_get
        self._clock = clock
        self._toa_do = None  # (tên, vĩ độ, kinh độ)
        self._cache: tuple[float, str | None] | None = None
        self._lock = threading.Lock()  # hai tin cùng lúc thì chỉ hỏi mạng một lần
        self.loi = ""  # lỗi lần lấy gần nhất (để trang kiểm tra sức khỏe báo)

    def da_lay(self) -> str | None:
        """Kết quả lần lấy gần nhất, KHÔNG gọi mạng (dùng cho kiểm tra sức khỏe)."""
        return self._cache[1] if self._cache else None

    @staticmethod
    def _http_get(url: str, params: dict) -> dict:
        import httpx

        r = httpx.get(url, params=params, timeout=5)
        r.raise_for_status()
        return r.json()

    def _tim_toa_do(self):
        data = self._get(GEO_URL, {"name": self.thanh_pho, "count": 1, "language": "vi"})
        res = (data.get("results") or [None])[0]
        if not res:
            raise ValueError(f"Không tìm thấy thành phố '{self.thanh_pho}'")
        return res.get("name") or self.thanh_pho, res["latitude"], res["longitude"]

    def hien_tai(self) -> str | None:
        if not self.thanh_pho:
            return None
        with self._lock:
            return self._hien_tai()

    def _hien_tai(self) -> str | None:
        now = self._clock()
        if self._cache and now < self._cache[0]:
            return self._cache[1]
        try:
            if self._toa_do is None:
                self._toa_do = self._tim_toa_do()
            ten, lat, lon = self._toa_do
            data = self._get(FORECAST_URL, {
                "latitude": lat, "longitude": lon, "timezone": "auto", "forecast_days": 2,
                "current": "temperature_2m,weather_code",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
            })
            text = tom_tat(ten, data)
            self._cache = (now + 3600, text)
            self.loi = ""
        except Exception as e:
            log.warning("Lấy thời tiết lỗi: %s", e)
            self.loi = str(e) if isinstance(e, ValueError) else "mất mạng hoặc Open-Meteo không trả lời"
            text = self._cache[1] if self._cache else None  # có bản cũ thì dùng tạm
            self._cache = (now + 600, text)
        return text
