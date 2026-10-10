"""Máy chủ web: phục vụ trang chat và nhận tin nhắn gửi tới bộ não."""
import base64
import secrets

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import config
from .brain import Brain, cost_usd, friendly_error
from .memory import Memory

app = FastAPI(title="AI Companion")
app.mount("/web", StaticFiles(directory=config.ROOT / "web"), name="web")
_brain: Brain | None = None


def _password_ok(header: str) -> bool:
    """Kiểm tra mật khẩu kiểu "Basic" (trình duyệt tự hiện ô nhập). Tên đăng nhập gõ gì cũng được."""
    if not header.startswith("Basic "):
        return False
    try:
        _, _, pw = base64.b64decode(header[6:]).decode("utf-8").partition(":")
    except Exception:
        return False
    return secrets.compare_digest(pw.encode(), config.APP_PASSWORD.encode())


@app.middleware("http")
async def require_password(request: Request, call_next):
    if request.url.path.startswith("/api/thiet-bi/"):
        return await call_next(request)  # thiết bị dùng khóa riêng (DEVICE_KEY), kiểm tra bên dưới
    if config.APP_PASSWORD and not _password_ok(request.headers.get("authorization", "")):
        return Response(
            "Cần mật khẩu để nói chuyện với Bơ.",
            status_code=401,
            headers={"WWW-Authenticate": 'Basic realm="Bo", charset="UTF-8"'},
            media_type="text/plain; charset=utf-8",
        )
    return await call_next(request)


class _DemoClient:
    """Bộ não giả cho chế độ DEMO=1: xem giao diện mà chưa cần API key."""

    def __init__(self):
        import itertools
        import json
        from types import SimpleNamespace

        self._ns = SimpleNamespace
        self._cycle = itertools.cycle([
            ("vui", "vay_tay"), ("hao_hung", "nhay"), ("suy_nghi", "nghieng_dau"),
            ("ngac_nhien", "khong"), ("thuong", "gat_dau"), ("buon", "lac_dau"),
        ])
        self._json = json
        self.messages = SimpleNamespace(create=self._create)

    def _create(self, messages, **_):
        emo, act = next(self._cycle)
        last = messages[-1]["content"]
        text = self._json.dumps({"noi": f"(demo) Bạn vừa nói: {last}", "cam_xuc": emo, "hanh_dong": act})
        return self._ns(content=[self._ns(type="text", text=text)])


def get_brain() -> Brain:
    global _brain
    if _brain is None:
        if config.DEMO:
            _brain = Brain(Memory(config.DB_PATH.with_name("demo.db")), client=_DemoClient())
            return _brain
        if not config.ANTHROPIC_API_KEY:
            raise HTTPException(500, "Chưa có ANTHROPIC_API_KEY trong file .env")
        _brain = Brain(Memory(config.DB_PATH))
    return _brain


class ChatIn(BaseModel):
    text: str


class FactIn(BaseModel):
    content: str


@app.get("/")
def index():
    return FileResponse(config.ROOT / "web" / "index.html")


@app.post("/api/chat")
def chat(body: ChatIn):
    text = body.text.strip()
    if not text:
        raise HTTPException(400, "Tin nhắn trống")
    try:
        reply = get_brain().chat(text[:2000])
    except HTTPException:
        raise
    except Exception as e:  # lỗi mạng, hết tiền API... (đã thử lại vài lần trong bộ não)
        raise HTTPException(502, friendly_error(e))
    return reply.to_dict()


@app.post("/api/chao")
def greet():
    """Gọi khi mở web: Bơ chủ động hỏi thăm chuyện cũ nếu có. Không có thì trả {"noi": null}."""
    try:
        reply = get_brain().greet()
    except HTTPException:
        raise
    except Exception:
        reply = None  # mở lời không được thì thôi, không báo lỗi làm phiền
    return reply.to_dict() if reply else {"noi": None}


@app.get("/api/chi-phi")
def usage():
    """Chi phí API hôm nay và từ đầu tháng (ước tính theo giá trong .env)."""
    from datetime import date

    mem = get_brain().memory
    today = date.today()
    out = {}
    for name, since in (("hom_nay", today), ("thang_nay", today.replace(day=1))):
        u = mem.usage_since(since.isoformat())
        out[name] = {**u, "usd": round(cost_usd(u), 4)}
    out["gioi_han_ngay"] = config.DAILY_LIMIT
    out["da_tra_loi_hom_nay"] = mem.replies_today()
    return out


@app.get("/api/history")
def history():
    return get_brain().memory.recent_messages(50)


@app.get("/api/facts")
def facts():
    return get_brain().memory.all_facts()


@app.delete("/api/facts/all")
def clear_facts():
    get_brain().memory.clear_facts()
    return {"ok": True}


@app.delete("/api/facts")
def delete_fact(body: FactIn):
    get_brain().memory.delete_fact(body.content)
    return {"ok": True}


# --- Cổng cho thiết bị phần cứng (ESP32...) — xem THIET_BI.md ---
def bo_dau(text: str) -> str:
    """Bỏ dấu tiếng Việt cho màn hình nhỏ không hiện được chữ có dấu: "Chào Tân" → "Chao Tan"."""
    import unicodedata

    text = text.replace("đ", "d").replace("Đ", "D")
    text = "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")
    text = "".join(c if c.isascii() else " " for c in text)  # emoji... → khoảng trắng
    return " ".join(text.split())


def _check_device(request: Request) -> None:
    if not config.DEVICE_KEY:
        raise HTTPException(403, "Cổng thiết bị đang tắt (chưa đặt DEVICE_KEY trong .env)")
    key = request.headers.get("x-device-key", "")
    if not secrets.compare_digest(key.encode(), config.DEVICE_KEY.encode()):
        raise HTTPException(401, "Sai khóa thiết bị")


def _device_out(data: dict, khong_dau: int) -> dict:
    if khong_dau and data.get("noi"):
        data = {**data, "noi": bo_dau(data["noi"])}
    return data


@app.post("/api/thiet-bi/chat")
def device_chat(body: ChatIn, request: Request, khong_dau: int = 0):
    """Thiết bị gửi chữ (đã nghe được), nhận {noi, cam_xuc, hanh_dong}. ?khong_dau=1 để bỏ dấu."""
    _check_device(request)
    return _device_out(chat(body), khong_dau)


@app.post("/api/thiet-bi/chao")
def device_greet(request: Request, khong_dau: int = 0):
    """Thiết bị gọi khi vừa bật / thấy người: Bơ chủ động hỏi thăm nếu có chuyện. Không thì {"noi": null}."""
    _check_device(request)
    return _device_out(greet(), khong_dau)
