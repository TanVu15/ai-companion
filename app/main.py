"""Máy chủ web: phục vụ trang chat và nhận tin nhắn gửi tới bộ não."""
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from . import config
from .brain import Brain
from .memory import Memory

app = FastAPI(title="AI Companion")
_brain: Brain | None = None


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
    except Exception as e:  # lỗi mạng, hết tiền API...
        raise HTTPException(502, f"Bộ não gặp lỗi: {type(e).__name__}: {e}")
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
