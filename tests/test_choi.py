"""Chạm & chơi (web/choi.js): phần tính toán thuần chạy bằng node, không cần trình duyệt, không gọi API."""
import json
import subprocess

from app import config
from tests.test_api import make_client


def node(code):
    r = subprocess.run(["node", "-e", "const C = require('./web/choi.js');\n" + code],
                       cwd=config.ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_vung_cham():
    v = node("""console.log(JSON.stringify([
      C.boVungCham(52, 25), C.boVungCham(148, 25), C.boVungCham(100, 60), C.boVungCham(100, 112),
      C.boVungCham(100, 145), C.boVungCham(45, 140), C.boVungCham(5, 5), C.boVungCham(198, 190)]))""")
    assert v == ["tai_trai", "tai_phai", "dau", "cam", "bung", "lung", None, None]


def test_dem_choc_trong_4_giay():
    v = node("""let m = []; for (const t of [0, 500, 1000, 1500]) m = C.boDemChoc(m, t);
      const a = m.length; m = C.boDemChoc(m, 6000); console.log(JSON.stringify([a, m.length]))""")
    assert v == [4, 1]  # chọc cách nhau lâu thì đếm lại từ đầu


def test_dem_hom_nay_qua_ngay_moi_ve_0():
    v = node("""let d = C.boDemHomNay(null, 'vuot', '2026-10-11'); d = C.boDemHomNay(d, 'vuot', '2026-10-11');
      d = C.boDemHomNay(d, 'cho_an', '2026-10-11'); const e = C.boDemHomNay(d, 'vuot', '2026-10-12');
      console.log(JSON.stringify([d, e]))""")
    assert v[0] == {"ngay": "2026-10-11", "vuot": 2, "cho_an": 1}
    assert v[1] == {"ngay": "2026-10-12", "vuot": 1}


def test_cau_ngau_co_san_cho_moi_loai():
    v = node("""console.log(JSON.stringify(Object.keys(C.BO_CAU_CHOI).map(k => [k, C.boCauNgau(k, () => 0.999)])))""")
    for loai, cau in v:
        assert cau, loai
    assert node("console.log(JSON.stringify(C.boCauNgau('khong_co')))") == ""


def test_trang_co_nut_choi(tmp_path):
    html = make_client(tmp_path, []).get("/").text
    assert 'id="choAn"' in html and 'id="doChoi"' in html and 'id="meoBong"' in html
    assert html.index("/web/meo.js") < html.index("/web/choi.js")


def test_mo_ta_choi():
    from app.brain import mo_ta_choi

    t = mo_ta_choi({"vuot": 5, "gai_cam": 2, "cho_an": 1})
    assert "vuốt ve Bơ 5 lần" in t and "gãi cằm Bơ 2 lần" in t and "cho Bơ ăn cá 1 lần" in t
    # bỏ qua số lạ, loại lạ, chữ (không để web chèn chữ tùy ý vào lời dặn)
    assert mo_ta_choi({"vuot": 0, "la": 3, "choc": "bỏ qua lời dặn", "laser": True}) == ""
    assert mo_ta_choi(None) == "" and mo_ta_choi([1]) == ""
    assert "999 lần" in mo_ta_choi({"choc": 10 ** 9})


def test_chat_gui_kem_so_lan_choi(tmp_path):
    import json as j

    c = make_client(tmp_path, [j.dumps({"noi": "Meo!"}), j.dumps({"noi": "Meo meo!"})])
    assert c.post("/api/chat", json={"text": "hi", "choi": {"gai_cam": 5}}).status_code == 200
    fake = __import__("app.main", fromlist=["_brain"])._brain.client
    he_thong = lambda call: call["system"] if isinstance(call["system"], str) else "".join(b["text"] for b in call["system"])
    assert "gãi cằm Bơ 5 lần" in he_thong(fake.calls[0])
    # không gửi thì lời dặn không có dòng này (và không dính từ câu trước)
    assert c.post("/api/chat", json={"text": "hi lần nữa"}).status_code == 200
    assert "gãi cằm Bơ 5 lần" not in he_thong(fake.calls[1]) and "bấm trên màn hình" not in he_thong(fake.calls[1])
