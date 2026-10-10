"""Máy chủ web: phục vụ trang chat và nhận tin nhắn gửi tới bộ não."""
import base64
import json
import os
import secrets

from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import cai_dat, config
from .brain import Brain, cost_usd, current_persona, friendly_error
from .memory import Memory
from .nhat_ky import bat_ghi_file, log

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
            ("vui", "vay_tay", "vui"), ("hao_hung", "nhay", "vui"), ("suy_nghi", "nghieng_dau", "binh_thuong"),
            ("ngac_nhien", "khong", "binh_thuong"), ("thuong", "gat_dau", "met"), ("buon", "lac_dau", "buon"),
        ])
        self._json = json
        self.messages = SimpleNamespace(create=self._create)

    def _create(self, messages, **_):
        emo, act, mood = next(self._cycle)
        last = messages[-1]["content"]
        text = self._json.dumps({"noi": f"(demo) Bạn vừa nói: {last}", "cam_xuc": emo, "hanh_dong": act, "tam_trang": mood})
        return self._ns(content=[self._ns(type="text", text=text)])


def _weather():
    if not config.THANH_PHO:
        return None
    from .thoi_tiet import ThoiTiet

    return ThoiTiet(config.THANH_PHO)


def get_brain() -> Brain:
    global _brain
    if _brain is None:
        bat_ghi_file(config.DB_PATH.parent / "loi.log")
        cai_dat.ap_dung()  # cài đặt chỉnh trên web (thành phố, giờ yên lặng...) ưu tiên hơn .env
        if config.DEMO:
            _brain = Brain(Memory(config.DB_PATH.with_name("demo.db")), client=_DemoClient(), background=True,
                           weather=_weather())
            return _brain
        if not config.ANTHROPIC_API_KEY:
            raise HTTPException(500, "Chưa có ANTHROPIC_API_KEY trong file .env")
        _brain = Brain(Memory(config.DB_PATH), background=True, weather=_weather())
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
        log.exception("Trả lời lỗi: %s", friendly_error(e))
        raise HTTPException(502, friendly_error(e))
    # id: để web ghim được tin vừa nói (giao diện khác bỏ qua cũng không sao)
    return {**reply.to_dict(), "id": reply.msg_id, "id_nguoi_dung": reply.user_msg_id}


@app.post("/api/chao")
def greet(chi_dip: int = 0):
    """Gọi khi mở web: Bơ chủ động hỏi thăm chuyện cũ nếu có. Không có thì trả {"noi": null}."""
    try:
        reply = get_brain().greet(only_occasion=bool(chi_dip))
    except HTTPException:
        raise
    except Exception as e:
        log.warning("Mở lời lỗi: %s", type(e).__name__)
        reply = None  # mở lời không được thì thôi, không báo lỗi làm phiền
    return {**reply.to_dict(), "id": reply.msg_id} if reply else {"noi": None}


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
    # Theo loại (tháng này) và theo ngày (7 ngày gần nhất, kể cả ngày không dùng)
    from datetime import timedelta

    rows = mem.usage_rows_since(min(today.replace(day=1), today - timedelta(days=6)).isoformat())
    loai: dict = {}
    for r in rows:
        if r["day"] >= today.replace(day=1).isoformat():
            x = loai.setdefault(r["kind"], {"calls": 0, "input_tokens": 0, "output_tokens": 0})
            for k in x:
                x[k] += r[k]
    out["theo_loai"] = {k: {**v, "usd": round(cost_usd(v), 4)} for k, v in loai.items()}
    days = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
    out["bay_ngay"] = []
    for d in days:
        u = {"calls": 0, "input_tokens": 0, "output_tokens": 0}
        for r in rows:
            if r["day"] == d:
                for k in u:
                    u[k] += r[k]
        out["bay_ngay"].append({"ngay": d, "calls": u["calls"], "usd": round(cost_usd(u), 4)})
    out["gioi_han_ngay"] = config.DAILY_LIMIT
    out["ngan_sach_thang"] = config.MONTHLY_USD_LIMIT
    out["da_tra_loi_hom_nay"] = mem.replies_today()
    return out


@app.get("/api/sao-luu")
def backup():
    """Tải toàn bộ trí nhớ về máy thành file JSON."""
    from datetime import date

    brain = get_brain()
    with brain._lock:  # không sao lưu giữa lúc đang nạp bản khác (sẽ ra file dở dang)
        data = brain.memory.export_all()
    body = json.dumps(data, ensure_ascii=False, indent=1)
    name = f"bo-sao-luu-{date.today().isoformat()}.json"
    return Response(body, media_type="application/json",
                    headers={"Content-Disposition": f'attachment; filename="{name}"'})


@app.get("/api/tai-chat")
def download_chat():
    """Tải toàn bộ trò chuyện về thành file chữ (.txt) để đọc lại."""
    from datetime import date

    name = f"bo-tro-chuyen-{date.today().isoformat()}.txt"
    brain = get_brain()
    with brain._lock:  # không đọc giữa lúc đang nạp sao lưu
        body = "\ufeff" + brain.memory.chat_as_text()  # BOM để Notepad cũ hiện đúng tiếng Việt
    return Response(body, media_type="text/plain; charset=utf-8",
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
        text, custom = current_persona()
        persona_ok = bool(text.strip())
    except OSError:
        persona_ok, custom = False, False
    add("Tính cách", persona_ok,
        (f"Đang dùng bản tự sửa trên web ({config.PERSONA_CUSTOM_PATH.name})" if custom else "Đang dùng persona.md mặc định")
        if persona_ok else "Thiếu hoặc trống file persona.md")
    if config.THANH_PHO:
        w = _brain.weather if _brain is not None else None
        if w is not None and w.loi:
            add("Thời tiết", False, f"{config.THANH_PHO}: không lấy được ({w.loi})", "canh_bao")
        else:
            add("Thời tiết", True, (w.da_lay() if w is not None else None)
                or f"{config.THANH_PHO} (sẽ lấy khi bạn nhắn tin)")
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
    return {"ok": all(c["muc"] != "loi" for c in checks), "model": config.MODEL, "kiem_tra": checks,
            "gio_yen_lang": config.GIO_YEN_LANG}


@app.get("/api/nhac")
def reminders_due():
    """Web gọi mỗi 30 giây: trả các lời nhắc vừa tới giờ (mỗi cái chỉ trả một lần)."""
    return [{**r.to_dict(), "viec": r.viec_nhac, "id": r.msg_id} for r in get_brain().due_reminders()]


class SnoozeIn(BaseModel):
    viec: str
    phut: int = 10


@app.post("/api/nhac/hoan")
def reminder_snooze(body: SnoozeIn):
    """Nút "Nhắc lại sau 10 phút" dưới lời nhắc."""
    viec = body.viec.strip()[:300]
    if not viec or not 1 <= body.phut <= 24 * 60:
        raise HTTPException(400, "Lời nhắc không hợp lệ")
    return {"luc": get_brain().snooze(viec, body.phut)}


@app.get("/api/nhac/sap-toi")
def reminders_upcoming():
    return get_brain().memory.upcoming_reminders()


class ReminderEditIn(BaseModel):
    viec: str
    luc: str  # "YYYY-MM-DD HH:MM" (hoặc "YYYY-MM-DDTHH:MM" từ ô chọn giờ của trình duyệt)
    lap: str = ""


@app.put("/api/nhac/{reminder_id}")
def reminder_edit(reminder_id: int, body: ReminderEditIn):
    brain = get_brain()
    with brain._lock:
        try:
            ok = brain.memory.update_reminder(reminder_id, body.viec, body.luc, body.lap)
        except ValueError as e:
            raise HTTPException(400, str(e))
    if not ok:
        raise HTTPException(404, "Lời nhắc này đã nhắc xong hoặc bị xóa rồi")
    return {"ok": True}


@app.delete("/api/nhac/{reminder_id}")
def reminder_delete(reminder_id: int):
    brain = get_brain()
    with brain._lock:
        brain.memory.delete_reminder(reminder_id)
    return {"ok": True}


@app.get("/api/history")
def history(before_id: int | None = None, limit: int = 50):
    """Tin nhắn gần nhất (kèm giờ). Gửi before_id để lấy thêm tin cũ hơn.
    Cố ý không chờ khóa: mở web không phải đợi Bơ trả lời xong tin của máy khác."""
    return get_brain().memory.history_page(min(max(limit, 1), 200), before_id)


class PinIn(BaseModel):
    ghim: bool = True


@app.get("/api/thong-ke")
def stats():
    brain = get_brain()
    with brain._lock:
        return brain.memory.stats()


def _hom_nay() -> dict:
    """Thứ, ngày dương, ngày âm, ngày lễ hôm nay (tính offline, không tốn API)."""
    from datetime import date

    from .am_lich import duong_sang_am, ngay_le, ten_nam
    from .brain import THU

    d = date.today()
    ngay, thang, nam, nhuan = duong_sang_am(d)
    return {
        "thu": THU[d.weekday()],
        "duong": d.strftime("%d/%m/%Y"),
        "am": f"{ngay}/{thang}{' nhuận' if nhuan else ''}",
        "nam_am": ten_nam(nam),
        "le": ngay_le(d),
    }


@app.get("/api/hom-nay")
def today_info():
    return _hom_nay()


@app.get("/api/cai-dat")
def settings():
    """Cài đặt đang dùng + những mục đã chỉnh trên web (khác .env)."""
    get_brain()
    return {"hien_tai": cai_dat.hien_tai(), "da_chinh": sorted(cai_dat.doc())}


def _after_settings(old_city: str) -> dict:
    brain = get_brain()
    if config.THANH_PHO != old_city:  # đổi thành phố → tạo lại bộ lấy thời tiết
        brain.weather = _weather()
        brain._weather_text = None
    return {"hien_tai": cai_dat.ap_dung(), "da_chinh": sorted(cai_dat.doc())}


@app.put("/api/cai-dat")
def settings_save(body: dict):
    brain = get_brain()
    with brain._lock:
        old_city = config.THANH_PHO
        try:
            cai_dat.luu(body)
        except ValueError as e:
            raise HTTPException(400, str(e))
        except OSError as e:
            log.warning("Lưu cài đặt lỗi: %s", e)
            raise HTTPException(500, "Không lưu được cài đặt (thử lại sau giây lát)")
        return _after_settings(old_city)


@app.delete("/api/cai-dat")
def settings_reset():
    brain = get_brain()
    with brain._lock:
        old_city = config.THANH_PHO
        try:
            cai_dat.ve_mac_dinh()
        except OSError as e:
            raise HTTPException(500, f"Không xóa được cài đặt: {e}")
        return _after_settings(old_city)


@app.get("/api/tam-trang")
def moods(days: int = 7):
    """Tâm trạng nổi bật của người dùng từng ngày (cũ → mới), để vẽ dải "Tâm trạng 7 ngày"."""
    brain = get_brain()
    with brain._lock:
        return brain.memory.moods_by_day(min(max(days, 1), 31))


class TodoIn(BaseModel):
    viec: str


class TodoDoneIn(BaseModel):
    xong: bool = True


@app.get("/api/viec")
def todos():
    """Việc cần làm: chưa xong trước, rồi việc vừa xong trong 3 ngày."""
    brain = get_brain()
    with brain._lock:
        return brain.memory.todos()


@app.post("/api/viec")
def add_todo(body: TodoIn):
    text = body.viec.strip()[:200]
    if not text:
        raise HTTPException(400, "Việc cần làm đang trống")
    brain = get_brain()
    with brain._lock:
        if len(brain.memory.todos(include_done=False)) >= brain.memory.TODO_MAX:
            raise HTTPException(400, f"Danh sách đã đủ {brain.memory.TODO_MAX} việc chưa xong, gạch bớt nha")
        if not brain.memory.add_todos([text]):
            raise HTTPException(400, "Việc này đã có trong danh sách rồi")
    return {"ok": True}


@app.put("/api/viec/{todo_id}")
def done_todo(todo_id: int, body: TodoDoneIn):
    brain = get_brain()
    with brain._lock:
        try:
            ok = brain.memory.set_todo_done(todo_id, body.xong)
        except ValueError as e:
            raise HTTPException(409, str(e))
        if not ok:
            raise HTTPException(404, "Không có việc này")
    return {"ok": True}


@app.delete("/api/viec/{todo_id}")
def delete_todo(todo_id: int):
    brain = get_brain()
    with brain._lock:
        brain.memory.delete_todo(todo_id)
    return {"ok": True}


@app.get("/api/ghim")
def pinned():
    brain = get_brain()
    with brain._lock:
        return brain.memory.pinned_messages()


@app.post("/api/ghim/{msg_id}")
def pin(msg_id: int, body: PinIn):
    brain = get_brain()
    with brain._lock:
        if not brain.memory.set_pinned(msg_id, body.ghim):
            raise HTTPException(404, "Không thấy tin nhắn này")
    return {"ok": True}


@app.get("/api/ngay-dac-biet")
def special_days():
    return get_brain().memory.special_days()


@app.delete("/api/ngay-dac-biet/{day_id}")
def special_day_delete(day_id: int):
    brain = get_brain()
    with brain._lock:
        brain.memory.delete_special_day(day_id)
    return {"ok": True}


class PersonaIn(BaseModel):
    noi_dung: str


@app.get("/api/tinh-cach")
def persona_get():
    try:
        text, custom = current_persona()
    except OSError:
        text, custom = "", False
    return {"noi_dung": text, "tu_sua": custom}


@app.put("/api/tinh-cach")
def persona_put(body: PersonaIn):
    """Lưu tính cách Tân tự sửa. Áp dụng ngay từ tin nhắn sau."""
    text = body.noi_dung.replace("\r\n", "\n").strip()
    if len(text) < 20:
        raise HTTPException(400, "Tính cách ngắn quá, viết thêm vài dòng nha")
    if len(text) > 20000:
        raise HTTPException(400, "Tính cách dài quá (tối đa 20.000 ký tự) — dài thì tốn tiền API mỗi câu")
    path = config.PERSONA_CUSTOM_PATH
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        _backup_persona()
        tmp = path.with_suffix(".tmp")
        tmp.write_text(text + "\n", encoding="utf-8")
        os.replace(tmp, path)  # thay một phát: không có lúc nào file trống/thiếu
    except OSError as e:
        log.warning("Lưu tính cách lỗi: %s", e)
        raise HTTPException(500, "Không lưu được file tính cách (thử lại sau giây lát)")
    return {"ok": True}


def _backup_persona() -> None:
    """Chép bản tự sửa hiện tại ra file có giờ (persona_tu_sua.20261010-200501.md), giữ 10 bản gần nhất."""
    import shutil
    from datetime import datetime

    path = config.PERSONA_CUSTOM_PATH
    if not path.exists() or path.resolve() == config.PERSONA_PATH.resolve():
        return
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    shutil.copy2(path, path.with_name(f"{path.stem}.{stamp}.md"))
    olds = sorted(path.parent.glob(f"{path.stem}.*.md"))
    for old in olds[:-10]:
        old.unlink(missing_ok=True)


@app.delete("/api/tinh-cach")
def persona_reset():
    """Về tính cách mặc định (persona.md trong dự án)."""
    path = config.PERSONA_CUSTOM_PATH
    if path.resolve() == config.PERSONA_PATH.resolve():
        raise HTTPException(400, "Không xóa file tính cách gốc")
    try:
        _backup_persona()
        path.unlink(missing_ok=True)
    except OSError as e:
        log.warning("Về tính cách mặc định lỗi: %s", e)
        raise HTTPException(500, "Không xóa được bản tự sửa (thử lại sau giây lát)")
    return {"ok": True}


@app.get("/api/tim")
def search(q: str = "", limit: int = 30):
    """Tìm trong lịch sử trò chuyện (gõ không dấu vẫn được). Mới nhất trước."""
    brain = get_brain()
    with brain._lock:
        return brain.memory.search_messages(q[:100], min(max(limit, 1), 100))


@app.get("/api/facts")
def facts():
    return get_brain().memory.all_facts()


class FactEditIn(BaseModel):
    cu: str
    moi: str


@app.post("/api/facts")
def add_fact(body: FactIn):
    """Tân tự thêm một điều cho Bơ nhớ."""
    text = body.content.strip()[:300]
    if not text:
        raise HTTPException(400, "Điều cần nhớ đang trống")
    brain = get_brain()
    with brain._lock:
        brain.memory.add_facts([text])
    return {"ok": True}


@app.put("/api/facts")
def edit_fact(body: FactEditIn):
    brain = get_brain()
    with brain._lock:
        if not brain.memory.update_fact(body.cu, body.moi[:300]):
            raise HTTPException(400, "Không sửa được (trống, trùng điều khác, hoặc điều cũ đã bị xóa)")
    return {"ok": True}


@app.delete("/api/facts/all")
def clear_facts():
    brain = get_brain()
    with brain._lock:  # chờ việc gộp trí nhớ đang chạy (nếu có) xong, để điều đã xóa không quay lại
        brain.memory.clear_facts()
    return {"ok": True}


@app.delete("/api/facts")
def delete_fact(body: FactIn):
    brain = get_brain()
    with brain._lock:
        brain.memory.delete_fact(body.content)
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
    if khong_dau:
        data = {**data, **{k: bo_dau(data[k]) for k in ("noi", "viec") if data.get(k)}}
    return data


@app.post("/api/thiet-bi/chat")
def device_chat(body: ChatIn, request: Request, khong_dau: int = 0):
    """Thiết bị gửi chữ (đã nghe được), nhận {noi, cam_xuc, hanh_dong}. ?khong_dau=1 để bỏ dấu."""
    _check_device(request)
    data = {k: v for k, v in chat(body).items() if k in ("noi", "cam_xuc", "hanh_dong")}  # thiết bị chỉ cần gọn
    return _device_out(data, khong_dau)


@app.post("/api/thiet-bi/chao")
def device_greet(request: Request, khong_dau: int = 0):
    """Thiết bị gọi khi vừa bật / thấy người: Bơ chủ động hỏi thăm nếu có chuyện. Không thì {"noi": null}."""
    _check_device(request)
    data = {k: v for k, v in greet().items() if k in ("noi", "cam_xuc", "hanh_dong")}
    return _device_out(data, khong_dau)


@app.get("/api/thiet-bi/nhac")
def device_reminders(request: Request, khong_dau: int = 0):
    """Thiết bị hỏi định kỳ: có lời nhắc nào tới giờ không."""
    _check_device(request)
    return [_device_out({k: v for k, v in r.items() if k != "id"}, khong_dau) for r in reminders_due()]


@app.get("/api/thiet-bi/viec")
def device_todos(request: Request, khong_dau: int = 0):
    """Việc cần làm chưa xong (cũ → mới), để màn hình nhỏ hiện danh sách: [{"viec": "Mua sữa"}]."""
    _check_device(request)
    brain = get_brain()
    with brain._lock:
        items = brain.memory.todos(include_done=False)
    return [_device_out({"viec": t["viec"]}, khong_dau) for t in items]


@app.get("/api/thiet-bi/hom-nay")
def device_today(request: Request, khong_dau: int = 0):
    """Cho màn hình đồng hồ: {"thu", "duong", "am", "nam_am", "le": [...]}. ?khong_dau=1 để bỏ dấu."""
    _check_device(request)
    d = _hom_nay()
    if khong_dau:
        d = {k: ([bo_dau(x) for x in v] if isinstance(v, list) else bo_dau(v)) for k, v in d.items()}
    return d
