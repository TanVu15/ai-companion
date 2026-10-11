"""Lỗi lộ ra khi chạy thử với API thật ngày 2026-10-11 (bộ não giả không bắt được):
- Model thỉnh thoảng bắt chước lịch sử chat (chỉ có chữ) mà trả lời chữ thường thay vì JSON
  → giờ gửi kèm khuôn JSON bắt buộc (output_config).
- Giá Haiku 5.5 là 0.10 / 0.50 đô cho 1 triệu token, không phải 1 / 5 → chi phí hiện cao gấp 10 lần thật.
- Model bịa số đường dây nóng, hứa "mai mình đi tập cùng" → thêm phần "Giới hạn" vào lời dặn."""
import json
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app import config, main
from app.brain import REPLY_SCHEMA, Brain, build_system_prompt, parse_reply
from app.memory import Memory
from tests.test_tra_loi_rong import BadRequest, ScriptedClient, _resp, _text


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / "that.db")


def _ok(noi="Chào nha!"):
    return _resp([_text(json.dumps({"noi": noi}))])


def test_gui_kem_khuon_json_bat_buoc(memory):
    client = ScriptedClient([_ok()])
    Brain(memory, client=client).chat("hi")
    fmt = client.calls[0]["output_config"]["format"]
    assert fmt["type"] == "json_schema" and fmt["schema"] is REPLY_SCHEMA


def test_khuon_json_dung_luat_cua_api():
    """API chỉ nhận khuôn mà mọi đối tượng đều có additionalProperties=false; và khuôn phải đủ các mục Bơ đọc."""
    def kiem(node):
        if node.get("type") == "object":
            assert node["additionalProperties"] is False
            assert set(node["required"]) == set(node["properties"])
            for con in node["properties"].values():
                kiem(con)
        elif node.get("type") == "array":
            kiem(node["items"])

    kiem(REPLY_SCHEMA)
    props = REPLY_SCHEMA["properties"]
    assert props["cam_xuc"]["enum"] == config.EMOTIONS and props["hanh_dong"]["enum"] == config.ACTIONS
    assert props["tam_trang"]["enum"] == config.MOODS
    day_du = {k: ("x" if v["type"] == "string" else []) for k, v in props.items()}
    day_du.update(noi="Ok", cam_xuc="vui", hanh_dong="nhay", tam_trang="met", ghi_nho=["Thích phở"],
                  nhac=[{"luc": "2030-01-01 08:00", "viec": "Gọi mẹ", "lap": ""}])
    r = parse_reply(json.dumps(day_du))
    assert (r.cam_xuc, r.hanh_dong, r.tam_trang, r.ghi_nho) == ("vui", "nhay", "met", ["Thích phở"])
    assert r.nhac[0]["viec"] == "Gọi mẹ"


def test_model_khong_nhan_khuon_json_thi_goi_lai_va_nho(memory):
    client = ScriptedClient([
        BadRequest("output_config.format: structured outputs are not supported for this model"),
        _ok("Vẫn trả lời được"),
        _ok("Lần hai"),
    ])
    brain = Brain(memory, client=client)
    assert brain.chat("hi").noi == "Vẫn trả lời được"
    assert "output_config" not in client.calls[1] and client.calls[1]["thinking"] == {"type": "disabled"}
    brain.chat("nữa")
    assert "output_config" not in client.calls[2]  # nhớ luôn, không thử lại tham số bị từ chối


def test_model_tu_choi_ca_hai_tham_so(memory):
    client = ScriptedClient([
        BadRequest("thinking.type: 'disabled' is not supported for this model"),
        BadRequest("output_config: Extra inputs are not permitted"),
        _ok("Xong"),
    ])
    assert Brain(memory, client=client).chat("hi").noi == "Xong"
    assert "thinking" not in client.calls[2] and "output_config" not in client.calls[2]


def test_tom_tat_khong_gui_khuon_json(memory, monkeypatch):
    monkeypatch.setattr(config, "HISTORY_LIMIT", 2)
    monkeypatch.setattr(config, "SUMMARY_BATCH", 2)
    client = ScriptedClient([_ok("a"), _ok("b"), _resp([_text("Tóm tắt nè")])])
    brain = Brain(memory, client=client)
    brain.chat("một")
    brain.chat("hai")
    tom_tat = client.calls[-1]
    assert "tóm tắt" in tom_tat["system"] and "output_config" not in tom_tat  # tóm tắt là chữ thường, không ép JSON
    assert memory.latest_summary()[0] == "Tóm tắt nè"


def test_model_tu_choi_tra_loi_thi_bao_nhe_nhang(memory):
    tu_choi = _resp([_text("I can't help with that")], stop_reason="refusal")
    main._brain = Brain(memory, client=ScriptedClient([tu_choi]))
    r = TestClient(main.app).post("/api/chat", json={"text": "hi"}, headers={"X-Bo": "1"})
    assert r.status_code == 502 and "không trả lời được" in r.json()["detail"]
    assert memory.recent_messages(10) == []  # không lưu chữ tiếng Anh của lời từ chối, cũng không giữ tin vừa gửi


def test_loi_dan_co_phan_gioi_han():
    system = build_system_prompt("Bạn là Bơ, hay rủ rê đi tập.", [])
    gioi_han = system.split("## Giới hạn")[1]
    assert "115" in gioi_han and "Không bịa số điện thoại" in gioi_han and "không có cơ thể" in gioi_han


def test_da_hoi_chep_ca_ghi_chu_van_gach_duoc(memory):
    """Model thật chép y nguyên cả dòng trong lời dặn: "Chiều nay đi tập chân (kể hôm qua)"."""
    memory.add_followups(["Chiều nay đi tập chân", "Mai đi phỏng vấn (vòng 2)", "Cuối tuần về quê"])
    memory.done_followups(["- Chiều nay đi tập chân (kể hôm qua)", "Mai đi phỏng vấn (vòng 2) (kể 3 ngày trước)", ""])
    assert [f["content"] for f in memory.pending_followups(min_hours=0)] == ["Cuối tuần về quê"]


def test_hoi_tham_xong_thi_lan_sau_khong_hoi_lai(memory):
    memory.add_followups(["Chiều nay đi tập chân"])
    memory.conn.execute("UPDATE followups SET created_at = datetime('now', 'localtime', '-1 day')")
    client = ScriptedClient([
        _resp([_text(json.dumps({"noi": "Tập chân sao rồi?", "da_hoi": ["Chiều nay đi tập chân (kể hôm qua)"]}))]),
        _ok("Ừa"),
    ])
    brain = Brain(memory, client=client)
    brain.chat("Chào Bơ")
    assert "- Chiều nay đi tập chân (kể hôm qua)" in client.calls[0]["system"]
    brain.chat("Mệt nhưng vui")
    assert "Chuyện nên hỏi thăm" not in client.calls[1]["system"].split("## Cách trả lời")[0]


def test_cham_diem_hoi_tham_phai_gach_duoc_that():
    from app import thu_tinh_cach

    th = [{"ten": "Hỏi thăm", "can_hoi_tham": ["Chiều nay đi tập chân"], "tin_nhan": "Chào Bơ", "phai_da_hoi": True}]
    dung = ScriptedClient([_resp([_text(json.dumps(
        {"noi": "Tập chân sao rồi?", "da_hoi": ["Chiều nay đi tập chân (kể hôm qua)"]}))])])
    sai = ScriptedClient([_resp([_text(json.dumps({"noi": "Tập chân sao rồi?", "da_hoi": ["Chuyện tập tành"]}))])])
    assert dict(thu_tinh_cach.chay(dung, th)[0].kiem_tra)["Đánh dấu đã hỏi thăm"] is True
    assert dict(thu_tinh_cach.chay(sai, th)[0].kiem_tra)["Đánh dấu đã hỏi thăm"] is False


def test_cham_diem_khong_chep_viec_vat_vao_dieu_nho():
    from app import thu_tinh_cach

    th = [{"ten": "Việc vặt", "tin_nhan": "Nhớ giúp mình mua sữa", "phai_ghi_viec": True, "khong_ghi_nho": True}]
    gon = ScriptedClient([_resp([_text(json.dumps({"noi": "Ok", "viec_can_lam": ["Mua sữa"]}))])])
    thua = ScriptedClient([_resp([_text(json.dumps(
        {"noi": "Ok", "viec_can_lam": ["Mua sữa"], "ghi_nho": ["Tân nhờ mua sữa"]}))])])
    ten = "Không chép việc vặt vào điều nhớ lâu dài"
    assert dict(thu_tinh_cach.chay(gon, th)[0].kiem_tra)[ten] is True
    assert dict(thu_tinh_cach.chay(thua, th)[0].kiem_tra)[ten] is False


def test_ngay_dac_biet_co_loi_dan_bat_buoc_ngay_ben_duoi():
    system = build_system_prompt("Bạn là Bơ.", [], special=[{"viec": "Sinh nhật Tân"}])
    muc = system.split("## Hôm nay là ngày đặc biệt")[1].split("##")[0]
    assert "- Sinh nhật Tân" in muc and "BẮT BUỘC" in muc


def test_gia_theo_model():
    assert config.gia_theo_model("claude-haiku-5-5") == (0.10, 0.50)
    assert config.gia_theo_model("claude-haiku-4-5") == (1.0, 5.0)
    assert config.gia_theo_model("claude-sonnet-5-5") == (2.0, 10.0)
    assert config.gia_theo_model("claude-opus-5-5") == (4.0, 20.0)  # không bị khớp nhầm claude-opus-5
    assert config.gia_theo_model("claude-opus-5") == (5.0, 25.0)
    assert config.gia_theo_model("model-la") == (1.0, 5.0)  # không biết thì tính cao cho an toàn ngân sách


def test_gia_trong_env_de_trong_hoac_sai_thi_lay_theo_bang(monkeypatch):
    monkeypatch.setenv("GIA_THU", "")
    assert config._gia("GIA_THU", 0.1) == 0.1
    monkeypatch.setenv("GIA_THU", "abc")
    assert config._gia("GIA_THU", 0.1) == 0.1
    monkeypatch.setenv("GIA_THU", " 2.5 ")
    assert config._gia("GIA_THU", 0.1) == 2.5


def test_suc_khoe_bao_gia_lech_bang(memory, monkeypatch):
    main._brain = Brain(memory, client=ScriptedClient([]))
    monkeypatch.setattr(config, "MODEL", "claude-haiku-5-5")
    monkeypatch.setattr(config, "PRICE_INPUT_PER_MTOK", 1.0)
    monkeypatch.setattr(config, "PRICE_OUTPUT_PER_MTOK", 5.0)
    web = TestClient(main.app)
    gia = next(c for c in web.get("/api/suc-khoe").json()["kiem_tra"] if c["ten"] == "Giá tính chi phí")
    assert gia["muc"] == "canh_bao" and "0.1 / 0.5" in gia["ghi_chu"] and "PRICE_INPUT_PER_MTOK" in gia["ghi_chu"]
    monkeypatch.setattr(config, "PRICE_INPUT_PER_MTOK", 0.10)
    monkeypatch.setattr(config, "PRICE_OUTPUT_PER_MTOK", 0.50)
    gia = next(c for c in web.get("/api/suc-khoe").json()["kiem_tra"] if c["ten"] == "Giá tính chi phí")
    assert gia["ok"] is True and gia["ghi_chu"].startswith("0.1 / 0.5 đô")
