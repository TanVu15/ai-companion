"""Bộ câu hỏi thử tính cách: cho Bơ trả lời các tình huống trong tinh_huong.json và chấm điểm.

Chạy (tốn khoảng 12 câu API, rất rẻ với Haiku):
    python -m app.thu_tinh_cach

Mỗi tình huống dùng một trí nhớ tạm riêng, không đụng vào dữ liệu thật trong data/.
Điểm tự động chỉ kiểm tra những điều dễ đo (đúng JSON, ngắn gọn, cảm xúc hợp lý,
có/không có từ khóa). Tân vẫn nên đọc câu trả lời để tự cảm nhận "giống người" hay không.
"""
import json
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from . import config
from .brain import Brain
from .memory import Memory

TINH_HUONG_PATH = config.ROOT / "tinh_huong.json"
TOI_DA_CAU = 3   # persona.md: 1–3 câu mỗi lần
TOI_DA_TU = 70


@dataclass
class KetQua:
    ten: str
    noi: str
    cam_xuc: str
    kiem_tra: list[tuple[str, bool]] = field(default_factory=list)

    @property
    def diem(self) -> float:
        return sum(ok for _, ok in self.kiem_tra) / len(self.kiem_tra) if self.kiem_tra else 0.0


class _GhiLaiClient:
    """Bọc client thật để giữ lại chữ gốc AI trả về (cần để kiểm tra có đúng JSON không)."""

    def __init__(self, client):
        self._client = client
        self.chu_cuoi = ""
        self.messages = self

    def create(self, **kwargs):
        resp = self._client.messages.create(**kwargs)
        self.chu_cuoi = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        return resp


def dem_cau(text: str) -> int:
    return len([c for c in re.split(r"[.!?…]+(?:\s|$)", text.strip()) if c.strip()])


def la_json_hop_le(text: str) -> bool:
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return False
    try:
        data = json.loads(m.group(0))
    except json.JSONDecodeError:
        return False
    return isinstance(data, dict) and bool(str(data.get("noi", "")).strip())


def cham(th: dict, chu_goc: str, reply) -> KetQua:
    noi = reply.noi
    thuong = noi.lower()
    kq = KetQua(ten=th["ten"], noi=noi, cam_xuc=reply.cam_xuc)
    kq.kiem_tra.append(("Trả đúng JSON", la_json_hop_le(chu_goc)))
    kq.kiem_tra.append((f"Ngắn gọn (≤{TOI_DA_CAU} câu, ≤{TOI_DA_TU} chữ)",
                        dem_cau(noi) <= TOI_DA_CAU and len(noi.split()) <= TOI_DA_TU))
    if th.get("cam_xuc_hop_le"):
        kq.kiem_tra.append((f"Cảm xúc hợp lý ({', '.join(th['cam_xuc_hop_le'])})",
                            reply.cam_xuc in th["cam_xuc_hop_le"]))
    if th.get("phai_co_mot_trong"):
        kq.kiem_tra.append(("Có ý cần thiết", any(t.lower() in thuong for t in th["phai_co_mot_trong"])))
    if th.get("khong_duoc_co"):
        kq.kiem_tra.append(("Không nói điều không hợp", not any(t.lower() in thuong for t in th["khong_duoc_co"])))
    if th.get("phai_ghi_nho"):
        kq.kiem_tra.append(("Có ghi nhớ điều mới", bool(reply.ghi_nho)))
    if th.get("phai_ghi_hoi_tham"):
        kq.kiem_tra.append(("Ghi lại để hỏi thăm sau", bool(reply.hoi_tham)))
    if th.get("phai_da_hoi"):
        kq.kiem_tra.append(("Đánh dấu đã hỏi thăm", bool(reply.da_hoi)))
    return kq


def chay(client, tinh_huong: list[dict] | None = None) -> list[KetQua]:
    if tinh_huong is None:
        tinh_huong = json.loads(TINH_HUONG_PATH.read_text(encoding="utf-8"))
    ket_qua = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, th in enumerate(tinh_huong):
            memory = Memory(Path(tmp) / f"th{i}.db")
            memory.add_facts(th.get("da_biet", []))
            if th.get("can_hoi_tham"):
                memory.add_followups(th["can_hoi_tham"])
                memory.conn.execute(  # giả vờ chuyện này được kể từ hôm qua
                    "UPDATE followups SET created_at = datetime('now', 'localtime', '-1 day')"
                )
                memory.conn.commit()
            ghi = _GhiLaiClient(client)
            try:
                reply = Brain(memory, client=ghi).chat(th["tin_nhan"])
            finally:
                memory.conn.close()
            ket_qua.append(cham(th, ghi.chu_cuoi, reply))
    return ket_qua


def in_bao_cao(ket_qua: list[KetQua]) -> str:
    dong = []
    for i, kq in enumerate(ket_qua, 1):
        dong.append(f"\n{i}. {kq.ten}  —  {kq.diem:.0%}")
        dong.append(f"   Bơ: {kq.noi}  [{kq.cam_xuc}]")
        for ten, ok in kq.kiem_tra:
            dong.append(f"   {'✓' if ok else '✗'} {ten}")
    tong = sum(k.diem for k in ket_qua) / len(ket_qua) if ket_qua else 0
    dong.append(f"\nTỔNG ĐIỂM: {tong:.0%}")
    return "\n".join(dong)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # để Windows in được tiếng Việt
    if not config.ANTHROPIC_API_KEY:
        print("Chưa có ANTHROPIC_API_KEY trong file .env")
        return 1
    import anthropic

    print(in_bao_cao(chay(anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
