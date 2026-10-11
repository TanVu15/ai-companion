// Đồ chơi của mèo Bơ: tia laser, cuộn len, cần câu lông vũ (tách từ choi.js cho dễ sửa). Chạy trên trình duyệt, KHÔNG gọi API.
// Mỗi lúc chỉ một đồ chơi; 15–20 giây không đụng thì tự cất; Esc cất; phím mũi tên điều khiển.
// Cần choi.js chạy trước (dùng chung window.boChoi: giu, noi, dem...).

// ---- Phần tính toán thuần (test được bằng node) ----
// Một bước vật lý của cuộn len trong khung rộng w, cao h (px; gốc ở góc trên trái), dt giây.
// Rơi theo trọng lực, nảy ở tường/sàn (mất bớt sức), lăn trên sàn chậm dần. Trả về trạng thái mới (không sửa cái cũ).
function boBuocLen(s, dt, w, h, r = 15) {
  let { x, y, vx, vy, goc = 0 } = s;
  vy += 1400 * dt;
  x += vx * dt; y += vy * dt;
  if (x < r) { x = r; vx = Math.abs(vx) * 0.7; }
  if (x > w - r) { x = w - r; vx = -Math.abs(vx) * 0.7; }
  if (y < r) { y = r; vy = Math.abs(vy) * 0.5; }
  const sat = y >= h - r;
  if (sat) {
    y = h - r;
    vy = Math.abs(vy) > 120 ? -Math.abs(vy) * 0.55 : 0;  // nảy, nhỏ quá thì nằm yên trên sàn
    vx *= Math.pow(0.35, dt);                           // ma sát sàn
    if (Math.abs(vx) < 4) vx = 0;
  }
  goc += vx * dt / r * 57.3;                            // lăn: xoay theo quãng đi
  return { x, y, vx, vy, goc, yen: sat && vx === 0 && vy === 0 };
}

// Cuộn len nằm yên đè lên nút (cá, laser...) thì che mất nút, bấm không được → trả về hướng lăn ra (về phía giữa khung), không đè thì 0.
// nut: danh sách khung chữ nhật {x, y, w, h} (px, cùng gốc với cuộn len); giua: hoành độ giữa khung.
function boLenDeNut(x, y, nut, giua, r = 15) {
  const de = (nut || []).some(n => x + r > n.x && x - r < n.x + n.w && y + r > n.y && y - r < n.y + n.h);
  return de ? (x < giua ? 1 : -1) : 0;
}

// Lông vũ (đầu lông, tọa độ khung vẽ 200×192 của mèo) đang sát đất ngay trước mặt Bơ? (chân Bơ ở y≈174, đất ≈184)
// Ở yên vùng này một lúc thì Bơ hạ người rình, ngoáy mông rồi nhảy vồ
function boLongVuRinh(x, y) {
  return y >= 165 && y <= 250 && Math.abs(x - 100) <= 95;
}

if (typeof module !== 'undefined') module.exports = { boBuocLen, boLenDeNut, boLongVuRinh };

// ---- Phần giao diện ----
(function () {
  if (typeof document === 'undefined' || !window.boChoi) return;
  const { face, khung, svg, nhin, header, giu, noi, dem, dangDoi, conChoi, doChoi } = window.boChoi;
  const { boVungCham, boHuongNhin, boGanMui } = window;
  const boLongVuRinh_ = typeof boLongVuRinh === 'function' ? boLongVuRinh : () => false;

  // ---- Tia laser: chấm đỏ theo ngón tay/chuột trong vùng quanh mèo; mèo nhìn theo, chấm tới gần thì vồ ----
  const nutLaser = document.getElementById('doChoi');
  let laserBat = false, cham_ = null, voCuoi = 0, laserTat = null;
  function batLaser(bat) {
    laserBat = bat;
    nutLaser.setAttribute('aria-pressed', bat);
    header.classList.toggle('dang-laser', bat);
    if (bat) {
      batLen(false);
      batLongVu(false);
      cham_ = document.createElement('span'); cham_.className = 'laser';
      header.appendChild(cham_);
      const r = header.getBoundingClientRect();
      datLaser(r.left + r.width * 0.8, r.top + 40);
      noi('laser', true); henTatLaser();
    } else {
      if (cham_) cham_.remove(); cham_ = null;
      if (nhin) nhin.removeAttribute('transform');
      clearTimeout(laserTat);
    }
  }
  function henTatLaser() { clearTimeout(laserTat); laserTat = setTimeout(() => batLaser(false), 15000); }
  function datLaser(cx, cy) {
    if (!cham_) return;
    conChoi();
    const r = header.getBoundingClientRect();
    cham_.style.left = (cx - r.left) + 'px'; cham_.style.top = (cy - r.top) + 'px';
    // mắt nhìn theo
    const m = svg.getScreenCTM();
    if (m && nhin) {
      const p = new DOMPoint(cx, cy).matrixTransform(m.inverse());
      const dx = p.x - 100, dy = p.y - 74, dai = Math.hypot(dx, dy) || 1;
      nhin.setAttribute('transform', `translate(${(dx / dai * 4).toFixed(1)} ${(dy / dai * 3).toFixed(1)})`);
      // chấm đỏ chạy vào người mèo → vồ (nghỉ 1,2 giây giữa hai lần)
      if (boVungCham(p.x, p.y) && Date.now() - voCuoi > 1200) {
        voCuoi = Date.now(); giu('vo', 600); dem('laser'); noi('laser');
      }
    }
  }
  nutLaser.addEventListener('click', ev => { ev.stopPropagation(); batLaser(!laserBat); });
  header.addEventListener('pointermove', ev => {
    if (!laserBat || ev.target.closest('button')) return;
    datLaser(ev.clientX, ev.clientY); henTatLaser();
  });
  header.addEventListener('pointerdown', ev => {
    if (!laserBat || ev.target.closest('button')) return;
    datLaser(ev.clientX, ev.clientY); henTatLaser();
  });
  document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && laserBat) batLaser(false); });

  // ---- Cuộn len: kéo rồi ném; len lăn, nảy; chạm vào người Bơ thì Bơ vồ, đập văng ra. 20 giây không đụng thì cất ----
  const nutLen = document.getElementById('cuonLen');
  let len = null, lenS = null, lenVong = 0, lenTruoc = 0, lenKeo = null, lenTat = null, voLen = 0;
  function henCatLen() { clearTimeout(lenTat); lenTat = setTimeout(() => batLen(false), 20000); }
  function veLen() { len.style.transform = `translate(${lenS.x.toFixed(1)}px, ${lenS.y.toFixed(1)}px) rotate(${(lenS.goc % 360).toFixed(0)}deg)`; }
  function chayLen() { if (!lenVong && len) { lenTruoc = 0; lenVong = requestAnimationFrame(buocLen); } }
  function buocLen(t) {
    lenVong = 0;
    if (!len) return;
    const dt = lenTruoc ? Math.min(0.04, (t - lenTruoc) / 1000) : 0.016; lenTruoc = t;
    if (!lenKeo) lenS = boBuocLen(lenS, dt, khung.clientWidth, khung.clientHeight);
    veLen(); lenChamMeo();
    if (lenS.yen && !lenKeo) lenTranhNut();
    if (!lenS.yen || lenKeo) lenVong = requestAnimationFrame(buocLen);
  }
  // Len nằm yên đè lên nút → tự lăn nhẹ vào giữa cho khỏi che nút
  function lenTranhNut() {
    const r = khung.getBoundingClientRect();
    const nut = [...khung.querySelectorAll('.nut-meo')].map(b => {
      const q = b.getBoundingClientRect(); return { x: q.left - r.left, y: q.top - r.top, w: q.width, h: q.height };
    });
    const huong = boLenDeNut(lenS.x, lenS.y, nut, khung.clientWidth / 2);
    if (huong) lenS = { ...lenS, vx: huong * 170, yen: false };
  }
  // Len chạm người Bơ → vồ: Bơ đập len văng ra xa (nghỉ 0,9 giây giữa hai lần vồ)
  function lenChamMeo() {
    const m = svg.getScreenCTM(); if (!m) return;
    const r = khung.getBoundingClientRect();
    const p = new DOMPoint(r.left + lenS.x, r.top + lenS.y).matrixTransform(m.inverse());
    if (nhin && face.dataset.e !== 'ngu') {
      const [tx, ty] = boHuongNhin(p.x - 100, p.y - 74); nhin.setAttribute('transform', `translate(${tx} ${ty})`);
    }
    if (lenKeo || !boVungCham(p.x, p.y) || Date.now() - voLen < 900 || dangDoi() || face.dataset.e === 'ngu') return;
    voLen = Date.now(); giu('vo', 600); dem('len'); noi('len'); conChoi();
    const huong = p.x < 100 ? -1 : 1;
    lenS = { ...lenS, vx: huong * (260 + Math.random() * 200), vy: -380 - Math.random() * 200 };
  }
  function batLen(bat) {
    if (bat === !!len) return;
    nutLen.setAttribute('aria-pressed', bat);
    if (bat) {
      if (laserBat) batLaser(false);
      batLongVu(false);
      len = document.createElement('span'); len.className = 'len'; len.innerHTML = nutLen.innerHTML;
      khung.appendChild(len);
      lenS = { x: khung.clientWidth - 30, y: 20, vx: -160, vy: 0, goc: 0 };
      veLen(); chayLen(); noi('len', true); henCatLen();
      len.addEventListener('pointerdown', ev => {
        ev.preventDefault(); ev.stopPropagation();
        try { len.setPointerCapture(ev.pointerId); } catch (e) {}
        const r = khung.getBoundingClientRect();
        lenKeo = { dx: ev.clientX - r.left - lenS.x, dy: ev.clientY - r.top - lenS.y, t: performance.now(), x: lenS.x, y: lenS.y, vx: 0, vy: 0 };
        chayLen(); henCatLen();
      });
      len.addEventListener('pointermove', ev => {
        if (!lenKeo) return;
        const r = khung.getBoundingClientRect(), bayGio = performance.now();
        const x = Math.max(15, Math.min(khung.clientWidth - 15, ev.clientX - r.left - lenKeo.dx));
        const y = Math.max(15, Math.min(khung.clientHeight - 15, ev.clientY - r.top - lenKeo.dy));
        const dt = Math.max(0.008, (bayGio - lenKeo.t) / 1000);
        lenKeo.vx = 0.6 * lenKeo.vx + 0.4 * (x - lenKeo.x) / dt; lenKeo.vy = 0.6 * lenKeo.vy + 0.4 * (y - lenKeo.y) / dt;
        lenKeo.x = x; lenKeo.y = y; lenKeo.t = bayGio;
        lenS = { ...lenS, x, y, vx: 0, vy: 0, goc: lenS.goc + (x - lenS.x) / 15 * 57.3 };
      });
      const tha = () => {
        if (!lenKeo) return;
        const gioiHan = v => Math.max(-1600, Math.min(1600, v || 0));
        lenS = { ...lenS, vx: gioiHan(lenKeo.vx), vy: gioiHan(lenKeo.vy), yen: false };
        lenKeo = null; chayLen();
      };
      len.addEventListener('pointerup', tha); len.addEventListener('pointercancel', tha);
    } else {
      cancelAnimationFrame(lenVong); lenVong = 0; clearTimeout(lenTat);
      len.remove(); len = null; lenKeo = null;
      if (nhin) nhin.removeAttribute('transform');
    }
  }
  nutLen.addEventListener('click', ev => { ev.stopPropagation(); batLen(!len); });
  document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && len) batLen(false); });

  // ---- Cần câu lông vũ: lông treo dây, lắc lư theo ngón tay/chuột trong vùng quanh Bơ; lông ở trên đầu thì Bơ đứng lên vồ ----
  const nutLongVu = document.getElementById('longVu');
  let lv = null, lvPos = null, lvDich = null, lvVong = 0, lvTat = null, lvNoi = 0, lvHatXi = 0;
  let lvRinh = null, lvVoRinh = 0;  // đang rình (hẹn giờ nhảy vồ), lần vồ gần nhất
  // Thôi rình (lông đi chỗ khác, cất lông, Bơ dỗi/ngủ...)
  function boRinh() { clearTimeout(lvRinh); lvRinh = null; svg.classList.remove('rinh'); }
  // Lông sát đất trước mặt: Bơ hạ người, mông ngoáy ngoáy; 1,4 giây sau nhảy vồ (nghỉ 3 giây giữa hai lần vồ)
  function rinhLongVu(trongVung) {
    const ranh = trongVung && !dangDoi() && face.dataset.e !== 'ngu' && Date.now() - lvVoRinh > 3000;
    if (!ranh) { if (lvRinh) boRinh(); return; }
    if (lvRinh) return;
    svg.classList.add('rinh'); conChoi(); noi('rinh');
    lvRinh = setTimeout(() => {
      lvRinh = null; svg.classList.remove('rinh');
      if (!lv || dangDoi() || face.dataset.e === 'ngu' || document.hidden) return;
      lvVoRinh = Date.now(); giu('vo-rinh', 700); conChoi(); dem('rinh'); noi('vo_rinh', true);
      if (navigator.vibrate && !matchMedia('(prefers-reduced-motion: reduce)').matches) { try { navigator.vibrate(18); } catch (e) {} }
    }, 1400);
  }
  function henTatLongVu() { clearTimeout(lvTat); lvTat = setTimeout(() => batLongVu(false), 15000); }
  function buocLongVu() {
    lvVong = 0;
    if (!lv) return;
    const vx = (lvDich.x - lvPos.x) * 0.14, vy = (lvDich.y - lvPos.y) * 0.14;
    lvPos = { x: lvPos.x + vx, y: lvPos.y + vy };
    lv.style.transform = `translate(${lvPos.x.toFixed(1)}px, ${lvPos.y.toFixed(1)}px) rotate(${Math.max(-35, Math.min(35, -vx * 3)).toFixed(1)}deg)`;
    const m = svg.getScreenCTM();
    if (m) {
      const r = header.getBoundingClientRect();
      const p = new DOMPoint(r.left + lvPos.x, r.top + lvPos.y + 20).matrixTransform(m.inverse());
      if (nhin && face.dataset.e !== 'ngu') { const [tx, ty] = boHuongNhin(p.x - 100, p.y - 74); nhin.setAttribute('transform', `translate(${tx} ${ty})`); }
      // lông quét ngang mũi → lâu lâu Bơ hắt xì (nghỉ 6 giây giữa hai lần)
      if (boGanMui(p.x, p.y) && Date.now() - lvHatXi > 6000 && !dangDoi() && face.dataset.e !== 'ngu') {
        lvHatXi = Date.now(); giu('hat-xi', 900); noi('hat_xi', true); conChoi();
      }
      // lông ở phía trên đầu, ngang tầm với của chân → đứng lên vồ
      if (p.y > -30 && p.y < 45 && Math.abs(p.x - 100) < 65 && !dangDoi() && face.dataset.e !== 'ngu') {
        giu('voi', 500); conChoi();
        if (Date.now() - lvNoi > 1500) { lvNoi = Date.now(); dem('long_vu'); noi('long_vu'); }
      }
      rinhLongVu(boLongVuRinh_(p.x, p.y));
    }
    if (Math.abs(vx) + Math.abs(vy) > 0.05) lvVong = requestAnimationFrame(buocLongVu);
  }
  function chayLongVu() { if (!lvVong && lv) lvVong = requestAnimationFrame(buocLongVu); }
  function batLongVu(bat) {
    if (bat === !!lv) return;
    nutLongVu.setAttribute('aria-pressed', bat);
    header.classList.toggle('dang-long-vu', bat);
    if (bat) {
      if (laserBat) batLaser(false);
      batLen(false);
      lv = document.createElement('span'); lv.className = 'long-vu';
      lv.innerHTML = '<svg viewBox="0 0 24 24"><path d="M12,2 C6,6 6,16 12,23 C18,16 18,6 12,2 Z" fill="#6cc3b0" stroke="#3a8a78" stroke-width="1.2"/><path d="M12,4 L12,22 M12,9 L8,7 M12,9 L16,7 M12,14 L7.5,12 M12,14 L16.5,12" fill="none" stroke="#3a8a78" stroke-width=".9" stroke-linecap="round"/></svg>';
      header.appendChild(lv);
      const fr = face.getBoundingClientRect(), r = header.getBoundingClientRect();
      lvPos = { x: fr.left - r.left + fr.width * 0.85, y: 6 };
      lvDich = { x: fr.left - r.left + fr.width * 0.6, y: fr.top - r.top + 4 };
      chayLongVu(); noi('long_vu', true); henTatLongVu();
    } else {
      cancelAnimationFrame(lvVong); lvVong = 0; clearTimeout(lvTat); boRinh();
      lv.remove(); lv = null;
      if (nhin) nhin.removeAttribute('transform');
    }
  }
  function dichLongVu(ev) {
    if (!lv || ev.target.closest('button')) return;
    const r = header.getBoundingClientRect();
    lvDich = { x: ev.clientX - r.left, y: ev.clientY - r.top - 30 };  // lông treo cao hơn ngón tay một chút cho khỏi che
    chayLongVu(); henTatLongVu();
  }
  nutLongVu.addEventListener('click', ev => { ev.stopPropagation(); batLongVu(!lv); });
  header.addEventListener('pointermove', dichLongVu);
  header.addEventListener('pointerdown', dichLongVu);
  document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && lv) batLongVu(false); });

  // ---- Đồ chơi bằng bàn phím: mũi tên di chuyển chấm laser / lông vũ, hoặc hất cuộn len (khi không đang gõ chữ) ----
  document.addEventListener('keydown', ev => {
    const huong = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] }[ev.key];
    if (!huong || !(laserBat || len || lv) || ev.target.closest('input, textarea, select, dialog')) return;
    ev.preventDefault();
    const [dx, dy] = huong, r = header.getBoundingClientRect();
    if (laserBat && cham_) {
      const x = parseFloat(cham_.style.left) || 0, y = parseFloat(cham_.style.top) || 0;
      datLaser(r.left + Math.max(0, Math.min(r.width, x + dx * 24)), r.top + Math.max(0, Math.min(r.height, y + dy * 24)));
      henTatLaser();
    } else if (lv) {
      lvDich = { x: Math.max(0, Math.min(r.width, lvDich.x + dx * 24)), y: Math.max(-20, Math.min(r.height, lvDich.y + dy * 24)) };
      chayLongVu(); henTatLongVu();
    } else if (len && !lenKeo) {
      const giua = khung.clientWidth / 2;
      lenS = { ...lenS, vx: dx ? dx * 450 : (giua - lenS.x) * 2, vy: dy < 0 ? -750 : dy > 0 ? 300 : -250, yen: false };
      chayLen(); henCatLen();
    }
  });

  // Cho choi.js biết đang chơi gì: đang có đồ chơi thì mắt khỏi nhìn theo chuột; laser/lông vũ bật thì chạm là để điều khiển
  doChoi.dangChoi = () => laserBat || !!len || !!lv;
  doChoi.dieuKhien = () => laserBat || !!lv;
  doChoi.keoLen = () => !!lenKeo;
  Object.assign(window.boChoi, { batLaser, batLen, batLongVu });
})();
