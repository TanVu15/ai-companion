"""Bộ não: ghép tính cách + trí nhớ + lịch sử chat, hỏi Claude, rồi đọc kết quả JSON."""
import json
import re
from dataclasses import dataclass, field
from datetime import datetime

from . import config

OUTPUT_RULES = f"""
## Cách trả lời (bắt buộc)
Chỉ trả về MỘT đối tượng JSON, không viết gì ngoài JSON:
{{
  "noi": "câu bạn nói với người dùng",
  "cam_xuc": một trong {config.EMOTIONS},
  "hanh_dong": một trong {config.ACTIONS},
  "ghi_nho": ["điều MỚI đáng nhớ về người dùng trong tin nhắn vừa rồi, nếu có"],
  "quen": ["điều trong phần 'Điều bạn đã biết' nay đã sai/lỗi thời, chép y nguyên"],
  "hoi_tham": ["chuyện sắp diễn ra mà lần sau nên hỏi lại, ví dụ 'Chiều nay đi tập chân'"],
  "da_hoi": ["chuyện trong phần 'Chuyện nên hỏi thăm' mà bạn vừa hỏi hoặc người dùng đã kể, chép y nguyên"]
}}
- "noi" ngắn gọn như nhắn tin với bạn bè, thường 1-3 câu.
- "ghi_nho" chỉ ghi điều người dùng tự kể (tên, sở thích, kế hoạch, chuyện đáng nhớ). Không có thì để [].
- Không ghi lại những gì đã có trong phần "Điều bạn đã biết".
- Nếu người dùng kể điều làm một điều cũ không còn đúng (ví dụ chuyển nhà, đổi việc, bỏ sở thích),
  chép điều cũ vào "quen" và ghi điều mới vào "ghi_nho". Không có thì để [].
- "hoi_tham": việc người dùng sắp làm/đang chờ (đi thi, đi khám, tập luyện, hẹn hò, phỏng vấn...),
  ghi ngắn kèm thời điểm nếu có. Không có thì để [].
- Nếu có phần "Chuyện nên hỏi thăm", hãy hỏi thăm TỰ NHIÊN một chuyện khi hợp lúc (không hỏi dồn),
  rồi chép chuyện đó vào "da_hoi". Không có thì để [].
"""


@dataclass
class Reply:
    noi: str
    cam_xuc: str = "binh_thuong"
    hanh_dong: str = "khong"
    ghi_nho: list[str] = field(default_factory=list)
    quen: list[str] = field(default_factory=list)
    hoi_tham: list[str] = field(default_factory=list)
    da_hoi: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"noi": self.noi, "cam_xuc": self.cam_xuc, "hanh_dong": self.hanh_dong}


SUMMARY_PROMPT = """Bạn tóm tắt cuộc trò chuyện giữa người dùng và Bơ (người bạn AI) để Bơ nhớ về sau.
Viết tiếng Việt, tối đa 150 chữ, chỉ giữ ý chính: chuyện người dùng kể, cảm xúc, kế hoạch, lời hứa.
Gộp với bản tóm tắt cũ (nếu có) thành MỘT bản mới. Chỉ trả về đoạn tóm tắt, không thêm gì khác."""

MERGE_PROMPT = """Đây là danh sách những điều Bơ (người bạn AI) nhớ về người dùng, xếp từ cũ đến mới.
Hãy dọn lại: gộp các điều trùng ý thành một, nếu hai điều mâu thuẫn thì giữ điều MỚI hơn (nằm sau),
không bịa thêm gì. Mỗi điều ngắn gọn, tiếng Việt.
Chỉ trả về một mảng JSON các chuỗi, ví dụ: ["Tên là Tân", "Thích tập gym"]."""


GREET_TRIGGER = (
    "(Tin nhắn hệ thống, không phải người dùng nói: người dùng vừa mở ứng dụng sau một thời gian. "
    "Hãy chủ động chào và hỏi thăm một chuyện trong phần 'Chuyện nên hỏi thăm'.)"
)


def _when(created_at: str, now: datetime) -> str:
    """Đổi thời điểm kể chuyện thành chữ dễ hiểu: hôm nay, hôm qua, 3 ngày trước."""
    try:
        days = (now.date() - datetime.fromisoformat(created_at).date()).days
    except ValueError:
        return ""
    return "hôm nay" if days <= 0 else "hôm qua" if days == 1 else f"{days} ngày trước"


def build_system_prompt(
    persona: str,
    facts: list[str],
    summary: str = "",
    followups: list[dict] | None = None,
    now: datetime | None = None,
) -> str:
    now = now or datetime.now()
    known = "\n".join(f"- {f}" for f in facts) if facts else "- (chưa biết gì)"
    out = f"{persona.strip()}\n\nBây giờ là {now.strftime('%H:%M')} ngày {now.strftime('%d/%m/%Y')}.\n"
    out += f"\n## Điều bạn đã biết về người dùng\n{known}\n"
    if summary:
        out += f"\n## Tóm tắt những lần trò chuyện trước\n{summary.strip()}\n"
    if followups:
        items = "\n".join(f"- {f['content']} (kể {_when(f['created_at'], now)})" for f in followups)
        out += f"\n## Chuyện nên hỏi thăm\n{items}\n"
    return out + OUTPUT_RULES


def clean_history(history: list[dict]) -> list[dict]:
    """API yêu cầu tin đầu tiên là của người dùng và hai bên nói xen kẽ nhau."""
    out: list[dict] = []
    for m in history:
        if not out and m["role"] != "user":
            continue
        if out and out[-1]["role"] == m["role"]:
            out[-1] = {"role": m["role"], "content": out[-1]["content"] + "\n" + m["content"]}
        else:
            out.append(dict(m))
    return out


def _str_list(value) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(x) for x in value if isinstance(x, (str, int, float))]


def parse_reply(text: str) -> Reply:
    """Đọc JSON từ câu trả lời. Nếu AI trả sai định dạng thì vẫn dùng được phần chữ."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(0))
            noi = str(data.get("noi", "")).strip()
            if noi:
                cam_xuc = data.get("cam_xuc")
                hanh_dong = data.get("hanh_dong")
                ghi_nho = data.get("ghi_nho") or []
                quen = data.get("quen") or []
                return Reply(
                    noi=noi,
                    cam_xuc=cam_xuc if cam_xuc in config.EMOTIONS else "binh_thuong",
                    hanh_dong=hanh_dong if hanh_dong in config.ACTIONS else "khong",
                    ghi_nho=_str_list(ghi_nho),
                    quen=_str_list(quen),
                    hoi_tham=_str_list(data.get("hoi_tham") or []),
                    da_hoi=_str_list(data.get("da_hoi") or []),
                )
        except json.JSONDecodeError:
            pass
    return Reply(noi=text.strip() or "...")


class Brain:
    def __init__(self, memory, client=None):
        self.memory = memory
        if client is None:
            import anthropic

            client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.client = client
        self._merged_at = 0  # số điều đáng nhớ còn lại sau lần gộp gần nhất

    def persona(self) -> str:
        return config.PERSONA_PATH.read_text(encoding="utf-8")

    def chat(self, user_text: str) -> Reply:
        if self.memory.replies_today() >= config.DAILY_LIMIT:
            return Reply(noi="Hôm nay mình nói nhiều quá rồi, mai nói tiếp nha!", cam_xuc="thuong")
        self.memory.add_message("user", user_text)
        history = clean_history(self.memory.recent_messages(config.HISTORY_LIMIT))
        return self._ask(history, self.memory.pending_followups(config.FOLLOWUP_MIN_HOURS))

    def greet(self) -> Reply | None:
        """Bơ chủ động mở lời khi người dùng quay lại sau một thời gian và có chuyện nên hỏi thăm.
        Không có gì để hỏi hoặc vừa mới nói chuyện xong thì trả về None (không tốn câu API nào)."""
        if self.memory.replies_today() >= config.DAILY_LIMIT:
            return None
        last = self.memory.last_message_time()
        if last and (datetime.now() - last).total_seconds() < config.GREET_AFTER_HOURS * 3600:
            return None
        followups = self.memory.pending_followups(config.FOLLOWUP_MIN_HOURS)
        if not followups:
            return None
        history = clean_history(self.memory.recent_messages(config.HISTORY_LIMIT))
        history.append({"role": "user", "content": GREET_TRIGGER})  # chỉ gửi đi, không lưu
        return self._ask(clean_history(history), followups)

    def _ask(self, history: list[dict], followups: list[dict]) -> Reply:
        summary, _ = self.memory.latest_summary()
        system = build_system_prompt(self.persona(), self.memory.all_facts(), summary, followups)
        resp = self.client.messages.create(
            model=config.MODEL,
            max_tokens=500,
            system=system,
            messages=history,
        )
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        reply = parse_reply(text)

        self.memory.add_message("assistant", reply.noi)
        self.memory.forget_facts(reply.quen)
        self.memory.add_facts(reply.ghi_nho)
        self.memory.done_followups(reply.da_hoi)
        self.memory.add_followups(reply.hoi_tham)
        self.maybe_merge_facts()
        self.maybe_summarize()
        return reply

    def maybe_summarize(self) -> None:
        """Gom tin nhắn cũ thành một đoạn tóm tắt ngắn, để Bơ nhớ chuyện xa mà không tốn nhiều tiền."""
        old = self.memory.messages_to_summarize(config.HISTORY_LIMIT)
        if len(old) < config.SUMMARY_BATCH:
            return
        previous, _ = self.memory.latest_summary()
        lines = "\n".join(f"{'Người dùng' if m['role'] == 'user' else 'Bơ'}: {m['content']}" for m in old)
        prompt = f"Bản tóm tắt cũ:\n{previous or '(chưa có)'}\n\nĐoạn trò chuyện mới:\n{lines}"
        try:
            resp = self.client.messages.create(
                model=config.MODEL,
                max_tokens=400,
                system=SUMMARY_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception:
            return  # tóm tắt lỗi thì lần sau thử lại, không làm hỏng câu trả lời
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
        if text:
            self.memory.add_summary(text, old[-1]["id"])

    def maybe_merge_facts(self) -> None:
        """Danh sách dài thì nhờ AI gộp điều trùng ý, bỏ điều mâu thuẫn cũ. Lỗi thì giữ nguyên."""
        facts = self.memory.all_facts()
        if len(facts) < config.FACTS_MERGE_AT or (self._merged_at and len(facts) < self._merged_at + 10):
            return
        listing = "\n".join(f"- {f}" for f in facts)
        try:
            resp = self.client.messages.create(
                model=config.MODEL,
                max_tokens=800,
                system=MERGE_PROMPT,
                messages=[{"role": "user", "content": listing}],
            )
            text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
            match = re.search(r"\[.*\]", text, re.DOTALL)
            merged = [str(x).strip() for x in json.loads(match.group(0)) if str(x).strip()] if match else []
        except Exception:
            merged = []
        # Chỉ nhận kết quả hợp lý: không rỗng và không dài hơn danh sách cũ
        if merged and len(merged) <= len(facts):
            self.memory.replace_facts(merged)
            self._merged_at = len(self.memory.all_facts())
        else:
            self._merged_at = len(facts)  # chờ thêm 10 điều mới rồi mới thử lại
