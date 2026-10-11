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
  laser: ['Cái chấm đỏ kìa!!', 'Bắt được rồi... ủa đâu?', 'Lần này Bơ bắt được cho coi!'],
  thuc: ['Ưm... ai gọi Bơ đó?', 'Bơ đâu có ngủ, Bơ nhắm mắt nghĩ thôi.'],
};
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

if (typeof module !== 'undefined') module.exports = { boVungCham, boDemChoc, boCauNgau, boDemHomNay, BO_CAU_CHOI };

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
    bong.textContent = boCauNgau(loai); bong.hidden = false;
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
        giu('doi', 4500); noi('doi', true);
        setTimeout(() => { noi('lanh', true); giu('lanh', 1200); }, 4600);
      } else { giu('giat', 500); noi('choc'); }
    } else if (vung === 'cam') {
      giu('gai-cam', 900); noi('gai_cam');
    } else if (vung === 'dau') {
      giu('vuot', 900); const p = viTriKhung(ev); tim(p.x, p.y - 10); noi('vuot');
    }
  }
  face.addEventListener('pointerdown', ev => {
    bam = { t: Date.now(), x: ev.clientX, y: ev.clientY, di: 0, ngu: face.dataset.e === 'ngu' };
    viTriTruoc = null; quangVuot = 0;
    try { face.setPointerCapture(ev.pointerId); } catch (e) {}
  });
  face.addEventListener('pointermove', ev => {
    if (laserBat) return;
    if (bam) bam.di = Math.max(bam.di, Math.hypot(ev.clientX - bam.x, ev.clientY - bam.y));
    // kéo ngón tay, hoặc rê chuột (không cần bấm) trên đầu/lưng/cằm = vuốt ve
    if (!bam && ev.pointerType !== 'mouse') return;
    const p = toaDo(ev); if (!p) return;
    const vung = boVungCham(p.x, p.y);
    if (vung === 'dau' || vung === 'lung' || vung === 'cam') vuot(ev, vung);
  });
  face.addEventListener('pointerup', ev => {
    const b = bam; bam = null;
    if (!b || laserBat) return;
    if (b.di < 10 && Date.now() - b.t < 500) {
      const p = toaDo(ev); if (p) cham(ev, boVungCham(p.x, p.y), b.ngu);
    }
  });
  face.addEventListener('pointercancel', () => { bam = null; });
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

  window.boChoi = { batLaser, dem };
})();
