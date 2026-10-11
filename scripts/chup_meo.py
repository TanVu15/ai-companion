"""Chụp ảnh mèo Bơ để kiểm tra giao diện (không cần API key, dữ liệu tạm, không đụng data/).

Chạy:  python scripts/chup_meo.py [thư_mục_ảnh]     (mặc định docs/anh)
Cần: playwright (pip install playwright) và Chromium.
Ra: trang-dien-thoai.png (390×800), trang-may-tinh.png (1100×800), meo-<cảm xúc>.png, meo-<hành động>.png,
     meo-tat-ca.png (mọi cảm xúc trên một tấm).
"""
import base64
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from app import config  # noqa: E402

TRANG_THAI = config.EMOTIONS + ["ngu"]
# (Ảnh chụp cả trang cho PROGRESS.md đừng đặt tên meo-<tư thế>.png: script này sẽ ghi đè.)
TRANG_THAI_NHO = ["ngap", "liem", "cho", "lan", "mung", "bep", "hong", "nghe", "nguoc-long", "dap-tay", "rua-mat", "chong-mat",
                  "hat-xi", "boop", "nung-ma-trai", "be", "dinh-sua", "rinh", "vo-rinh", "nhoi"]


def cong_trong():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    port, tmp = cong_trong(), tempfile.mkdtemp()
    env = {**os.environ, "DEMO": "1", "DB_PATH": str(Path(tmp) / "c.db")}
    srv = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--port", str(port)],
                           cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = f"http://127.0.0.1:{port}/"
    try:
        for _ in range(50):
            try:
                socket.create_connection(("127.0.0.1", port), 0.2).close()
                break
            except OSError:
                time.sleep(0.2)
        with sync_playwright() as p:
            b = p.chromium.launch()
            for ten, w, h in [("dien-thoai", 390, 800), ("may-tinh", 1100, 800)]:
                pg = b.new_page(viewport={"width": w, "height": h}, reduced_motion="reduce")
                pg.goto(url); pg.wait_for_timeout(800)
                pg.screenshot(path=out / f"trang-{ten}.png")
                pg.close()
            pg = b.new_page(viewport={"width": 390, "height": 800}, reduced_motion="reduce", device_scale_factor=2)
            pg.goto(url); pg.wait_for_timeout(500)
            face = pg.locator("#face")
            for e in TRANG_THAI:
                pg.evaluate("e => { face.dataset.e = e; face.className = 'face'; }", e)
                pg.wait_for_timeout(450)
                face.screenshot(path=out / f"meo-{e}.png")
            pg.evaluate("() => { face.dataset.e = 'binh_thuong'; }")
            for c in TRANG_THAI_NHO:
                pg.evaluate("c => { const s = face.querySelector('svg'); s.classList.add(c); s.style.setProperty('--nhac', 1); }", c)  # bế: nhấc hẳn lên, chân thòng vẫn nằm trong khung
                pg.wait_for_timeout(450)
                face.screenshot(path=out / f"meo-{c}.png")
                pg.evaluate("c => face.querySelector('svg').classList.remove(c)", c)
            # Một tấm gom mọi cảm xúc, để Tân xem nhanh trên GitHub
            html = "".join(
                f'<figure><img src="data:image/png;base64,{base64.b64encode((out / f"meo-{e}.png").read_bytes()).decode()}">'
                f'<figcaption>{e}</figcaption></figure>'
                for e in TRANG_THAI + TRANG_THAI_NHO)
            pg2 = b.new_page(viewport={"width": 1000, "height": 400})
            pg2.set_content("<style>body{margin:0;display:flex;flex-wrap:wrap;gap:8px;padding:12px;background:#f6f3ee;"
                            "font:14px system-ui}figure{margin:0;text-align:center}img{width:150px}</style>" + html)
            pg2.wait_for_timeout(300)
            pg2.screenshot(path=out / "meo-tat-ca.png", full_page=True)
            b.close()
    finally:
        srv.terminate()
    print("Đã chụp vào", out)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "anh")
