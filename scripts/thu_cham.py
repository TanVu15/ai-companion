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
    pg.evaluate("meo.dat('bep', true)"); pg.wait_for_timeout(300)  # nằm bẹp mà chạm đuôi quấn quanh người → đuôi khẽ vẫy, vẫn nằm
    pg.mouse.click(X(108), Y(187)); pg.wait_for_timeout(60)
    kq.append(("nằm bẹp, chạm đuôi quấn → khẽ vẫy, vẫn nằm", co("vay-duoi-ngu") and co("bep") and not co("rut-chan")))
    pg.evaluate("meo.dat('bep', false)"); nghi()
    pg.mouse.click(X(118), Y(174)); pg.wait_for_timeout(120); pg.mouse.click(X(118), Y(174)); pg.wait_for_timeout(60)
    kq.append(("đập tay", co("dap-tay"))); nghi()
    pg.mouse.click(X(100), Y(145)); pg.wait_for_timeout(60); kq.append(("chọc bụng", co("giat"))); nghi()
    pg.mouse.move(X(100), Y(80)); pg.mouse.move(X(101), Y(89)); pg.wait_for_timeout(1100)
    kq.append(("ngửi tay", co("ngui"))); pg.mouse.move(X(100), Y(150)); nghi()
    pg.mouse.move(X(100), Y(145)); pg.mouse.down(); pg.wait_for_timeout(900); kq.append(("nhấn giữ lăn", co("lan")))
    pg.mouse.up(); pg.wait_for_timeout(3400)
    pg.mouse.move(X(100), Y(55)); pg.mouse.down(); pg.wait_for_timeout(550)
    for i in range(1, 9):
        pg.mouse.move(X(100), Y(55) - 12 * i); pg.wait_for_timeout(30)
    dang_be = co("be"); pg.wait_for_timeout(2700); em = co("em"); pg.mouse.up(); pg.wait_for_timeout(100)
    kq.append(("bế Bơ lên, bế yên thì lim dim, thả ra", dang_be and em and not co("be") and not co("em") and co("roi"))); nghi()
    pg.mouse.click(X(100), Y(88)); pg.wait_for_timeout(150); kq.append(("boop mũi", co("boop"))); nghi()
    pg.mouse.click(X(138), Y(92)); pg.wait_for_timeout(150); kq.append(("nựng má", co("nung-ma-phai"))); nghi()
    pg.mouse.move(X(5), Y(5))
    for i in range(110):  # vuốt lưng liền ~6,6 giây → nhồi bột
        pg.mouse.move(X(60 + (i % 2) * 80), Y(130)); pg.wait_for_timeout(60)
    kq.append(("vuốt lâu → nhồi bột", co("nhoi"))); pg.mouse.move(5, 5); pg.wait_for_timeout(1200)
    kq.append(("vuốt xong → chớp mắt chậm", co("chop-cham"))); nghi()
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
    for i in range(8):  # chấm đứng yên trên cao, phía trên đầu → ke ke ke; kéo chấm xuống thì thôi
        pg.mouse.move(X(60 + i * 5), Y(0)); pg.wait_for_timeout(30)
    pg.wait_for_timeout(1500); kk = co("ke-ke"); pg.mouse.move(X(170), Y(120)); pg.wait_for_timeout(100)
    kq.append(("laser đứng yên trên cao → ke ke ke", kk and not co("ke-ke"))); nghi()
    for i in range(10):  # chấm đứng yên trước chân → rình, vồ đè lên, nhấc chân ngó
        pg.mouse.move(X(140 - i * 4), Y(189)); pg.wait_for_timeout(30)
    cho = lambda c, ms: any(co(c) or pg.wait_for_timeout(100) for _ in range(ms // 100))  # noqa: E731  (đợi tới khi có lớp c)
    kq.append(("laser đứng yên trước chân → rình, vồ, ngó", cho("rinh", 2000) and cho("vo-rinh", 2000) and cho("ngo-chan", 1500)))
    pg.wait_for_timeout(1500)
    pg.click('#doChoi'); pg.wait_for_timeout(300)  # vừa vồ trúng chấm laser, cất laser rồi vuốt đầu → Bơ khoe
    for i in range(8):
        pg.mouse.move(X(70 + (i % 2) * 60), Y(60)); pg.wait_for_timeout(40)
    kq.append(("vừa vồ trúng mà vuốt → khoe", co("khoe"))); pg.mouse.move(5, 5); pg.wait_for_timeout(1900)
    pg.click('#doChoi'); pg.wait_for_timeout(300)
    pg.click('#cuonLen'); pg.wait_for_timeout(300)
    kq.append(("cuộn len (cất laser)", pg.evaluate("!!document.querySelector('.len') && !document.querySelector('.laser')")))
    pg.wait_for_timeout(2200); l = pg.locator('.len').bounding_box()  # đặt len nằm yên sát bên Bơ → ôm, cắn, đá ra
    pg.mouse.move(l['x'] + 15, l['y'] + 15); pg.mouse.down()
    for i in range(1, 11):
        pg.mouse.move(l['x'] + 15 + (X(20) - l['x'] - 15) * i / 10, l['y'] + 15 + (Y(175) - l['y'] - 15) * i / 10); pg.wait_for_timeout(30)
    for _ in range(8):
        pg.mouse.move(X(20), Y(175)); pg.wait_for_timeout(30)
    pg.mouse.up(); pg.mouse.move(5, 5)
    om = cho("om-len", 4000); da = cho("da-len", 3500)
    kq.append(("len nằm yên sát bên → ôm rồi đá ra", om and da and not co("om-len")))
    pg.wait_for_timeout(1500)  # lăn len ngang sàn qua trước mặt Bơ → đầu quay theo, đuôi giật
    kh = pg.evaluate("(()=>{const b=document.querySelector('.len').parentElement.getBoundingClientRect();return [b.left,b.top,b.width,b.height]})()")
    l = pg.locator('.len').bounding_box(); x0, fy = kh[0] + 18, kh[1] + kh[3] - 16
    pg.mouse.move(l['x'] + 15, l['y'] + 15); pg.mouse.down()
    for i in range(1, 9):
        pg.mouse.move(l['x'] + 15 + (x0 - l['x'] - 15) * i / 8, l['y'] + 15 + (fy - l['y'] - 15) * i / 8); pg.wait_for_timeout(30)
    for _ in range(10):
        pg.mouse.move(x0, fy); pg.wait_for_timeout(30)
    for i in range(1, 5):
        pg.mouse.move(x0 + 10 * i, fy); pg.wait_for_timeout(16)
    pg.mouse.up(); pg.mouse.move(5, 5)
    kq.append(("len lăn qua trước mặt → quay đầu nhìn theo", cho("theo-len", 600)))
    pg.wait_for_timeout(1000)  # ném len từ mép phải lăn vào đuôi → đuôi vểnh, Bơ ngoái lại nhìn đuôi (không vồ)
    l = pg.locator('.len').bounding_box(); x1 = min(X(224), kh[0] + kh[2] - 18)
    pg.mouse.move(l['x'] + 15, l['y'] + 15); pg.mouse.down()
    for i in range(1, 9):
        pg.mouse.move(l['x'] + 15 + (x1 - l['x'] - 15) * i / 8, l['y'] + 15 + (fy - l['y'] - 15) * i / 8); pg.wait_for_timeout(30)
    for _ in range(100):  # cầm len chờ ~3 giây (len lăn ngược về có thể vừa chạm đuôi: đợi hết lúc nghỉ)
        pg.mouse.move(x1, fy); pg.wait_for_timeout(30)
    for i in range(1, 5):
        pg.mouse.move(x1 - 8 * i, fy); pg.wait_for_timeout(16)
    pg.mouse.up(); pg.mouse.move(5, 5)
    kq.append(("len lăn chạm đuôi → ngoái lại nhìn đuôi", cho("ngoai-duoi", 1500)))
    pg.click('#longVu'); pg.wait_for_timeout(300); kq.append(("lông vũ", pg.evaluate("!!document.querySelector('.long-vu')")))
    for i in range(8):
        pg.mouse.move(X(100), Y(120 + i * 8) + 10); pg.wait_for_timeout(30)
    pg.wait_for_timeout(600); rinh = co("rinh"); pg.wait_for_timeout(1000)
    kq.append(("lông vũ sát đất → rình rồi vồ", rinh and co("vo-rinh") and not co("rinh")))
    pg.wait_for_timeout(2500)
    for i in range(16):
        pg.mouse.move(X(15) + (i % 2) * 6, Y(100) + 10); pg.wait_for_timeout(60)
    kq.append(("lông vũ bên hông → quơ chân", co("quo-trai")))
    pg.mouse.move(X(150), Y(120) + 10); pg.wait_for_timeout(3200)  # (đường về đã lướt qua bụng: đợi hết lúc nghỉ) lông lướt ngang qua lưng/bụng → nhột, lông rùng
    for i in range(8):
        pg.mouse.move(X(150 - i * 8), Y(120) + 10); pg.wait_for_timeout(40)
    kq.append(("lông vũ lướt qua lưng → nhột", co("nhot-long")))
    pg.mouse.move(X(184), Y(60) + 10); pg.wait_for_timeout(2700)  # (đường sang có thể vừa quét qua đuôi: đợi hết lúc nghỉ 2,5 giây) lông quét nhanh lên xuống qua đuôi → đuôi quất theo lông
    qd = False
    for i in range(12):
        pg.mouse.move(X(184), Y(70 + (i % 6) * 14) + 10); pg.wait_for_timeout(40); qd = qd or co("quat-duoi")
    if not qd: print("   (lớp trên mèo:", pg.evaluate(CLS), "| cảm xúc:", pg.evaluate("document.querySelector('#face').dataset.e"), ")")
    kq.append(("lông vũ quét qua đuôi → đuôi quất theo", qd))
    if co("quat-duoi"):  # đang quất đuôi mà lông bay lên đầu → Bơ vồ, bỏ tư thế quất đuôi (không lẫn hai tư thế)
        for i in range(6):
            pg.mouse.move(X(100), Y(40 - i * 4) + 10); pg.wait_for_timeout(40)
        kq.append(("đang quất đuôi, lông lên đầu → vồ, thôi quất đuôi", co("voi") and not co("quat-duoi")))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
    kq.append(("Esc cất đồ chơi", pg.evaluate("!document.querySelector('.long-vu, .len, .laser')")))
    pg.focus('#face'); pg.keyboard.press('d'); pg.wait_for_timeout(60); kq.append(("phím D", co("dap-tay"))); nghi()
    pg.keyboard.press('n'); pg.wait_for_timeout(60); kq.append(("phím N (boop)", co("boop"))); nghi()
    pg.keyboard.down('b'); pg.wait_for_timeout(100); dang_be = co("be"); pg.keyboard.up('b'); pg.wait_for_timeout(60)
    kq.append(("giữ phím B (bế)", dang_be and not co("be"))); nghi()
    pg.fill('#input', 'tối nay ăn cá'); pg.keyboard.press('Enter'); pg.wait_for_timeout(300)
    kq.append(("tin có chữ cá", co("liem-mep")))
    pg.wait_for_timeout(3000); pg.fill('#input', 'buồn ngủ quá'); pg.keyboard.press('Enter'); pg.wait_for_timeout(300)
    kq.append(("tin buồn ngủ → ngáp lây", co("ngap")))
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
