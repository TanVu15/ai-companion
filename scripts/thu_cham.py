"""Thử nhanh mọi trò chạm & chơi bằng trình duyệt thật (Playwright + Chromium), không cần API key.

Chạy:  python scripts/thu_cham.py
In ra từng trò: ĐẠT / LỖI. Dùng sau khi sửa web/choi.js, do_choi.js, meo.js để chắc không hỏng trò nào.
Máy chủ chạy DEMO=1 với dữ liệu tạm (không đụng data/).
"""
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CLS = "[...document.querySelector('#face svg').classList].join(' ')"


def cong_trong():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def thu(pg, ten, w, h):
    kq = []
    f = pg.locator('#face').bounding_box()
    k = f['width'] / 200
    X = lambda x: f['x'] + x * k  # noqa: E731  (tọa độ khung vẽ 200×192 → màn hình)
    Y = lambda y: f['y'] + y * k  # noqa: E731
    co = lambda c: c in pg.evaluate(CLS).split()  # noqa: E731
    nghi = lambda: pg.wait_for_timeout(1700)  # noqa: E731

    def keo(x0, y0, x1, y1, buoc=10):
        pg.mouse.move(X(x0), Y(y0)); pg.mouse.down()
        for i in range(1, buoc + 1):
            pg.mouse.move(X(x0 + (x1 - x0) * i / buoc), Y(y0 + (y1 - y0) * i / buoc)); pg.wait_for_timeout(25)

    keo(70, 60, 130, 60); kq.append(("vuốt đầu", co("vuot"))); pg.mouse.up(); nghi()
    keo(42, 160, 42, 110); kq.append(("vuốt ngược lông", co("nguoc-long"))); pg.mouse.up(); nghi()
    pg.mouse.click(X(52), Y(25)); pg.wait_for_timeout(60); kq.append(("chạm tai", co("giat-tai-trai"))); nghi()
    pg.mouse.click(X(186), Y(105)); pg.wait_for_timeout(60); kq.append(("chạm đuôi", co("giat-duoi"))); nghi()
    pg.mouse.click(X(118), Y(174)); pg.wait_for_timeout(120); pg.mouse.click(X(118), Y(174)); pg.wait_for_timeout(60)
    kq.append(("đập tay", co("dap-tay"))); nghi()
    pg.mouse.click(X(100), Y(145)); pg.wait_for_timeout(60); kq.append(("chọc bụng", co("giat"))); nghi()
    pg.mouse.move(X(100), Y(80)); pg.mouse.move(X(101), Y(89)); pg.wait_for_timeout(1100)
    kq.append(("ngửi tay", co("ngui"))); pg.mouse.move(X(100), Y(150)); nghi()
    pg.mouse.move(X(100), Y(145)); pg.mouse.down(); pg.wait_for_timeout(900); kq.append(("nhấn giữ lăn", co("lan")))
    pg.mouse.up(); pg.wait_for_timeout(3400)
    pg.click('#choAn'); pg.wait_for_timeout(200); kq.append(("cho ăn", co("an"))); pg.wait_for_timeout(4200)
    b = pg.locator('#choAn').bounding_box()
    pg.mouse.move(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); pg.mouse.down(); pg.wait_for_timeout(700); pg.mouse.up()
    mo = pg.is_visible('#menuAn'); pg.wait_for_timeout(300); chua_an = not co("an")
    pg.click('#menuAn [data-mon="sua"]'); pg.wait_for_timeout(2900)
    kq.append(("nhấn giữ nút cá → chọn sữa", mo and chua_an and co("dinh-sua") and not pg.is_visible('#menuAn')))
    pg.wait_for_timeout(1400)
    pg.click('#choAn'); pg.wait_for_timeout(2900)  # bấm thường: vẫn là món vừa chọn
    kq.append(("bấm lại nhớ món sữa", co("dinh-sua") and 'sữa' in (pg.get_attribute('#choAn', 'aria-label') or '')))
    pg.evaluate("localStorage.removeItem('bo_mon_an')"); pg.wait_for_timeout(1400)
    pg.click('#doChoi'); pg.wait_for_timeout(150); kq.append(("laser", pg.evaluate("!!document.querySelector('.laser')")))
    pg.click('#cuonLen'); pg.wait_for_timeout(300)
    kq.append(("cuộn len (cất laser)", pg.evaluate("!!document.querySelector('.len') && !document.querySelector('.laser')")))
    pg.click('#longVu'); pg.wait_for_timeout(300); kq.append(("lông vũ", pg.evaluate("!!document.querySelector('.long-vu')")))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
    kq.append(("Esc cất đồ chơi", pg.evaluate("!document.querySelector('.long-vu, .len, .laser')")))
    pg.focus('#face'); pg.keyboard.press('d'); pg.wait_for_timeout(60); kq.append(("phím D", co("dap-tay"))); nghi()
    pg.fill('#input', 'tối nay ăn cá'); pg.keyboard.press('Enter'); pg.wait_for_timeout(300)
    kq.append(("tin có chữ cá", co("liem-mep")))
    return kq


def main():
    port, tmp = cong_trong(), tempfile.mkdtemp()
    env = {**os.environ, "DEMO": "1", "DB_PATH": str(Path(tmp) / "c.db")}
    srv = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--port", str(port)],
                           cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    hong = 0
    try:
        for _ in range(50):
            try:
                socket.create_connection(("127.0.0.1", port), 0.2).close()
                break
            except OSError:
                time.sleep(0.2)
        with sync_playwright() as p:
            b = p.chromium.launch()
            for ten, w, h in [("điện thoại", 390, 800), ("máy tính", 1100, 800)]:
                pg = b.new_page(viewport={"width": w, "height": h})
                loi = []
                pg.on("pageerror", lambda e: loi.append(str(e)))
                pg.goto(f"http://127.0.0.1:{port}/"); pg.wait_for_timeout(800)
                print(f"--- {ten} ({w}×{h})")
                for tro, dat in thu(pg, ten, w, h):
                    print(("  ĐẠT " if dat else "  LỖI ") + tro)
                    hong += not dat
                for e in loi:
                    print("  LỖI trang:", e); hong += 1
                pg.close()
            b.close()
    finally:
        srv.terminate()
    print("Xong:", "mọi trò đều chạy" if not hong else f"{hong} chỗ hỏng")
    sys.exit(1 if hong else 0)


if __name__ == "__main__":
    main()
