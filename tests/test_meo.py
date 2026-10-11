"""Mèo Bơ (web/meo.js + web/meo.css): đủ bộ phận, đủ tư thế cho mọi cảm xúc/hành động của bộ não."""
import re
import subprocess

from app import config
from tests.test_api import make_client

ROOT = config.ROOT
JS = (ROOT / "web" / "meo.js").read_text(encoding="utf-8")
CSS = (ROOT / "web" / "meo.css").read_text(encoding="utf-8")


def test_trang_co_meo(tmp_path):
    c = make_client(tmp_path, [])
    html = c.get("/").text
    assert "/web/meo.css" in html and "/web/meo.js" in html
    # meo.js phải chạy trước app.js (app.js gọi meo.cho)
    assert html.index("/web/meo.js") < html.index("/web/app.js")
    assert c.get("/web/meo.css").status_code == 200 and c.get("/web/meo.js").status_code == 200


def test_meo_du_bo_phan():
    for cls in ["head", "ear-l", "ear-r", "mat-mo", "mat-cuoi", "mat-nham", "ria", "mieng-w", "mieng-mo",
                "bung", "paw-l", "paw-r", "chan-sau", "tail", "tail-ngu", "zzz"]:
        assert re.search(r'class="[^"]*\b' + cls + r'\b', JS), cls


def test_moi_cam_xuc_co_tu_the():
    # binh_thuong là tư thế mặc định; còn lại phải có luật riêng. Thêm cảm xúc mới vào config thì thêm cả ở meo.css
    for e in config.EMOTIONS + ["ngu"]:
        if e != "binh_thuong":
            assert f'[data-e="{e}"]' in CSS, e


def test_moi_hanh_dong_co_chuyen_dong():
    for a in config.ACTIONS:
        if a != "khong":
            assert f".a-{a}" in CSS, a


def test_ton_trong_giam_chuyen_dong():
    # mọi animation lặp chỉ nằm trong khối no-preference
    dau = CSS.index("@media (prefers-reduced-motion: no-preference)")
    truoc = CSS[:dau]
    assert "animation:" not in truoc
    assert "prefers-reduced-motion: reduce" in CSS


def test_meo_js_chay_khong_loi_va_tao_svg():
    # Chạy meo.js bằng node với một DOM giả tối thiểu: phải gắn svg vào #face và có window.meo.cho
    js = r"""
    const added = new Set();
    const svg = { classList: { add: c => added.add(c), remove: c => added.delete(c),
                               toggle: (c, b) => b ? added.add(c) : added.delete(c), contains: c => added.has(c) } };
    const face = { dataset: { e: 'binh_thuong' }, classList: { contains: () => false }, set innerHTML(v) { this.h = v; },
                   querySelector: () => svg };
    global.document = { getElementById: () => face, hidden: false };
    global.window = global; global.matchMedia = () => ({ matches: false });
    global.MutationObserver = class { constructor(f) {} observe() {} };
    global.setTimeout = () => 0; global.setInterval = () => 0;
    require('./web/meo.js');
    if (!face.h.includes('<svg')) throw new Error('khong ve svg');
    window.meo.cho(true); if (!added.has('cho')) throw new Error('cho khong bat');
    window.meo.cho(false); if (added.has('cho')) throw new Error('cho khong tat');
    console.log('ok');
    """
    r = subprocess.run(["node", "-e", js], cwd=ROOT, capture_output=True, text=True, timeout=30)
    assert r.stdout.strip() == "ok", r.stderr
