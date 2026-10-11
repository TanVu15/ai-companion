"""Bộ câu hỏi thử tính cách: cho Bơ trả lời các tình huống trong tinh_huong.json và chấm điểm.

Chạy (tốn khoảng 20 câu API, rất rẻ với Haiku):
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


def cham(th: dict, chu_goc: str, reply, viec_con_lai: int = 0) -> KetQua:
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
    if th.get("phai_ghi_ngay_dac_biet"):
        kq.kiem_tra.append(("Ghi ngày đặc biệt", any(str(d.get("ngay", "")).strip() for d in reply.ngay_dac_biet)))
    if th.get("phai_nhac_lap"):
        kq.kiem_tra.append((f"Nhắc lặp lại ({th['phai_nhac_lap']})",
                            any(str(x.get("lap", "")) == th["phai_nhac_lap"] for x in reply.nhac)))
    if th.get("phai_ghi_ngay_am"):
        kq.kiem_tra.append(("Ghi đúng là ngày âm lịch",
                            any(d.get("am_lich") in (True, "true") for d in reply.ngay_dac_biet)))
    if th.get("phai_noi_ngay_am"):
        from datetime import date

        from .am_lich import duong_sang_am

        ngay, thang, _, _ = duong_sang_am(date.today())
        kq.kiem_tra.append(("Nói đúng ngày âm hôm nay",
                            any(t in thuong for t in (f"{ngay}/{thang}", f"{ngay} tháng {thang}"))))
    if th.get("phai_ghi_viec"):
        kq.kiem_tra.append(("Ghi vào việc cần làm", bool(reply.viec_can_lam)))
    if th.get("phai_xong_viec"):
        kq.kiem_tra.append(("Gạch việc đã xong", bool(reply.xong_viec) and viec_con_lai == 0))
    if th.get("phai_thoi_quen_moi"):
        kq.kiem_tra.append(("Thêm thói quen để theo dõi", bool(reply.thoi_quen_moi)))
    if th.get("phai_huy_nhac"):
        kq.kiem_tra.append((f"Bỏ đúng lời nhắc ({th['phai_huy_nhac']})", getattr(reply, "huy_nhac_dung", False)))
    if th.get("phai_tich_hom_qua"):
        kq.kiem_tra.append(("Tích thói quen vào hôm qua (không phải hôm nay)", getattr(reply, "tich_hom_qua_dung", False)))
    if th.get("phai_ghi_nhat_ky"):
        kq.kiem_tra.append(("Ghi nhật ký", bool(reply.nhat_ky)))
    if th.get("khong_ghi_nhat_ky"):
        kq.kiem_tra.append(("Không ghi nhật ký chuyện vặt", not reply.nhat_ky))
    if th.get("phai_tam_trang"):
        kq.kiem_tra.append((f"Đoán đúng tâm trạng ({', '.join(th['phai_tam_trang'])})",
                            reply.tam_trang in th["phai_tam_trang"]))
    return kq


def chay(client, tinh_huong: list[dict] | None = None) -> list[KetQua]:
    if tinh_huong is None:
        tinh_huong = json.loads(TINH_HUONG_PATH.read_text(encoding="utf-8"))
    ket_qua = []
    nhanh_cu = config.TRA_LOI_NHANH
    config.TRA_LOI_NHANH = False  # chấm câu trả lời của AI, không chấm câu soạn sẵn ("mấy giờ rồi"...)
    try:
        return _chay(client, tinh_huong, ket_qua)
    finally:
        config.TRA_LOI_NHANH = nhanh_cu


def _chay(client, tinh_huong: list[dict], ket_qua: list) -> list[KetQua]:
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
            if th.get("hom_nay_dac_biet"):  # giả vờ hôm nay là ngày đặc biệt này
                from datetime import date

                today = date.today().strftime("%d/%m")
                memory.add_special_days([{"ngay": today, "viec": v} for v in th["hom_nay_dac_biet"]])
            memory.add_todos(th.get("viec_dang_co", []))
            memory.add_habits(th.get("thoi_quen_dang_co", []))
            if th.get("nhac_dang_co"):  # [{"viec", "lap"}] — lần nhắc tới là 1 giờ sau
                from datetime import datetime, timedelta

                luc = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
                memory.add_reminders([{"luc": luc, **x} for x in th["nhac_dang_co"]])
            if th.get("buon_may_ngay"):  # giả vờ hôm qua và hôm kia người dùng buồn
                for d in (1, 2):
                    mid = memory.add_message("user", "Chán quá")
                    memory.conn.execute(
                        f"UPDATE messages SET tam_trang = 'buon', created_at = datetime('now', 'localtime', '-{d} day') "
                        "WHERE id = ?", (mid,))
                    memory.add_message("assistant", "Thương ghê, kể Bơ nghe nha.")
                memory.conn.commit()
            ghi = _GhiLaiClient(client)
            try:
                reply = Brain(memory, client=ghi).chat(th["tin_nhan"])
                cu = set(th.get("viec_dang_co", []))  # việc có sẵn từ trước mà vẫn chưa được gạch
                con_lai = sum(t["viec"] in cu for t in memory.todos(include_done=False))
                if th.get("phai_huy_nhac"):  # đúng: bỏ việc này, giữ các lời nhắc khác
                    con = [r["viec"] for r in memory.upcoming_reminders()]
                    reply.huy_nhac_dung = th["phai_huy_nhac"] not in con and len(con) == len(th["nhac_dang_co"]) - 1
                if th.get("phai_tich_hom_qua"):  # đúng: tích hôm qua, KHÔNG tích hôm nay
                    hs = memory.habits()
                    reply.tich_hom_qua_dung = bool(hs) and all(h["ngay_30"][-2] and not h["hom_nay"] for h in hs)
            finally:
                memory.conn.close()
            ket_qua.append(cham(th, ghi.chu_cuoi, reply, con_lai))
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
