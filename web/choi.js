// Chạm & chơi với mèo Bơ – chạy hoàn toàn trên trình duyệt, KHÔNG gọi API (miễn phí, tức thì).
// Vuốt đầu/lưng → rừ rừ, tim bay; gãi cằm → ngửa cổ; chạm tai → tai giật; chọc bụng → giật mình (5 lần liền → dỗi);
// nút cá → Bơ ăn; nút laser → chấm đỏ theo ngón tay, Bơ nhìn theo và vồ. Câu nói nhỏ hiện bong bóng, không vào lịch sử chat.

// ---- Phần tính toán thuần (test được bằng node) ----
// Vùng chạm theo tọa độ trong khung vẽ 200×192 của mèo
function boVungCham(x, y) {
  const trong = (cx, cy, rx, ry) => ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1;
  if (y > 4 && y < 54) { if (x > 38 && x < 72) return 'tai_trai'; if (x > 128 && x < 162) return 'tai_phai'; }
  if (trong(100, 74, 58, 47)) return y > 100 && Math.abs(x - 100) < 30 ? 'cam' : 'dau';
  if (trong(100, 140, 40, 32)) return 'bung';
  if (trong(100, 130, 68, 50)) return 'lung';
  return null;
}
// Đếm số lần chọc trong cửa sổ thời gian; trả về danh sách mốc còn giữ
function boDemChoc(moc, bayGio, cuaSo = 4000) {
  return moc.concat(bayGio).filter(t => bayGio - t <= cuaSo);
}
const BO_CAU_CHOI = {
  vuot: ['rừ rừ~', 'meo~ thêm chút nữa đi', 'sướng ghê á', 'đúng chỗ đó đó!', 'Bơ tan chảy rồi nè'],
  gai_cam: ['ư ư~ gãi nữa đi', 'chỗ này nè, chỗ này!', 'mèo béo thích lắm luôn'],
  tai: ['nhột á!', 'ơ, tai Bơ mà', 'hửm?'],
  choc: ['ối!', 'giật cả mình!', 'bụng Bơ không phải cái nút đâu nha', 'hí hí, nhột'],
  doi: ['Hứ! Bơ dỗi rồi.', 'Không chơi với bạn nữa... một xíu thôi.'],
  lanh: ['Thôi, làm lành nha~', 'Bơ hết giận rồi đó.'],
  an: ['Ngon quá trời~', 'Cá! Cá của Bơ!', 'Măm măm, cảm ơn nha!'],
  no: ['Bơ no căng rồi, để dành mai nha~', 'Béo quá rồi, thôi thôi.'],
  len: ['Cuộn len! Của Bơ!', 'Bép! Bơ đập trúng rồi', 'Ném nữa đi, ném nữa đi!', 'Hí hí, lăn đi đâu đó?'],
  laser: ['Cái chấm đỏ kìa!!', 'Bắt được rồi... ủa đâu?', 'Lần này Bơ bắt được cho coi!'],
  thuc: ['Ưm... ai gọi Bơ đó?', 'Bơ đâu có ngủ, Bơ nhắm mắt nghĩ thôi.'],
  lan: ['Gãi bụng Bơ đi mà~', 'Bơ lăn nè, thấy dễ thương hông?', 'Nũng xíu thôi hà~'],
  mung: ['Bạn về rồi! Bơ nhớ bạn ghê~', 'A, bạn đây rồi! Meo meo!', 'Vui quá, bạn quay lại rồi nè!'],
  vuon: ['Ưm... chào buổi sáng~', 'Sáng rồi hả? Bơ vươn vai cái đã.', 'Ngáp... chào bạn buổi sáng nha!'],
};
// Những loại câu chơi được đọc to khi bật "Giọng nói" (câu vuốt/chọc lặp nhiều quá nên chỉ hiện chữ)
const BO_DOC_TO = ['mung', 'vuon', 'an', 'no', 'doi', 'lanh', 'thuc'];  // ('len' chỉ hiện chữ: vồ liên tục)
function boCauNgau(loai, rnd = Math.random) {
  const ds = BO_CAU_CHOI[loai] || [];
  return ds.length ? ds[Math.floor(rnd() * ds.length) % ds.length] : '';
}
// Đếm nhẹ trong ngày (lưu trên máy này): hôm nay vuốt mấy lần, gãi cằm, cho ăn... Qua ngày mới thì về 0
function boDemHomNay(cu, loai, ngay) {
  const d = cu && cu.ngay === ngay ? { ...cu } : { ngay };
  d[loai] = (d[loai] || 0) + 1;
  return d;
}
// Mắt nhìn theo ngón tay/chuột: (dx, dy) từ giữa đầu mèo (đơn vị khung vẽ) → độ dời con ngươi. Gần quá thì nhìn thẳng
function boHuongNhin(dx, dy) {
  const d = Math.hypot(dx, dy);
  if (d < 6) return [0, 0];
  const k = Math.min(1, d / 80);
  return [+(dx / d * 4 * k).toFixed(1), +(dy / d * 3 * k).toFixed(1)];
}
// Lúc mở web (hoặc quay lại tab): lâu rồi mới gặp (từ 1 ngày) → 'mung'; sáng sớm 5–10h, lần đầu sau ít nhất 4 tiếng → 'vuon'.
// Lần đầu dùng (chưa có mốc) hoặc giờ máy lùi → null. Không bao giờ trách người dùng đi lâu.
function boLucMo(lanTruoc, bayGio, gio) {
  if (!lanTruoc || bayGio < lanTruoc) return null;
  const tieng = (bayGio - lanTruoc) / 3600000;
  if (tieng >= 24) return 'mung';
  if (gio >= 5 && gio < 10 && tieng >= 4) return 'vuon';
  return null;
}
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

if (typeof module !== 'undefined') module.exports = { boVungCham, boDemChoc, boCauNgau, boDemHomNay, boHuongNhin, boLucMo, boBuocLen, BO_CAU_CHOI, BO_DOC_TO };

// ---- Phần giao diện ----
(function () {
  if (typeof document === 'undefined') return;
  const face = document.getElementById('face'), khung = document.getElementById('meoKhung');
  const svg = face && face.querySelector('svg');
  if (!svg || !khung) return;
  const bong = document.getElementById('meoBong');
  const nhin = svg.querySelector('.nhin');
  const yenLang = () => window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  const homNay = () => new Date().toLocaleDateString('sv');  // YYYY-MM-DD theo giờ máy

  // Đếm trong ngày (dùng cho dòng gửi bộ não ở bước sau)
  function dem(loai) {
    let cu = null;
    try { cu = JSON.parse(localStorage.getItem('bo_choi') || 'null'); } catch (e) {}
    const moi = boDemHomNay(cu, loai, homNay());
    try { localStorage.setItem('bo_choi', JSON.stringify(moi)); } catch (e) {}
    return moi;
  }

  // Bong bóng câu nói nhỏ, không lưu vào lịch sử
  let bongTimer = null, lanNoiCuoi = 0;
  function noi(loai, batBuoc) {
    const now = Date.now();
    if (!batBuoc && (now - lanNoiCuoi < 3500 || Math.random() < 0.45)) return;
    lanNoiCuoi = now;
    const cau = boCauNgau(loai);
    bong.textContent = cau; bong.hidden = false;
    // Đang bật "Giọng nói": vài câu chơi được đọc to (không cắt ngang khi Bơ đang đọc câu trả lời; giờ yên lặng thì thôi)
    // (đợi một chút: cú chạm vừa rồi còn sự kiện "click" — chạm Bơ lúc đang đọc là bảo Bơ im — kẻo câu vừa đọc bị tắt ngay)
    if (BO_DOC_TO.includes(loai)) setTimeout(() => {
      if (typeof speakAuto === 'function' && typeof speaking !== 'undefined' && !speaking) speakAuto(cau);
    }, 80);
    bong.classList.remove('hien'); void bong.offsetWidth; bong.classList.add('hien');
    clearTimeout(bongTimer);
    bongTimer = setTimeout(() => { bong.hidden = true; }, 2600);
  }

  // Trạng thái tạm trên mèo: bật rồi tự tắt sau ms (gọi lại thì kéo dài)
  const hen = {};
  function giu(cls, ms) {
    svg.classList.add(cls);
    clearTimeout(hen[cls]);
    hen[cls] = setTimeout(() => svg.classList.remove(cls), ms);
  }

  // Tim bay lên
  let timCuoi = 0;
  function tim(x, y) {
    const now = Date.now();
    if (now - timCuoi < 350) return;
    timCuoi = now;
    const t = document.createElement('span');
    t.className = 'tim'; t.textContent = '♥';
    t.style.left = x + 'px'; t.style.top = y + 'px';
    khung.appendChild(t);
    setTimeout(() => t.remove(), 1200);
  }

  // ---- Tiếng rừ rừ: tạo bằng Web Audio (tiếng ồn trầm, nhấp nhô ~24 lần/giây), không cần file ----
  let ac = null, rr = null;
  function grgr(bat) {
    try {
      if (bat) {
        if (rr) return;
        ac = ac || new (window.AudioContext || window.webkitAudioContext)();
        if (ac.state === 'suspended') ac.resume();
        const buf = ac.createBuffer(1, ac.sampleRate * 2, ac.sampleRate), d = buf.getChannelData(0);
        let last = 0;
        for (let i = 0; i < d.length; i++) { last = (last + 0.04 * (Math.random() * 2 - 1)) / 1.04; d[i] = last * 3; }
        const src = ac.createBufferSource(); src.buffer = buf; src.loop = true;
        const loc = ac.createBiquadFilter(); loc.type = 'lowpass'; loc.frequency.value = 260;
        const nhip = ac.createGain(); nhip.gain.value = 0.5;
        const lfo = ac.createOscillator(); lfo.frequency.value = 24;
        const sau = ac.createGain(); sau.gain.value = 0.5; lfo.connect(sau); sau.connect(nhip.gain);
        const tong = ac.createGain(); tong.gain.value = 0;
        tong.gain.linearRampToValueAtTime(0.35, ac.currentTime + 0.3);
        src.connect(loc); loc.connect(nhip); nhip.connect(tong); tong.connect(ac.destination);
        src.start(); lfo.start();
        rr = { src, lfo, tong };
      } else if (rr) {
        const { src, lfo, tong } = rr; rr = null;
        tong.gain.cancelScheduledValues(ac.currentTime);
        tong.gain.setValueAtTime(tong.gain.value, ac.currentTime);
        tong.gain.linearRampToValueAtTime(0, ac.currentTime + 0.4);
        setTimeout(() => { try { src.stop(); lfo.stop(); } catch (e) {} }, 500);
      }
    } catch (e) { rr = null; }
  }

  // ---- Đổi tọa độ màn hình sang khung vẽ của mèo ----
  function toaDo(ev) {
    const m = svg.getScreenCTM();
    if (!m) return null;
    const p = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(m.inverse());
    return { x: p.x, y: p.y };
  }
  function viTriKhung(ev) {
    const r = khung.getBoundingClientRect();
    return { x: ev.clientX - r.left, y: ev.clientY - r.top };
  }

  // ---- Vuốt ve / chạm ----
  let bam = null, vuotDangChay = false, vuotTat = null, quangVuot = 0, viTriTruoc = null, mocChoc = [];
  const dangDoi = () => svg.classList.contains('doi');
  function vuot(ev, vung) {
    if (dangDoi()) return;
    const pos = viTriKhung(ev);
    if (viTriTruoc) quangVuot += Math.hypot(pos.x - viTriTruoc.x, pos.y - viTriTruoc.y);
    viTriTruoc = pos;
    if (quangVuot < 40) return;
    // rê chuột vuốt ve cũng là đang chơi: Bơ đang thức thì đừng ngủ gật giữa chừng (đang ngủ thì rừ rừ trong mơ)
    if (face.dataset.e !== 'ngu' && typeof scheduleSleep === 'function') scheduleSleep();
    const loai = vung === 'cam' ? 'gai_cam' : 'vuot';
    if (!vuotDangChay) { vuotDangChay = loai; dem(loai); noi(loai); }
    giu(loai === 'gai_cam' ? 'gai-cam' : 'vuot', 700);
    if (loai === 'vuot') tim(pos.x, pos.y - 10);
    grgr(true);
    clearTimeout(vuotTat);
    vuotTat = setTimeout(() => { vuotDangChay = false; quangVuot = 0; viTriTruoc = null; grgr(false); }, 700);
  }
  function cham(ev, vung, vuaNgu) {
    if (vuaNgu) { noi('thuc', true); return; }  // đang ngủ: chạm là tỉnh (hop_thoai.js lo), Bơ lầm bầm
    if (dangDoi()) return;
    if (typeof speaking !== 'undefined' && speaking) return;  // đang đọc to: chạm là để Bơ im (hop_thoai.js)
    if (vung === 'tai_trai' || vung === 'tai_phai') {
      giu(vung === 'tai_trai' ? 'giat-tai-trai' : 'giat-tai-phai', 450); noi('tai');
    } else if (vung === 'bung' || vung === 'lung') {
      mocChoc = boDemChoc(mocChoc, Date.now());
      dem('choc');
      if (mocChoc.length >= 5) {
        mocChoc = [];
        svg.classList.remove('lan'); giu('doi', 4500); noi('doi', true);
        setTimeout(() => { noi('lanh', true); giu('lanh', 1200); }, 4600);
      } else { giu('giat', 500); noi('choc'); }
    } else if (vung === 'cam') {
      giu('gai-cam', 900); noi('gai_cam');
    } else if (vung === 'dau') {
      giu('vuot', 900); const p = viTriKhung(ev); tim(p.x, p.y - 10); noi('vuot');
    }
  }
  // Nhấn giữ lên lưng/bụng (không kéo) khoảng 0,7 giây → Bơ lăn qua lăn lại nũng nịu
  let henLan = null;
  face.addEventListener('pointerdown', ev => {
    const b = bam = { t: Date.now(), x: ev.clientX, y: ev.clientY, di: 0, ngu: face.dataset.e === 'ngu' };
    viTriTruoc = null; quangVuot = 0;
    try { face.setPointerCapture(ev.pointerId); } catch (e) {}
    clearTimeout(henLan);
    const p = toaDo(ev), vung = p && boVungCham(p.x, p.y);
    if (!b.ngu && !laserBat && (vung === 'bung' || vung === 'lung')) {
      henLan = setTimeout(() => {
        if (bam !== b || b.di >= 10 || dangDoi() || (typeof speaking !== 'undefined' && speaking)) return;
        giu('lan', 3200); noi('lan', true);
      }, 700);
    }
  });
  face.addEventListener('pointermove', ev => {
    if (laserBat || (typeof lenKeo !== 'undefined' && lenKeo)) return;  // đang kéo cuộn len ngang qua Bơ: không tính là vuốt
    if (bam) bam.di = Math.max(bam.di, Math.hypot(ev.clientX - bam.x, ev.clientY - bam.y));
    // kéo ngón tay, hoặc rê chuột (không cần bấm) trên đầu/lưng/cằm = vuốt ve
    if (!bam && ev.pointerType !== 'mouse') return;
    const p = toaDo(ev); if (!p) return;
    const vung = boVungCham(p.x, p.y);
    if (vung === 'dau' || vung === 'lung' || vung === 'cam') vuot(ev, vung);
  });
  face.addEventListener('pointerup', ev => {
    const b = bam; bam = null; clearTimeout(henLan);
    if (!b || laserBat) return;
    if (b.di < 10 && Date.now() - b.t < 500) {
      const p = toaDo(ev); if (p) cham(ev, boVungCham(p.x, p.y), b.ngu);
    }
  });
  face.addEventListener('pointercancel', () => { bam = null; clearTimeout(henLan); });
  // Bàn phím: Tab tới Bơ rồi bấm Enter = xoa đầu, phím cách = gãi cằm (đang ngủ thì Bơ tỉnh)
  face.tabIndex = 0;
  face.addEventListener('keydown', ev => {
    if (ev.key !== 'Enter' && ev.key !== ' ') return;
    ev.preventDefault();
    if (ev.repeat) return;
    if (typeof boNgungDoc === 'function' && boNgungDoc()) return;  // đang đọc to: phím = bảo Bơ im, như chạm
    const r = face.getBoundingClientRect(), giua = { clientX: r.left + r.width / 2, clientY: r.top + r.height * 0.3 };
    cham(giua, ev.key === 'Enter' ? 'dau' : 'cam', face.dataset.e === 'ngu');  // hop_thoai.js tự đánh thức khi có phím bấm
  });
  face.addEventListener('pointerleave', () => { if (!bam) { viTriTruoc = null; } });

  // ---- Cho ăn: không có thanh "đói", cho bao nhiêu cũng được; ăn nhiều quá thì Bơ bảo no ----
  const nutCa = document.getElementById('choAn');
  let dangAn = false;
  nutCa.addEventListener('click', () => {
    if (dangAn || dangDoi()) return;
    dangAn = true;
    const d = dem('cho_an');
    if (d.cho_an > 5) { noi('no', true); giu('liem-mep', 1200); setTimeout(() => { dangAn = false; }, 1200); return; }
    const ca = document.createElement('span');
    ca.className = 'ca-an'; ca.innerHTML = nutCa.innerHTML;
    khung.appendChild(ca);
    giu('an', 2600);
    setTimeout(() => { ca.remove(); giu('liem-mep', 1300); noi('an', true); }, 2600);
    setTimeout(() => { dangAn = false; }, 3900);
  });

  // ---- Tia laser: chấm đỏ theo ngón tay/chuột trong vùng quanh mèo; mèo nhìn theo, chấm tới gần thì vồ ----
  const nutLaser = document.getElementById('doChoi');
  const header = khung.closest('header') || khung;
  let laserBat = false, cham_ = null, voCuoi = 0, laserTat = null;
  function batLaser(bat) {
    laserBat = bat;
    nutLaser.setAttribute('aria-pressed', bat);
    header.classList.toggle('dang-laser', bat);
    if (bat) {
      if (typeof batLen === 'function') batLen(false);
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
    if (!lenS.yen || lenKeo) lenVong = requestAnimationFrame(buocLen);
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
    voLen = Date.now(); giu('vo', 600); dem('len'); noi('len');
    const huong = p.x < 100 ? -1 : 1;
    lenS = { ...lenS, vx: huong * (260 + Math.random() * 200), vy: -380 - Math.random() * 200 };
  }
  function batLen(bat) {
    if (bat === !!len) return;
    nutLen.setAttribute('aria-pressed', bat);
    if (bat) {
      if (laserBat) batLaser(false);
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

  // ---- Mắt nhìn theo ngón tay/chuột (ngoài lúc chơi laser); đứng yên 3 giây thì thôi nhìn ----
  let nhinTat = null, nhinCho = false, nhinEv = null;
  function nhinTheo() {
    nhinCho = false;
    const ev = nhinEv;
    if (!ev || laserBat || len || !nhin || face.dataset.e === 'ngu' || dangDoi()) return;
    const m = svg.getScreenCTM(); if (!m) return;
    const p = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(m.inverse());
    if (Math.hypot(p.x - 100, p.y - 74) > 600) { nhin.removeAttribute('transform'); return; }  // xa quá: kệ
    const [tx, ty] = boHuongNhin(p.x - 100, p.y - 74);
    nhin.setAttribute('transform', `translate(${tx} ${ty})`);
    clearTimeout(nhinTat);
    nhinTat = setTimeout(() => { if (!laserBat) nhin.removeAttribute('transform'); }, 3000);
  }
  document.addEventListener('pointermove', ev => {
    if (ev.pointerType !== 'mouse' && !bam) return;  // điện thoại: chỉ khi đang chạm vào Bơ
    nhinEv = ev;
    if (!nhinCho) { nhinCho = true; requestAnimationFrame(nhinTheo); }
  }, { passive: true });

  // ---- Mở web / quay lại tab: lâu rồi mới gặp thì mừng rỡ, sáng sớm thì vươn vai (không gọi API) ----
  const docMoc = () => { try { return +localStorage.getItem('bo_lan_gap') || 0; } catch (e) { return 0; } };
  const ghiMoc = () => { try { localStorage.setItem('bo_lan_gap', String(Date.now())); } catch (e) {} };
  function lucMo() {
    const kieu = boLucMo(docMoc(), Date.now(), new Date().getHours());
    ghiMoc();
    if (!kieu) return;
    setTimeout(() => {
      if (face.dataset.e === 'ngu') return;
      giu(kieu === 'mung' ? 'mung' : 'vuon', kieu === 'mung' ? 2400 : 1300); noi(kieu, true);
    }, 700);
  }
  lucMo();
  document.addEventListener('visibilitychange', () => { document.hidden ? ghiMoc() : lucMo(); });
  setInterval(() => { if (!document.hidden) ghiMoc(); }, 60000);  // còn đang mở thì coi như vẫn đang gặp

  window.boChoi = { batLaser, dem, lucMo };
})();
