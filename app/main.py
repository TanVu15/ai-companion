"""Máy chủ web: phục vụ trang chat và nhận tin nhắn gửi tới bộ não."""
import base64
import json
import secrets

from fastapi import Body, FastAPI, HTTPException, Request
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


# Lệnh làm thay đổi dữ liệu phải có header "X-Bo: 1". Trang web lạ không tự gắn được header này
# (trình duyệt chặn), nên không thể lén xóa trí nhớ hay tiêu tiền API của Tân.
_CHANGES_DATA_GET = {"/api/nhac"}  # GET nhưng có đánh dấu "đã nhắc"


@app.middleware("http")
async def require_password(request: Request, call_next):
    if request.url.path.startswith("/api/thiet-bi/"):
        return await call_next(request)  # thiết bị dùng khóa riêng (DEVICE_KEY), kiểm tra bên dưới
    changes = request.method not in ("GET", "HEAD", "OPTIONS") or request.url.path in _CHANGES_DATA_GET
    if changes and request.headers.get("x-bo") != "1":
        return Response("Thiếu header X-Bo", status_code=403, media_type="text/plain; charset=utf-8")
    if config.APP_PASSWORD and not _password_ok(request.headers.get("authorization", "")):
        return Response(
            "Cần mật khẩu để nói chuyện với Bơ.",
            status_code=401,
            headers={"WWW-Authenticate": 'Basic realm="Bo", charset="UTF-8"'},
            media_type="text/plain; charset=utf-8",
        )
    response = await call_next(request)
    if request.url.path.startswith("/web/") or request.url.path == "/":
        response.headers["Cache-Control"] = "no-cache"  # git pull xong mở lại là thấy bản mới ngay
    return response


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
            _brain = Brain(Memory(config.DB_PATH.with_name("demo.db")), client=_DemoClient(), background=True)
            return _brain
        if not config.ANTHROPIC_API_KEY:
            raise HTTPException(500, "Chưa có ANTHROPIC_API_KEY trong file .env")
        _brain = Brain(Memory(config.DB_PATH), background=True)
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
    out["ngan_sach_thang"] = config.MONTHLY_USD_LIMIT
    out["da_tra_loi_hom_nay"] = mem.replies_today()
    return out


@app.get("/api/sao-luu")
def backup():
    """Tải toàn bộ trí nhớ về máy thành file JSON."""
    from datetime import date

    body = json.dumps(get_brain().memory.export_all(), ensure_ascii=False, indent=1)
    name = f"bo-sao-luu-{date.today().isoformat()}.json"
    return Response(body, media_type="application/json",
                    headers={"Content-Disposition": f'attachment; filename="{name}"'})


@app.post("/api/khoi-phuc")
def restore(data: dict = Body(...)):
    """Nạp lại file sao lưu (thay toàn bộ trí nhớ hiện tại). Chỉ nhận Content-Type: application/json."""
    brain = get_brain()
    try:
        with brain._lock:  # không cho tin nhắn/lời nhắc ghi xen vào giữa lúc đang nạp
            brain.memory.import_all(data)
    except (ValueError, UnicodeDecodeError) as e:
        raise HTTPException(400, str(e) if "Bơ" in str(e) or "hỏng" in str(e) else "File không đọc được")
    return {"ok": True}


@app.get("/api/suc-khoe")
def health():
    """Kiểm tra cấu hình: thiếu gì thì báo bằng câu dễ hiểu. Không gọi API, không tốn tiền."""
    checks = []

    def add(ten: str, ok: bool, ghi_chu: str, muc: str = "loi"):
        checks.append({"ten": ten, "ok": ok, "muc": "ok" if ok else muc, "ghi_chu": ghi_chu})

    if config.DEMO:
        add("Bộ não", True, "Đang chạy DEMO (không cần API key, Bơ chỉ nhắc lại lời bạn)")
    else:
        key = config.ANTHROPIC_API_KEY
        add("API key", key.startswith("sk-"),
            "Có API key" if key.startswith("sk-") else
            ("Chưa có ANTHROPIC_API_KEY trong .env" if not key else "API key trông không đúng (thường bắt đầu bằng sk-)"))
    try:
        persona_ok = bool(config.PERSONA_PATH.read_text(encoding="utf-8").strip())
    except OSError:
        persona_ok = False
    add("Tính cách", persona_ok, "Có persona.md" if persona_ok else "Thiếu hoặc trống file persona.md")
    db = config.DB_PATH.with_name("demo.db") if config.DEMO else config.DB_PATH
    try:
        db.parent.mkdir(parents=True, exist_ok=True)
        probe = db.parent / ".thu_ghi"
        probe.write_text("ok")
        probe.unlink()
        size = db.stat().st_size / 1e6 if db.exists() else 0
        add("Dữ liệu", True, f"Ghi được vào {db.parent.name}/, trí nhớ nặng {size:.1f} MB")
    except OSError as e:
        add("Dữ liệu", False, f"Không ghi được thư mục dữ liệu: {e}")
    add("Mật khẩu web", bool(config.APP_PASSWORD),
        "Đã đặt APP_PASSWORD" if config.APP_PASSWORD else "Chưa đặt APP_PASSWORD (ổn nếu chỉ dùng trong nhà)", "canh_bao")
    add("Ngân sách tháng", config.MONTHLY_USD_LIMIT > 0,
        f"{config.MONTHLY_USD_LIMIT:g} đô/tháng" if config.MONTHLY_USD_LIMIT > 0 else "Không giới hạn (đặt MONTHLY_USD_LIMIT)",
        "canh_bao")
    return {"ok": all(c["muc"] != "loi" for c in checks), "model": config.MODEL, "kiem_tra": checks}


@app.get("/api/nhac")
def reminders_due():
    """Web gọi mỗi 30 giây: trả các lời nhắc vừa tới giờ (mỗi cái chỉ trả một lần)."""
    return [r.to_dict() for r in get_brain().due_reminders()]


@app.get("/api/nhac/sap-toi")
def reminders_upcoming():
    return get_brain().memory.upcoming_reminders()


@app.delete("/api/nhac/{reminder_id}")
def reminder_delete(reminder_id: int):
    get_brain().memory.delete_reminder(reminder_id)
    return {"ok": True}


@app.get("/api/history")
def history(before_id: int | None = None, limit: int = 50):
    """Tin nhắn gần nhất (kèm giờ). Gửi before_id để lấy thêm tin cũ hơn."""
    return get_brain().memory.history_page(min(max(limit, 1), 200), before_id)


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


@app.get("/api/thiet-bi/nhac")
def device_reminders(request: Request, khong_dau: int = 0):
    """Thiết bị hỏi định kỳ: có lời nhắc nào tới giờ không."""
    _check_device(request)
    return [_device_out(r, khong_dau) for r in reminders_due()]
