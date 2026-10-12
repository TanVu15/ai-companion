"""Chạm & chơi (web/choi.js): phần tính toán thuần chạy bằng node, không cần trình duyệt, không gọi API."""
import json
import subprocess

from app import config
from tests.test_api import make_client


def node(code):
    r = subprocess.run(["node", "-e", "const C = {...require('./web/choi.js'), ...require('./web/do_choi.js')};\n" + code],
                       cwd=config.ROOT, capture_output=True, text=True, timeout=30)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_vung_cham():
    v = node("""console.log(JSON.stringify([
      C.boVungCham(52, 25), C.boVungCham(148, 25), C.boVungCham(100, 60), C.boVungCham(100, 112),
      C.boVungCham(100, 145), C.boVungCham(45, 140), C.boVungCham(5, 5), C.boVungCham(198, 190)]))""")
    assert v == ["tai_trai", "tai_phai", "dau", "cam", "bung", "lung", None, None]
    assert node("console.log(JSON.stringify([C.boVungCham(82, 176), C.boVungCham(118, 172), C.boVungCham(100, 150)]))") == ["chan", "chan", "bung"]
    assert node("console.log(JSON.stringify([C.boVungCham(186, 105), C.boVungCham(176, 80), C.boVungCham(190, 150)]))") == ["duoi", "duoi", None]


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
    assert html.index("/web/meo.js") < html.index("/web/choi.js") < html.index("/web/do_choi.js")


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


def test_huong_nhin():
    v = node("""console.log(JSON.stringify([C.boHuongNhin(0, 0), C.boHuongNhin(200, 0), C.boHuongNhin(0, -300),
      C.boHuongNhin(40, 0)]))""")
    assert v == [[0, 0], [4, 0], [0, -3], [2, 0]]  # gần thì liếc nhẹ, xa thì liếc hết cỡ


def test_luc_mo_mung_va_vuon_vai():
    v = node("""const H = 3600000, t = 1000 * H;
      console.log(JSON.stringify([C.boLucMo(0, t, 8), C.boLucMo(t - 30 * H, t, 15), C.boLucMo(t - 5 * H, t, 7),
        C.boLucMo(t - 2 * H, t, 7), C.boLucMo(t - 5 * H, t, 14), C.boLucMo(t + H, t, 8)]))""")
    assert v == [None, "mung", "vuon", None, None, None]


def test_cau_doc_to_deu_co_cau_va_doc_duoc():
    v = node("""console.log(JSON.stringify(C.BO_DOC_TO.map(k => C.BO_CAU_CHOI[k])))""")
    for ds in v:
        assert ds and all(len(c) < 60 for c in ds)


def test_cuon_len_roi_nay_roi_nam_yen():
    v = node("""let s = {x: 100, y: 20, vx: 300, vy: 0}; const vet = [];
      for (let i = 0; i < 400; i++) { s = C.boBuocLen(s, 0.016, 300, 200); vet.push(s); }
      const trongKhung = vet.every(q => q.x >= 15 && q.x <= 285 && q.y >= 15 && q.y <= 185);
      const daNay = vet.some((q, i) => i && q.vy < 0 && vet[i - 1].vy >= 0);
      console.log(JSON.stringify([trongKhung, daNay, s.yen, s.y]))""")
    assert v == [True, True, True, 185]  # luôn trong khung, có nảy, cuối cùng nằm yên trên sàn


def test_mo_ta_choi_co_cuon_len():
    from app.brain import mo_ta_choi

    assert "cuộn len" in mo_ta_choi({"len": 3})


def test_nut_long_vu_va_dem():
    from app.brain import mo_ta_choi

    html = (config.ROOT / "web" / "index.html").read_text(encoding="utf-8")
    assert 'id="longVu"' in html and 'id="cuonLen"' in html
    assert "lông vũ" in mo_ta_choi({"long_vu": 2})
    assert node("console.log(JSON.stringify(C.boCauNgau('long_vu', () => 0)))")


def test_do_choi_tach_rieng():
    """Đồ chơi (laser, cuộn len, lông vũ) nằm ở do_choi.js; choi.js chỉ hỏi qua boChoi.doChoi, không đụng biến của đồ chơi."""
    choi = (config.ROOT / "web" / "choi.js").read_text(encoding="utf-8")
    do_choi = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    giao_dien = choi.split("// ---- Phần giao diện")[1]
    for ten in ("laserBat", "lenKeo", "batLen", "batLongVu", "getElementById('doChoi')", "getElementById('cuonLen')"):
        assert ten not in giao_dien, ten
    for ten in ("function batLaser", "function batLen", "function batLongVu", "doChoi.dangChoi =", "doChoi.dieuKhien =", "doChoi.keoLen ="):
        assert ten in do_choi, ten
    assert "boBuocLen" not in choi


def test_cuon_len_khong_nam_de_len_nut():
    v = node("""const nut = [{x: 0, y: 150, w: 40, h: 40}, {x: 260, y: 150, w: 40, h: 40}];
      console.log(JSON.stringify([C.boLenDeNut(20, 185, nut, 150), C.boLenDeNut(280, 185, nut, 150),
        C.boLenDeNut(150, 185, nut, 150), C.boLenDeNut(54, 185, nut, 150), C.boLenDeNut(20, 185, [], 150)]))""")
    assert v == [1, -1, 0, 1, 0]  # đè nút bên trái → lăn sang phải, bên phải → sang trái; chỉ chạm mép (54-15<40) cũng tính


def test_huong_vuot_nguoc_long():
    v = node("""console.log(JSON.stringify([C.boHuongVuot(0, -50), C.boHuongVuot(5, -40), C.boHuongVuot(0, 50),
      C.boHuongVuot(60, -30), C.boHuongVuot(0, -10), C.boHuongVuot(-30, -45)]))""")
    assert v == ["nguoc", "nguoc", "xuoi", "xuoi", "xuoi", "nguoc"]  # chỉ vuốt hẳn lên trên mới là ngược lông


def test_meo_co_long_dung_khi_vuot_nguoc():
    meo = (config.ROOT / "web" / "meo.js").read_text(encoding="utf-8")
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    assert 'class="long-dung"' in meo and ".meo.nguoc-long .long-dung" in css


def test_cham_chan_hai_lan_la_dap_tay():
    v = node("""console.log(JSON.stringify([C.boChamChan(0, 5000), C.boChamChan(4700, 5000), C.boChamChan(4000, 5000),
      C.boChamChan(5200, 5000)]))""")
    assert v == ["chan", "dap_tay", "chan", "chan"]
    from app.brain import mo_ta_choi
    assert "đập tay với Bơ 2 lần" in mo_ta_choi({"dap_tay": 2})  # lần đầu / hai lần nhanh / cách xa / giờ máy lùi


def test_thong_so_tieng_meo():
    v = node("""console.log(JSON.stringify(['ngan', 'vui', 'la'].map(C.boThongSoMeo)))""")
    for s in v:
        assert 0.1 < s["dai"] < 1 and len(s["cao"]) == 3 and len(s["vang"]) == 3
        assert all(200 < f < 3000 for f in s["cao"] + s["vang"])
    assert v[2] == v[0]  # kiểu lạ → tiếng ngắn
    assert v[1]["cao"][1] > v[1]["cao"][0]  # "meo~" vui thì cao dần lên
    choi = (config.ROOT / "web" / "choi.js").read_text(encoding="utf-8")
    ham = choi.split("function duocKeu(")[1].split("\n  }\n")[0]
    assert "if (!duocKeu()) return;" in choi.split("function keu(")[1] and "if (!duocKeu()) return;" in choi.split("function tiengAn(")[1]
    for dk in ("voiceOn", "speaking", "handsFree", "boGioYenLang"):  # chỉ kêu khi bật giọng, không lúc đang đọc/nghe/giờ yên lặng
        assert dk in ham, dk


def test_gan_mui():
    v = node("""console.log(JSON.stringify([C.boGanMui(100, 88), C.boGanMui(115, 95), C.boGanMui(100, 60), C.boGanMui(140, 90),
      C.boGanMui(100, 140)]))""")
    assert v == [True, True, False, False, False]  # ngay mũi / sát bên mũi / trán / má xa / bụng


def test_phim_tat_cho_cham_moi():
    html = (config.ROOT / "web" / "index.html").read_text(encoding="utf-8")
    choi = (config.ROOT / "web" / "choi.js").read_text(encoding="utf-8")
    assert "T chạm tai, D đập tay" in html
    assert "t: Math.random() < 0.5 ? 'tai_trai' : 'tai_phai', d: 'chan'" in choi


def test_ru_ru_to_dan():
    v = node("""console.log(JSON.stringify([0, 1, 3, 10, 100, -5].map(C.boDoToRuRu)))""")
    assert v[0] < v[1] < v[2] < v[3] and v[3] == v[4] == 0.5 and v[5] == v[0]


def test_nhan_biet_lac_dien_thoai():
    v = node("""const a = {x: 0, y: 9.8, z: 0}, b = {x: 15, y: -5, z: 3};
      let s = {moc: []}; const ra = [];
      for (const [t, g] of [[0, 30], [200, 30], [400, 5], [500, 30], [700, 30]]) { s = C.boLac(s.moc, t, g); ra.push(s.lac); }
      const cham = [0, 1500, 3000, 4500, 6000].reduce((q, t) => C.boLac(q.moc, t, 30), {moc: []});
      console.log(JSON.stringify([C.boDoGiat(a, b), C.boDoGiat(null, b), ra, cham.lac]))""")
    assert v[0] == 32.8 and v[1] == 0
    assert v[2] == [False, False, False, False, True]  # đủ 4 cú giật mạnh trong 1 giây mới tính là lắc
    assert v[3] is False  # giật lẻ tẻ cách xa nhau (đi bộ, đặt máy xuống) không tính
    html = (config.ROOT / "web" / "index.html").read_text(encoding="utf-8")
    assert 'id="lacBat"' in html


def test_vuot_luc_dang_doc_khong_bao_im():
    # chạm nhanh = bảo Bơ im; vuốt (kéo) hay nhấn giữ thì không — choi.js báo qua boChoi.vuaKeo()
    choi = (config.ROOT / "web" / "choi.js").read_text(encoding="utf-8")
    hop = (config.ROOT / "web" / "hop_thoai.js").read_text(encoding="utf-8")
    assert "vuaKeo = !!b && (b.di >= 10 || Date.now() - b.t >= 500)" in choi
    assert "boChoi.vuaKeo()) return; stopSpeaking()" in hop
    assert "'chong_mat', 'ngui'" in choi  # câu chóng mặt, ngửi tay được đọc to khi bật Giọng nói


def test_goi_y_tro_chua_thu():
    v = node("""const tat = Object.keys(C.BO_GOI_Y);
      console.log(JSON.stringify([
        C.boGoiY([], '2026-10-10', '2026-10-11', true, () => 0),
        C.boGoiY([], '2026-10-11', '2026-10-11', true, () => 0),
        C.boGoiY(tat.filter(k => k !== 'ngui'), '', '2026-10-11', true, () => 0.99),
        C.boGoiY(tat.filter(k => k !== 'chong_mat'), '', '2026-10-11', false),
        C.boGoiY(tat, '', '2026-10-11', true),
        Object.values(C.BO_GOI_Y).every(c => c.length < 70)]))""")
    assert v == ["dap_tay", None, "ngui", None, None, True]  # 1 lần/ngày; chỉ trò chưa thử; máy không lắc được thì khỏi gợi ý lắc


def test_bo_de_y_tin_nhan():
    v = node("""console.log(JSON.stringify(['Tối nay ăn cá kho', 'các bạn ơi', 'cám ơn Bơ', 'cả ngày mệt', '🐟🐟',
      'thương Bơ ghê', 'dễ thương quá', 'yêu cầu gửi báo cáo', 'mình yêu Bơ', 'hihi ❤️', 'hôm nay đi làm', '', null, 'việc cá nhân', 'cá tính mạnh', 'mua cá'].map(C.boPhanUngTin)))""")
    assert v == ["ca", None, None, None, "ca", "tim", "tim", None, "tim", "tim", None, None, None, None, None, "ca"]


def test_chon_mon_an():
    v = node("""console.log(JSON.stringify([
      Object.keys(C.BO_MON_AN), ['ca', 'sua', 'pate', 'banh', '', null, undefined, 'toString'].map(C.boMonAn),
      Object.values(C.BO_MON_AN).map(m => [m.ten, C.BO_CAU_CHOI[m.cau].length > 0, C.BO_DOC_TO.includes(m.cau), m.svg.startsWith('<svg')])]))""")
    assert v[0] == ["ca", "sua", "pate"]
    assert v[1] == ["ca", "sua", "pate", "ca", "ca", "ca", "ca", "ca"]  # món lạ → cá
    assert v[2] == [["Cá", True, True, True], ["Sữa", True, True, True], ["Pate", True, True, True]]


def test_trang_co_menu_chon_mon(tmp_path):
    html = make_client(tmp_path, []).get("/").text
    assert 'id="menuAn"' in html and 'role="menu"' in html and 'aria-controls="menuAn"' in html
    choi = (config.ROOT / "web" / "choi.js").read_text(encoding="utf-8")
    assert "localStorage.setItem('bo_mon_an'" in choi  # nhớ món vừa chọn trên máy này
    assert "cho_an > 5" in choi  # vẫn không có thanh đói: ăn nhiều chỉ bảo no


def test_tieng_an_theo_mon():
    v = node("""const r = () => 0.5; console.log(JSON.stringify(['ca', 'sua', 'pate', 'la'].map(m => C.boNhipAn(m, r))))""")
    ca, sua, pate, la = v
    assert la == ca  # món lạ → tiếng nhai cá
    assert len(sua) > len(ca) > len(pate) >= 5  # sữa liếm nhanh, nhiều nhịp; pate chép chậm
    assert pate[0]["hz"] < sua[0]["hz"] < ca[0]["hz"]  # cá giòn nhất, pate trầm nhất
    for ds in (ca, sua, pate):
        assert all(0.3 < n["t"] and n["t"] + n["dai"] < 2.6 and 0 < n["to"] <= 0.8 for n in ds)  # gọn trong lúc ăn, không quá to (đã đo: cỡ tiếng meo)
        assert [n["t"] for n in ds] == sorted(n["t"] for n in ds)
    w = node("""console.log(JSON.stringify([0, 0.999].map(x => C.boNhipAn('ca', () => x).every(n => n.to > 0 && n.t > 0.3))))""")
    assert w == [True, True]


def test_be_bo_keo_len():
    v = node("""console.log(JSON.stringify([[0, -10], [0, -20], [0, -60], [5, -100], [0, -200], [80, -60], [0, 60], [-30, -50]].map(([x, y]) => C.boDoNhac(x, y))))""")
    assert v == [0, 0, 0.5, 1, 1, 0, 0, 0.38]  # phải kéo hẳn lên (quá 20px, dọc nhiều hơn ngang); cao tối đa 1
    choi = (config.ROOT / "web" / "choi.js").read_text(encoding="utf-8")
    assert "clearTimeout(henBe); thaBe();" in choi  # nhả tay (hay bị hủy) là thả Bơ xuống, không kẹt trên không
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    assert ".meo.be {" in css and ".meo.roi .body" in css and ".meo.be.em" in css
    assert "dem('be').be === 1" in choi  # lần bế đầu trong ngày mới đọc to
    v = node("console.log(JSON.stringify([C.BO_DOC_TO.includes('em'), C.BO_DOC_TO.includes('be'), C.BO_CAU_CHOI.em.length]))")
    assert v == [True, False, 3]  # bế yên: "Bế Bơ êm ghê~" được đọc to; câu bế thì chỉ lần đầu


def test_boop_mui_va_nung_ma():
    v = node("""console.log(JSON.stringify([[100, 88], [100, 94], [62, 91], [138, 92], [100, 60], [80, 74]].map(([x, y]) => [C.boVungCham(x, y), C.boChiTietDau(x, y)])))""")
    assert v == [["dau", "mui"], ["dau", "mui"], ["dau", "ma_trai"], ["dau", "ma_phai"], ["dau", None], ["dau", None]]  # mũi, má đều nằm trong đầu; trán, mắt thì vẫn là xoa đầu


def test_ngap_lay():
    v = node("""console.log(JSON.stringify(['buồn ngủ quá', 'Bơ ơi mình đi ngủ nha', '😴', 'ngáp hoài', 'ngủ ngon nha Bơ', 'ngủ trưa dậy rồi', 'thương Bơ, buồn ngủ quá', 'tối ăn cá rồi đi ngủ'].map(C.boPhanUngTin)))""")
    assert v == ["ngap", "ngap", "ngap", "ngap", "ngap", None, "tim", "ca"]  # cá / tim ưu tiên trước


def test_long_vu_rinh():
    """Lông vũ sát đất trước mặt Bơ → Bơ rình; trên đầu, ngang mũi, xa hai bên thì không."""
    v = node("""console.log(JSON.stringify([C.boLongVuRinh(100, 190), C.boLongVuRinh(40, 175), C.boLongVuRinh(170, 230),
      C.boLongVuRinh(100, 20), C.boLongVuRinh(100, 90), C.boLongVuRinh(100, 140), C.boLongVuRinh(-10, 190), C.boLongVuRinh(100, 290)]))""")
    assert v == [True, True, True, False, False, False, False, False]


def test_rinh_co_cau_va_kieu_dang():
    v = node("console.log(JSON.stringify([C.BO_CAU_CHOI.rinh.length, C.BO_CAU_CHOI.vo_rinh.length, 'rinh' in C.BO_GOI_Y]))")
    assert v == [3, 4, True]
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    do_choi = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    for c in (".meo.rinh", ".meo.vo-rinh", "meo-ngoay"):
        assert c in css, c
    assert "boRinh();" in do_choi  # cất lông vũ thì thôi rình (không kẹt tư thế)


def test_ngap_lay_khong_buon_ngu():
    """Nói "không/chưa/hết buồn ngủ" thì Bơ không ngáp."""
    v = node("""console.log(JSON.stringify(['mình không buồn ngủ', 'chưa buồn ngủ gì hết', 'hết buồn ngủ rồi',
      'Bơ không buồn ngủ hả, mình buồn ngủ quá'].map(C.boPhanUngTin)))""")
    assert v == [None, None, None, "ngap"]


def test_nhoi_bot():
    """Vuốt liền 6 giây trở lên thì Bơ nhồi bột; có câu và kiểu dáng riêng."""
    v = node("console.log(JSON.stringify([C.boNhoiBot(0), C.boNhoiBot(5.9), C.boNhoiBot(6), C.boNhoiBot(20), C.BO_CAU_CHOI.nhoi.length]))")
    assert v == [False, False, True, True, 3]
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    assert ".meo.nhoi .paw-l" in css and "meo-nhoi" in css


def test_vo_rinh_doc_to_lan_dau():
    """Lần vồ lông vũ đầu tiên trong ngày được đọc to; các lần sau chỉ kêu meo (không đọc lặp)."""
    do_choi = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    assert "dem('rinh').rinh === 1" in do_choi
    assert "noi('vo_rinh', true, dauTien)" in do_choi
    assert "vo_rinh" not in node("console.log(JSON.stringify(C.BO_DOC_TO))")


def test_be_va_nguoc_long_tat_nhoi_bot():
    """Đang nhồi bột mà bế Bơ / vuốt ngược lông thì thôi nhồi (kẻo chân vẫn dẫm khi đang lủng lẳng)."""
    choi = (config.ROOT / "web" / "choi.js").read_text(encoding="utf-8")
    assert "svg.classList.add('be'); svg.classList.remove('vuot', 'gai-cam', 'lan', 'bep', 'nhoi');" in choi
    assert "svg.classList.remove('vuot', 'gai-cam', 'nhoi');\n    giu('nguoc-long'" in choi


def test_chop_mat_cham():
    """Vuốt xong một lượt dài (≥3 giây) thì Bơ chớp mắt chậm; không lặp trong 20 giây."""
    v = node("console.log(JSON.stringify([C.boChopCham(1, 1e9), C.boChopCham(3, 1e9), C.boChopCham(8, 5000), C.boChopCham(8, 20000)]))")
    assert v == [False, True, False, True]
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    assert "meo-chop-cham" in css


def test_chop_cham_khong_chen_khi_vuot_lai():
    """Đang chớp mắt chậm mà vuốt lại thì thôi chớp; đang bế/đang vuốt thì không chớp chen vào."""
    choi = (config.ROOT / "web" / "choi.js").read_text(encoding="utf-8")
    assert "svg.classList.remove('chop-cham');" in choi
    assert "if (!vuotDangChay && !svg.classList.contains('be')" in choi


def test_long_vu_ben_hong():
    """Lông vũ ngang tầm bên hông → Bơ quơ chân về bên đó; trên đầu, sát đất, trước mặt thì không."""
    v = node("""console.log(JSON.stringify([C.boLongVuBenHong(10, 100), C.boLongVuBenHong(190, 80), C.boLongVuBenHong(100, 100),
      C.boLongVuBenHong(10, 20), C.boLongVuBenHong(190, 190), C.boLongVuBenHong(-100, 100)]))""")
    assert v == ["trai", "phai", None, None, None, None]
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    assert ".meo.quo-trai .paw-l" in css and ".meo.quo-phai .paw-r" in css


def test_quo_chan_khong_chong_tu_the():
    """Quơ chân không chen vào lúc đang rình hay đang đứng vồ lông trên đầu; đổi bên thì bỏ bên cũ."""
    do_choi = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    assert "!svg.classList.contains('rinh') && !svg.classList.contains('voi')" in do_choi
    assert "svg.classList.remove(hong === 'trai' ? 'quo-phai' : 'quo-trai')" in do_choi


def test_len_gan_meo():
    """Cuộn len nằm yên sát bên Bơ (ngang tầm chân, hai bên) → Bơ ôm len; xa quá hay trên cao thì không."""
    v = node("""console.log(JSON.stringify([C.boLenGanMeo(20, 178), C.boLenGanMeo(185, 178), C.boLenGanMeo(100, 160),
      C.boLenGanMeo(-30, 178), C.boLenGanMeo(240, 178), C.boLenGanMeo(20, 100)]))""")
    assert v == [True, True, True, False, False, False]
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    assert ".meo.om-len .paw-l" in css and ".meo.da-len .chan-sau" in css
    js = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    # cầm len lên giữa chừng thì thôi ôm; vừa đá ra thì khỏi vồ lại liền
    assert "ev.preventDefault(); ev.stopPropagation(); thoiOmLen();" in js
    assert "voLen = Date.now() + 400;" in js
    assert "noi('om_len', true, dem('om_len').om_len === 1);" in js  # lần ôm đầu tiên trong ngày đọc to


def test_len_lan_qua():
    """Cuộn len lăn ngang qua trước mặt Bơ → đầu quay theo (-1 trái … 1 phải); len đứng yên, chậm, trên cao, xa quá thì thôi."""
    v = node("""console.log(JSON.stringify([C.boLenLanQua(-20, 180, 300), C.boLenLanQua(220, 180, -300), C.boLenLanQua(100, 200, 200),
      C.boLenLanQua(40, 180, 0), C.boLenLanQua(40, 180, 30), C.boLenLanQua(40, 60, 300), C.boLenLanQua(-250, 180, 300)]))""")
    assert v == [-1, 1, 0, None, None, None, None]
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    assert ".meo.theo-len .head" in css and "var(--theo-len" in css and ".meo.theo-len .tail { animation" in css
    js = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    # vồ len thì thôi quay đầu liền (khỏi lẫn tư thế); cất len, ôm len cũng thôi
    assert "thoiTheoLen(); giu('vo', 600)" in js and "thoiTheoLen(); svg.classList.add('om-len')" in js
    assert "len.remove(); len = null; lenKeo = null; thoiTheoLen();" in js
    # đang được vuốt, gãi cằm, boop... thì khỏi quay đầu theo len (không đè tư thế đầu khác)
    for c in ["'vuot'", "'gai-cam'", "'boop'", "'khoe'", "'nhoi'", "'em'"]:
        assert c in js.split("const TU_THE_KHAC")[1].split("];")[0]


def test_laser_tren_cao_ke_ke():
    """Chấm laser đứng yên trên cao phía trên đầu Bơ → Bơ ngửa nhìn, miệng run run "ke ke ke"; chấm trước chân/xa thì không."""
    v = node("""console.log(JSON.stringify([C.boLaserTrenCao(100, 10), C.boLaserTrenCao(20, -5), C.boLaserTrenCao(180, 20),
      C.boLaserTrenCao(100, 60), C.boLaserTrenCao(100, 190), C.boLaserTrenCao(-60, 0), C.BO_CAU_CHOI.ke_ke.length > 0]))""")
    assert v == [True, True, True, False, False, False, True]
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    assert ".meo.ke-ke .mieng-mo" in css and "@keyframes meo-ke-ke" in css
    js = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    # phải đứng yên mới tính (chấm còn chạy thì đếm lại); tắt laser thì thôi; nghỉ 6 giây giữa hai lần
    assert "clearTimeout(kkHen);        // chấm còn di chuyển" in js
    assert "thoiRinhLaser(); thoiKeKe();" in js and "Date.now() - kkCuoi < 6000" in js
    assert "noi('ke_ke', true, dem('ke_ke').ke_ke === 1);" in js  # lần ke ke đầu tiên trong ngày đọc to
    # đang ke ke mà cho ăn → thôi ke ke (không vừa ăn vừa run miệng)
    assert "doChoi.thaLen = () => { thaLen(); thoiRinhLaser(); thoiKeKe(); thoiTheoLen(); };" in js


def test_long_vu_cu_lung():
    """Lông vũ lướt qua lưng/bụng Bơ → lông rùng nhẹ, Bơ quay đầu nhìn chỗ nhột, cười; lông đứng yên thì không (nghỉ 3 giây)."""
    v = node("console.log(JSON.stringify([C.BO_CAU_CHOI.nhot.length > 0, C.BO_DOC_TO.includes('nhot')]))")
    assert v == [True, False]
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    assert ".meo.nhot-long .head" in css and "var(--nhot" in css and "@keyframes meo-rung-long" in css
    js = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    assert "(vung === 'lung' || vung === 'bung') && dangLuot && Date.now() - lvNhot > 3000" in js
    assert "giu('nhot-long', 900)" in js
    # đang nhột mà lông bay lên đầu (vồ), sang hông (quơ), xuống đất (rình), qua mũi (hắt xì) → bỏ tư thế nhột cho khỏi lẫn
    assert js.count("svg.classList.remove('nhot-long');") + js.count("svg.classList.remove('nhot-long', 'quat-duoi');") == 4


def test_cho_an_luc_om_len_thi_buong_len():
    """Đang ôm cuộn len mà cho ăn → Bơ buông len ra (không vừa ôm vừa ăn)."""
    choi = (config.ROOT / "web" / "choi.js").read_text(encoding="utf-8")
    assert "dangAn = true; doChoi.thaLen();" in choi
    assert "doChoi.thaLen = () => { thaLen(); thoiRinhLaser();" in (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")


def test_laser_truoc_mat():
    """Chấm laser đứng yên trên sàn trước/cạnh chân Bơ → Bơ rình rồi vồ đè lên, nhấc chân ngó; trên cao hay xa quá thì không."""
    v = node("""console.log(JSON.stringify([C.boLaserTruocMat(100, 190), C.boLaserTruocMat(50, 180), C.boLaserTruocMat(170, 200),
      C.boLaserTruocMat(100, 120), C.boLaserTruocMat(195, 190), C.boLaserTruocMat(100, 270)]))""")
    assert v == [True, True, True, False, False, False]
    assert "laser_mat" in node("console.log(JSON.stringify(Object.keys(C.BO_CAU_CHOI)))")
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    assert ".laser.bi-de" in css and ".meo.ngo-chan .paw-r" in css
    js = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    assert "clearTimeout(laserTat); thoiRinhLaser();" in js  # tắt laser thì thôi rình


def test_khoe_chien_tich():
    """Vừa vồ trúng (trong 8 giây) mà được vuốt → Bơ khoe; lâu quá hoặc vừa khoe xong (dưới 20 giây) thì không."""
    v = node("""console.log(JSON.stringify([C.boKhoe(2000, 60000), C.boKhoe(9000, 60000), C.boKhoe(2000, 5000), C.boKhoe(-5, 60000)]))""")
    assert v == [True, False, False, False]
    assert "khoe" in node("console.log(JSON.stringify(Object.keys(C.BO_CAU_CHOI)))")
    js = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    assert js.count("daBat();") >= 5  # laser vồ, laser rình-vồ, len vồ, đá len, lông vũ rình-vồ
    choi = (config.ROOT / "web" / "choi.js").read_text(encoding="utf-8")
    assert "noi('khoe', true, dem('khoe').khoe === 1);" in choi  # lần đầu trong ngày đọc to


def test_len_cham_duoi_ngoai_lai():
    """Cuộn len lăn chạm đuôi Bơ → đuôi vểnh, Bơ ngoái lại "Ai đụng đuôi Bơ?" (không vồ); len ở chân, trên đầu, bên trái thì không."""
    v = node("""console.log(JSON.stringify([C.boLenChamDuoi(184, 108), C.boLenChamDuoi(175, 80), C.boLenChamDuoi(185, 176),
      C.boLenChamDuoi(118, 174), C.boLenChamDuoi(40, 170), C.boLenChamDuoi(100, 20), C.boLenChamDuoi(225, 176),
      C.BO_CAU_CHOI.ngoai_duoi.length > 0]))""")
    assert v == [True, True, True, False, False, False, False, True]
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    assert ".meo.ngoai-duoi .head" in css and "@keyframes meo-duoi-vinh" in css
    js = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    # kiểm tra chạm đuôi trước khi vồ; nghỉ 3 giây; ngủ/buồn/nằm bẹp/bế thì thôi; len vừa thả ra khỏi tính liền
    assert "if (lenChamDuoi(p)) return;\n    if (lenKeo || !boVungCham" in js
    assert "Date.now() - duoiCuoi < 3000 || Date.now() - voLen < 1500" in js and "['ngu', 'buon'].includes(face.dataset.e)" in js
    assert "lenMoi = true;" in js and "thoiOmLen(); lenMoi = false;" in js and "lenKeo || lenMoi || lenS.yen" in js
    assert "'ngoai-duoi'" in js.split("const TU_THE_KHAC")[1].split("];")[0]
    # bật Giọng nói: lần "Ai đụng đuôi Bơ?" đầu tiên trong ngày đọc to, các lần sau chỉ hiện chữ
    assert "noi('ngoai_duoi', true, dem('ngoai_duoi').ngoai_duoi === 1);" in js


def test_khuya_mat_lim_dim_khong_de_mat_tron():
    """Khuya (lim-dim) mắt lim dim, nhưng lúc giật mình, vồ, rình, nhìn theo len, ke ke, ngoái đuôi, được bế... mắt vẫn tròn."""
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    dong = [d for d in css.splitlines() if d.startswith('.face[data-e="binh_thuong"] .meo.lim-dim') and "scaleY(.6)" in d][0]
    for c in [".giat", ".vo", ".be", ".rinh", ".om-len", ".theo-len", ".ke-ke", ".ngoai-duoi"]:
        assert c + "," in dong.split(":not(")[1] or c + ")" in dong.split(":not(")[1]


def test_long_vu_quet_duoi():
    """Lông vũ quét nhanh qua đuôi → đuôi quất qua quất lại đuổi theo lông (không quơ chân); nghỉ 2,5 giây."""
    v = node("console.log(JSON.stringify([C.BO_CAU_CHOI.quat_duoi.length > 0, C.BO_DOC_TO.includes('quat_duoi'), C.boVungCham(184, 108)]))")
    assert v == [True, False, "duoi"]
    css = (config.ROOT / "web" / "meo.css").read_text(encoding="utf-8")
    assert ".meo.quat-duoi .tail { animation" in css and "@keyframes meo-quat-duoi" in css
    js = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    assert "const quetDuoi = vung === 'duoi' && Math.abs(vx) + Math.abs(vy) > 4;" in js and "Date.now() - lvDuoi > 2500" in js
    assert "const hong = svg.classList.contains('quat-duoi') ? null : boLongVuBenHong(p.x, p.y);" in js


def test_quat_duoi_khong_lan_tu_the():
    """Đang quất đuôi mà lông bay lên đầu (vồ), qua mũi (hắt xì), xuống đất (rình) → bỏ tư thế quất đuôi; lướt qua lưng thì không nhột chen vào."""
    js = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    assert "svg.classList.remove('nhot-long', 'quat-duoi'); giu('voi', 500);" in js
    assert "lvHatXi = Date.now(); svg.classList.remove('nhot-long', 'quat-duoi');" in js
    assert "svg.classList.remove('nhot-long', 'quat-duoi'); svg.classList.add('rinh');" in js
    assert "'quo-trai', 'quo-phai', 'quat-duoi', 'be', 'an'].some" in js


def test_len_cham_duoi_van_con_choi():
    """Len chạm đuôi vẫn gọi conChoi() (đang chơi thì Bơ đừng ngủ gật) — trước đây lỡ nằm trong dòng chú thích."""
    js = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    assert "noi('ngoai_duoi', true, dem('ngoai_duoi').ngoai_duoi === 1); conChoi();" in js
    for dong in js.splitlines():  # không dòng nào có lệnh nằm sau "//" kiểu "...) conChoi();"
        if "//" in dong and not dong.strip().startswith("//"):
            assert not dong.rstrip().endswith("conChoi();"), dong


def test_quat_duoi_doc_to_lan_dau():
    """Bật Giọng nói: lần quất đuôi đầu tiên trong ngày Bơ nói chắc chắn và đọc to; các lần sau lâu lâu mới hiện chữ."""
    js = (config.ROOT / "web" / "do_choi.js").read_text(encoding="utf-8")
    assert "if (dem('quat_duoi').quat_duoi === 1) noi('quat_duoi', true, true); else noi('quat_duoi');" in js
