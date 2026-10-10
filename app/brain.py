"""Bộ não: ghép tính cách + trí nhớ + lịch sử chat, hỏi Claude, rồi đọc kết quả JSON."""
import json
import re
from dataclasses import dataclass, field

from . import config

OUTPUT_RULES = f"""
## Cách trả lời (bắt buộc)
Chỉ trả về MỘT đối tượng JSON, không viết gì ngoài JSON:
{{
  "noi": "câu bạn nói với người dùng",
  "cam_xuc": một trong {config.EMOTIONS},
  "hanh_dong": một trong {config.ACTIONS},
  "ghi_nho": ["điều MỚI đáng nhớ về người dùng trong tin nhắn vừa rồi, nếu có"]
}}
- "noi" ngắn gọn như nhắn tin với bạn bè, thường 1-3 câu.
- "ghi_nho" chỉ ghi điều người dùng tự kể (tên, sở thích, kế hoạch, chuyện đáng nhớ). Không có thì để [].
- Không ghi lại những gì đã có trong phần "Điều bạn đã biết".
"""


@dataclass
class Reply:
    noi: str
    cam_xuc: str = "binh_thuong"
    hanh_dong: str = "khong"
    ghi_nho: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"noi": self.noi, "cam_xuc": self.cam_xuc, "hanh_dong": self.hanh_dong}


def build_system_prompt(persona: str, facts: list[str]) -> str:
    known = "\n".join(f"- {f}" for f in facts) if facts else "- (chưa biết gì)"
    return f"{persona.strip()}\n\n## Điều bạn đã biết về người dùng\n{known}\n{OUTPUT_RULES}"


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
                return Reply(
                    noi=noi,
                    cam_xuc=cam_xuc if cam_xuc in config.EMOTIONS else "binh_thuong",
                    hanh_dong=hanh_dong if hanh_dong in config.ACTIONS else "khong",
                    ghi_nho=[str(x) for x in ghi_nho if isinstance(x, (str, int, float))],
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

    def persona(self) -> str:
        return config.PERSONA_PATH.read_text(encoding="utf-8")

    def chat(self, user_text: str) -> Reply:
        if self.memory.replies_today() >= config.DAILY_LIMIT:
            return Reply(noi="Hôm nay mình nói nhiều quá rồi, mai nói tiếp nha!", cam_xuc="thuong")

        self.memory.add_message("user", user_text)
        history = clean_history(self.memory.recent_messages(config.HISTORY_LIMIT))
        system = build_system_prompt(self.persona(), self.memory.all_facts())

        resp = self.client.messages.create(
            model=config.MODEL,
            max_tokens=500,
            system=system,
            messages=history,
        )
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        reply = parse_reply(text)

        self.memory.add_message("assistant", reply.noi)
        self.memory.add_facts(reply.ghi_nho)
        return reply
