// Chạm & chơi với mèo Bơ – chạy hoàn toàn trên trình duyệt, KHÔNG gọi API (miễn phí, tức thì).
// Vuốt đầu/lưng → rừ rừ, tim bay; gãi cằm → ngửa cổ; chạm tai → tai giật; chọc bụng → giật mình (5 lần liền → dỗi);
// nút cá → Bơ ăn. Đồ chơi (laser, cuộn len, lông vũ) nằm ở do_choi.js. Câu nói nhỏ hiện bong bóng, không vào lịch sử chat.

// ---- Phần tính toán thuần (test được bằng node) ----
// Vùng chạm theo tọa độ trong khung vẽ 200×192 của mèo
function boVungCham(x, y) {
  const trong = (cx, cy, rx, ry) => ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1;
  if (y > 4 && y < 54) { if (x > 38 && x < 72) return 'tai_trai'; if (x > 128 && x < 162) return 'tai_phai'; }
  if (trong(100, 74, 58, 47)) return y > 100 && Math.abs(x - 100) < 30 ? 'cam' : 'dau';
  if (trong(82, 174, 15, 11) || trong(118, 174, 15, 11)) return 'chan';  // hai chân trước
  if (trong(184, 108, 13, 30) || trong(175, 80, 10, 9)) return 'duoi';  // đuôi dựng bên phải
  if (trong(100, 140, 40, 32)) return 'bung';
  if (trong(100, 130, 68, 50)) return 'lung';
  return null;
}
// Chỗ nhỏ trên mặt (chỉ dùng khi đã chạm vào 'dau'): mũi → 'mui' (boop), hai má → 'ma_trai' / 'ma_phai' (nựng má); không thì null
function boChiTietDau(x, y) {
  const trong = (cx, cy, rx, ry) => ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1;
  if (trong(100, 88, 10, 8)) return 'mui';
  if (trong(62, 91, 14, 10)) return 'ma_trai';
  if (trong(138, 91, 14, 10)) return 'ma_phai';
  return null;
}
// Đếm số lần chọc trong cửa sổ thời gian; trả về danh sách mốc còn giữ
function boDemChoc(moc, bayGio, cuaSo = 4000) {
  return moc.concat(bayGio).filter(t => bayGio - t <= cuaSo);
}
const BO_CAU_CHOI = {
  nhoi: ['Nhồi nhồi... Bơ nhồi bột nè~', 'Sướng quá, chân Bơ tự dẫm luôn á', 'Rừ rừ... nhồi nhồi~'],
  vuot: ['rừ rừ~', 'meo~ thêm chút nữa đi', 'sướng ghê á', 'đúng chỗ đó đó!', 'Bơ tan chảy rồi nè'],
  gai_cam: ['ư ư~ gãi nữa đi', 'chỗ này nè, chỗ này!', 'mèo béo thích lắm luôn'],
  tai: ['nhột á!', 'ơ, tai Bơ mà', 'hửm?'],
  choc: ['ối!', 'giật cả mình!', 'bụng Bơ không phải cái nút đâu nha', 'hí hí, nhột'],
  doi: ['Hứ! Bơ dỗi rồi.', 'Không chơi với bạn nữa... một xíu thôi.'],
  lanh: ['Thôi, làm lành nha~', 'Bơ hết giận rồi đó.'],
  an: ['Ngon quá trời~', 'Cá! Cá của Bơ!', 'Măm măm, cảm ơn nha!'],
  an_sua: ['Lép lép... sữa mát ghê~', 'Râu Bơ dính sữa rồi nè, hí hí', 'Sữa! Bơ liếm sạch bát luôn!'],
  an_pate: ['Pate! Bơ mê pate nhất trần đời~', 'Măm măm, béo ngậy ghê!', 'Pate ngon quá, Bơ béo thêm nữa rồi nè'],
  no: ['Bơ no căng rồi, để dành mai nha~', 'Béo quá rồi, thôi thôi.'],
  len: ['Cuộn len! Của Bơ!', 'Bép! Bơ đập trúng rồi', 'Ném nữa đi, ném nữa đi!', 'Hí hí, lăn đi đâu đó?'],
  laser: ['Cái chấm đỏ kìa!!', 'Bắt được rồi... ủa đâu?', 'Lần này Bơ bắt được cho coi!'],
  long_vu: ['Lông vũ! Lông vũ!', 'Hụt rồi... lần nữa!', 'Bơ với tới nè!', 'Xuống thấp xíu đi mà~'],
  nguoc: ['Ngược lông rồi á!', 'Ơ kìa, vuốt xuôi cơ mà~', 'Lông Bơ dựng hết rồi nè!', 'Hướng kia mới đúng nha!'],
  chan: ['Chân Bơ đó nha~', 'Hí, nhột chân!', 'Hửm? Muốn nắm tay Bơ hả?'],
  dap_tay: ['Đập tay nè!', 'Bốp! Tuyệt vời!', 'Hi-five với Bơ nè!', 'Một, hai, bốp!'],
  duoi: ['Đuôi Bơ mà!', 'Ơ, ai đụng đuôi Bơ đó?', 'Đuôi này không phải đồ chơi nha~', 'Hửm? Đuôi Bơ có gì hả?'],
  ngui: ['Hít hít... thơm tay bạn ghê~', 'Cho Bơ ngửi xíu... ừm, quen quen!', 'Hít hít~ Bơ cọ cọ nè'],
  chong_mat: ['Ối ối, chóng mặt quá~', 'Đừng lắc nữa mà, Bơ xoay vòng vòng rồi!', 'Trời đất quay cuồng... meo~'],
  boop: ['Boop! Mũi Bơ đó nha~', 'Hí, nhột mũi!', 'Ơ... Bơ bị boop rồi!', 'Mũi Bơ hồng hông?'],
  ma: ['Nựng má Bơ hả~', 'Má Bơ phúng phính chưa?', 'Hí hí, cọ cọ nè', 'Thêm bên này nữa nha~'],
  be: ['Ơ ơ, bế Bơ đi đâu đó?', 'Úi, Bơ bay lên rồi nè!', 'Bơ nặng lắm đó nha~', 'Thả Bơ xuống điii~'],
  em: ['Bế Bơ êm ghê~', 'Rừ rừ... cứ bế Bơ vầy hoài nha', 'Bơ ngủ trên tay bạn luôn á~'],
  tha: ['Bịch! Về chỗ cũ rồi~', 'Hú hồn, đất đây rồi!', 'Hạ cánh an toàn, meo!'],
  rinh: ['Rình... rình...', 'Suỵt... Bơ đang rình đó', 'Mông ngoáy ngoáy... chuẩn bị nè'],
  vo_rinh: ['Phập! Bắt được rồi!', 'Vồ! Lông vũ là của Bơ!', 'Hây da! Trúng phóc!', 'Bơ là thợ săn số một~'],
  hat_xi: ['Hắt xì!', 'Hắt... xì! Lông vũ nhột mũi quá~', 'Ắt xì! Hí hí'],
  goi: ['Dạ? Bơ nghe nè!', 'Meo? Bạn gọi Bơ hả?', 'Dạaa~ Bơ đây!'],
  dep: ['Bộ lông mới nè, Bơ đẹp hông?', 'Hí, Bơ điệu chưa~', 'Thấy Bơ xinh lên hông?'],
  khuya: ['Khuya rồi nè, bạn ngủ sớm nha~', 'Rừ rừ... Bơ buồn ngủ quá, bạn cũng ngủ đi nha', 'Vuốt xíu nữa rồi mình đi ngủ ha~'],
  thuc: ['Ưm... ai gọi Bơ đó?', 'Bơ đâu có ngủ, Bơ nhắm mắt nghĩ thôi.'],
  lan: ['Gãi bụng Bơ đi mà~', 'Bơ lăn nè, thấy dễ thương hông?', 'Nũng xíu thôi hà~'],
  mung: ['Bạn về rồi! Bơ nhớ bạn ghê~', 'A, bạn đây rồi! Meo meo!', 'Vui quá, bạn quay lại rồi nè!'],
  vuon: ['Ưm... chào buổi sáng~', 'Sáng rồi hả? Bơ vươn vai cái đã.', 'Ngáp... chào bạn buổi sáng nha!'],
};
// Những loại câu chơi được đọc to khi bật "Giọng nói" (câu vuốt/chọc lặp nhiều quá nên chỉ hiện chữ)
const BO_DOC_TO = ['mung', 'vuon', 'an', 'an_sua', 'an_pate', 'em', 'no', 'doi', 'lanh', 'thuc', 'dep', 'chong_mat', 'ngui'];  // (đập tay: chỉ lần đầu trong ngày)  // ('len' chỉ hiện chữ: vồ liên tục)
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
// Chạm chân trước: hai lần liền nhau (cách nhau dưới 450 ms) → 'dap_tay' (Bơ giơ chân đập tay); không thì 'chan'
function boChamChan(lanTruoc, bayGio) {
  return lanTruoc && bayGio - lanTruoc >= 0 && bayGio - lanTruoc < 450 ? 'dap_tay' : 'chan';
}
// Tiếng "meo" tổng hợp (Web Audio, không cần file): thời lượng (giây) và ba mốc cao độ / độ vang (Hz) theo kiểu
// 'ngan' = "mrr?" ngắn (chạm tai/đuôi), 'vui' = "meo~" cao dần (đập tay). Kiểu lạ → 'ngan'.
function boThongSoMeo(kieu) {
  const ds = {
    ngan: { dai: 0.22, cao: [520, 640, 560], vang: [900, 1300, 1000] },
    vui: { dai: 0.5, cao: [560, 820, 700], vang: [1000, 1900, 1400] },
  };
  return ds[kieu] || ds.ngan;
}
// Tiếng ăn (Web Audio, tiếng ồn lọc, không file): danh sách nhịp {t: giây bắt đầu, dai: giây, hz: tần số lọc, to: độ to}.
// (độ to đã đo bằng OfflineAudioContext: cả ba món cỡ tiếng meo ngắn.) Cá: nhai rộp rộp giòn; pate: chép chép mềm, trầm; sữa: liếm lép lép nhanh. Món lạ → cá. Nằm gọn trong lúc Bơ ăn (0,4–2,5 giây).
function boNhipAn(mon, rnd = Math.random) {
  const ds = {
    ca: { dau: 0.45, cach: 0.3, so: 7, dai: 0.06, hz: 2200, to: 0.5 },
    pate: { dau: 0.45, cach: 0.34, so: 6, dai: 0.09, hz: 900, to: 0.8 },
    sua: { dau: 0.4, cach: 0.2, so: 10, dai: 0.045, hz: 1400, to: 0.7 },
  };
  const k = ds[mon] || ds.ca, kq = [];
  for (let i = 0; i < k.so; i++) {
    const lech = rnd() - 0.5;  // lệch nhẹ cho tự nhiên
    kq.push({ t: +(k.dau + i * k.cach + lech * 0.04).toFixed(3), dai: k.dai, hz: Math.round(k.hz * (1 + lech * 0.2)), to: +(k.to * (0.8 + rnd() * 0.2)).toFixed(3) });
  }
  return kq;
}
// Ngón tay/chuột ở ngay trước mũi Bơ (khung vẽ 200×192, mũi ở 100,88)? Giữ yên ở đây ~1 giây thì Bơ ngửi
function boGanMui(x, y) {
  return ((x - 100) / 24) ** 2 + ((y - 90) / 16) ** 2 <= 1;
}
// Độ to tiếng rừ rừ theo số giây đã vuốt liền: mới vuốt thì nhỏ, vuốt lâu to dần, tối đa 0,5
function boDoToRuRu(giay) {
  return +Math.min(0.5, 0.18 + Math.max(0, giay) * 0.05).toFixed(3);
}
// Vuốt lưng/đầu liền một mạch bao nhiêu giây thì Bơ sướng quá bắt đầu nhồi bột (hai chân trước dẫm luân phiên)
function boNhoiBot(giayVuot) {
  return giayVuot >= 6;
}
// Vuốt xong một lượt dài (từ 3 giây) thì Bơ nhìn mình chớp mắt thật chậm (kiểu mèo nói "thương bạn"); nghỉ 20 giây giữa hai lần
function boChopCham(giayVuot, msTuLanTruoc) {
  return giayVuot >= 3 && msTuLanTruoc >= 20000;
}
// Lắc điện thoại: độ "giật" giữa hai lần đo gia tốc (m/s², có cả trọng lực) = tổng chênh lệch ba trục
function boDoGiat(a, b) {
  if (!a || !b) return 0;
  return Math.abs((a.x || 0) - (b.x || 0)) + Math.abs((a.y || 0) - (b.y || 0)) + Math.abs((a.z || 0) - (b.z || 0));
}
// Giữ mốc các cú giật mạnh (từ 22 trở lên) trong 1 giây gần nhất; đủ 4 cú là đang lắc thật (đi bộ, bỏ túi không tới mức này)
function boLac(moc, bayGio, doGiat) {
  const m = (doGiat >= 22 ? moc.concat(bayGio) : moc).filter(t => bayGio - t <= 1000);
  return { moc: m, lac: m.length >= 4 };
}
// Gợi ý trò chạm chưa thử (tối đa 1 lần/ngày). daThu: các loại đã từng chơi; ngayCuoi: ngày gợi ý gần nhất; coLac: máy lắc được
const BO_GOI_Y = {
  dap_tay: 'Psst... chạm nhanh hai lần vào chân Bơ thử xem~',
  ngui: 'Để yên tay trước mũi Bơ một xíu đi, Bơ ngửi cho~',
  lan: 'Nhấn giữ bụng Bơ một giây xem Bơ lăn nè~',
  duoi: 'Đuôi Bơ cũng biết giật nha, chạm thử coi~',
  nguoc: 'Bí mật nè: vuốt ngược lông lên là Bơ xù đó!',
  len: 'Bơ thèm chơi cuộn len quá, bấm nút cuộn len đi~',
  long_vu: 'Có cần câu lông vũ đó, đưa lên đầu Bơ thử!',
  rinh: 'Thả lông vũ sát đất trước mặt Bơ đi, Bơ rình cho coi~',
  chong_mat: 'Lắc điện thoại thử coi, Bơ chóng mặt cho xem!',
  be: 'Nhấn giữ đầu Bơ rồi kéo lên, bế Bơ đi~',
  boop: 'Chạm nhẹ vào mũi Bơ thử coi... boop!',
  an_pate: 'Nhấn giữ nút con cá đi, Bơ thèm pate quá~',
};
function boGoiY(daThu, ngayCuoi, homNay, coLac, rnd = Math.random) {
  if (ngayCuoi === homNay) return null;
  const con = Object.keys(BO_GOI_Y).filter(k => !(daThu || []).includes(k) && (coLac || k !== 'chong_mat'));
  return con.length ? con[Math.floor(rnd() * con.length) % con.length] : null;
}
// Bế Bơ: đã nhấn giữ đầu, kéo (dx, dy px; y hướng xuống) → độ nhấc 0..1. Phải kéo hẳn lên trên (dọc nhiều hơn ngang, quá 20px)
function boDoNhac(dx, dy) {
  if (-dy < 20 || Math.abs(dx) > -dy) return 0;
  return +Math.min(1, (-dy - 20) / 80).toFixed(2);
}
// Món ăn (nhấn giữ nút cá để chọn). Không có thanh đói; chỉ khác hình và câu Bơ nói.
const BO_MON_AN = {
  ca: { ten: 'Cá', cau: 'an', svg: '<svg viewBox="0 0 32 20" aria-hidden="true"><path d="M2,10 C8,1 20,1 25,10 C20,19 8,19 2,10 Z" fill="#7fb7e6" stroke="#3d6f99" stroke-width="1.5"/><path d="M24,10 L31,4 L31,16 Z" fill="#7fb7e6" stroke="#3d6f99" stroke-width="1.5" stroke-linejoin="round"/><circle cx="8" cy="9" r="1.6" fill="#1f2a33"/></svg>' },
  sua: { ten: 'Sữa', cau: 'an_sua', svg: '<svg viewBox="0 0 32 20" aria-hidden="true"><path d="M3,8 L29,8 Q28,18 16,18 Q4,18 3,8 Z" fill="#9fc8e8" stroke="#3d6f99" stroke-width="1.5" stroke-linejoin="round"/><ellipse cx="16" cy="8" rx="13" ry="3" fill="#fffdf7" stroke="#3d6f99" stroke-width="1.5"/><path d="M8,12 Q16,15 24,12" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="1.2" stroke-linecap="round"/></svg>' },
  pate: { ten: 'Pate', cau: 'an_pate', svg: '<svg viewBox="0 0 32 20" aria-hidden="true"><rect x="5" y="7" width="22" height="11" rx="3" fill="#e9b949" stroke="#9a6b12" stroke-width="1.5"/><ellipse cx="16" cy="7" rx="11" ry="3" fill="#c97a54" stroke="#9a6b12" stroke-width="1.5"/><path d="M10,12 L22,12" stroke="#9a6b12" stroke-width="1.2" stroke-linecap="round"/><circle cx="16" cy="14.5" r="1.3" fill="#9a6b12"/></svg>' },
};
// Món hợp lệ (món lạ hay chưa chọn → cá)
function boMonAn(id) { return Object.prototype.hasOwnProperty.call(BO_MON_AN, id) ? id : 'ca'; }
// Tin nhắn Tân vừa gửi có nhắc tới cá (không tính "cá nhân", "cá tính"...) → 'ca' (Bơ liếm mép); có tim / thương / yêu → 'tim' (tim bay);
// buồn ngủ / ngáp / 😴 → 'ngap' (Bơ ngáp lây); không thì null
function boPhanUngTin(text) {
  const s = String(text || '');
  if (/[🐟🐠🐡🍣]/u.test(s) || /(^|[^\p{L}])cá(?!\s*(nhân|tính|cược|thể|biệt))($|[^\p{L}])/iu.test(s)) return 'ca';
  if (/[❤♥💕💖💗😍🥰😘]/u.test(s) || /(^|[^\p{L}])(thương|yêu)(?!\s*cầu)($|[^\p{L}])/iu.test(s)) return 'tim';
  // ngáp lây ("không/chưa/hết buồn ngủ" thì thôi)
  if (/[😴🥱💤]/u.test(s) || /(^|[^\p{L}])(?<!(không|chưa|hết|chẳng|chả|đỡ|đâu có)\s+)(buồn ngủ|ngáp|đi ngủ|ngủ ngon)($|[^\p{L}])/iu.test(s)) return 'ngap';
  return null;
}
// Hướng vuốt trên lưng (dx, dy: px từ chỗ bắt đầu vuốt tới giờ; y hướng xuống). Lông mèo mọc xuôi xuống,
// nên vuốt hẳn lên trên (dọc nhiều hơn ngang) là 'nguoc'; còn lại là 'xuoi'.
function boHuongVuot(dx, dy) {
  return dy < -25 && -dy > 1.2 * Math.abs(dx) ? 'nguoc' : 'xuoi';
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

if (typeof module !== 'undefined') module.exports = { boVungCham, boChiTietDau, boDemChoc, boCauNgau, boDemHomNay, boHuongNhin, boHuongVuot, boChamChan, boThongSoMeo, boGanMui, boDoToRuRu, boNhoiBot, boChopCham, boDoGiat, boLac, boGoiY, BO_GOI_Y, boPhanUngTin, boLucMo, boMonAn, BO_MON_AN, boNhipAn, boDoNhac, BO_CAU_CHOI, BO_DOC_TO };

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
  // Nhớ các trò đã từng chơi (trên máy này) để gợi ý trò chưa thử
  function docDaThu() { try { const d = JSON.parse(localStorage.getItem('bo_da_thu') || '[]'); return Array.isArray(d) ? d : []; } catch (e) { return []; } }
  function ghiDaThu(loai) {
    if (!(loai in BO_GOI_Y)) return;
    const d = docDaThu();
    if (!d.includes(loai)) { d.push(loai); try { localStorage.setItem('bo_da_thu', JSON.stringify(d)); } catch (e) {} }
  }
  function hienBong(cau, ms) {
    bong.textContent = cau; bong.hidden = false;
    bong.classList.remove('hien'); void bong.offsetWidth; bong.classList.add('hien');
    clearTimeout(bongTimer);
    bongTimer = setTimeout(() => { bong.hidden = true; }, ms);
  }
  function noi(loai, batBuoc, docThem) {
    ghiDaThu(loai);
    const now = Date.now();
    if (!batBuoc && (now - lanNoiCuoi < 3500 || Math.random() < 0.45)) return;
    lanNoiCuoi = now;
    const cau = boCauNgau(loai);
    hienBong(cau, 2600);
    // Đang bật "Giọng nói": vài câu chơi được đọc to (không cắt ngang khi Bơ đang đọc câu trả lời; giờ yên lặng thì thôi)
    // (đợi một chút: cú chạm vừa rồi còn sự kiện "click" — chạm Bơ lúc đang đọc là bảo Bơ im — kẻo câu vừa đọc bị tắt ngay)
    if (BO_DOC_TO.includes(loai) || docThem) setTimeout(() => {
      if (typeof speakAuto === 'function' && typeof speaking !== 'undefined' && !speaking) speakAuto(cau);
    }, 80);
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
  let ac = null, rr = null, rrBatDau = 0;
  function grgr(bat) {
    try {
      if (bat) {
        if (rr) {  // đang rừ rừ: vuốt càng lâu càng to
          rr.tong.gain.setTargetAtTime(boDoToRuRu((Date.now() - rrBatDau) / 1000), ac.currentTime, 0.4);
          return;
        }
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
        tong.gain.linearRampToValueAtTime(boDoToRuRu(0), ac.currentTime + 0.3);
        rrBatDau = Date.now();
        // điện thoại có rung: rung rất nhẹ vài nhịp lúc Bơ bắt đầu rừ rừ (máy bật giảm chuyển động thì thôi)
        if (navigator.vibrate && !yenLang()) { try { navigator.vibrate([12, 50, 12, 50, 12]); } catch (e) {} }
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

  // ---- Tiếng "meo" ngắn: chỉ khi bật "Giọng nói", ngoài giờ yên lặng, Bơ không đang đọc, không bật rảnh tay (micro khỏi nghe nhầm) ----
  let meoCuoi = 0;
  function duocKeu() {
    if (typeof voiceOn === 'undefined' || !voiceOn || (typeof speaking !== 'undefined' && speaking)) return false;
    if (typeof handsFree !== 'undefined' && handsFree) return false;
    if (typeof boGioYenLang === 'function' && typeof quietRange !== 'undefined' && boGioYenLang(new Date().getHours(), quietRange)) return false;
    return true;
  }
  // Tiếng ăn: rộp rộp / chép chép / lép lép (cùng điều kiện với tiếng meo)
  function tiengAn(mon) {
    if (!duocKeu()) return;
    try {
      ac = ac || new (window.AudioContext || window.webkitAudioContext)();
      if (ac.state === 'suspended') ac.resume();
      const buf = ac.createBuffer(1, Math.ceil(ac.sampleRate * 0.1), ac.sampleRate), d = buf.getChannelData(0);
      for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
      const t0 = ac.currentTime + 0.02;
      for (const n of boNhipAn(mon)) {
        const src = ac.createBufferSource(); src.buffer = buf;
        const loc = ac.createBiquadFilter(); loc.type = 'bandpass'; loc.frequency.value = n.hz; loc.Q.value = 1.4;
        const to = ac.createGain(), b = t0 + n.t;
        to.gain.setValueAtTime(0, b); to.gain.linearRampToValueAtTime(n.to, b + 0.008); to.gain.exponentialRampToValueAtTime(0.001, b + n.dai);
        src.connect(loc); loc.connect(to); to.connect(ac.destination);
        src.start(b); src.stop(b + n.dai + 0.02);
        src.onended = () => { try { to.disconnect(); } catch (e) {} };
      }
    } catch (e) {}
  }
  function keu(kieu) {
    if (!duocKeu()) return;
    const now = Date.now();
    if (now - meoCuoi < 1500) return;
    meoCuoi = now;
    try {
      ac = ac || new (window.AudioContext || window.webkitAudioContext)();
      if (ac.state === 'suspended') ac.resume();
      const { dai, cao, vang } = boThongSoMeo(kieu), t0 = ac.currentTime, giua = t0 + dai * 0.4, het = t0 + dai;
      const osc = ac.createOscillator(); osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(cao[0], t0); osc.frequency.linearRampToValueAtTime(cao[1], giua); osc.frequency.linearRampToValueAtTime(cao[2], het);
      const loc = ac.createBiquadFilter(); loc.type = 'bandpass'; loc.Q.value = 2.5;
      loc.frequency.setValueAtTime(vang[0], t0); loc.frequency.linearRampToValueAtTime(vang[1], giua); loc.frequency.linearRampToValueAtTime(vang[2], het);
      const to = ac.createGain(); to.gain.setValueAtTime(0, t0);
      to.gain.linearRampToValueAtTime(0.45, t0 + 0.04); to.gain.setValueAtTime(0.45, het - 0.08); to.gain.linearRampToValueAtTime(0, het);
      osc.connect(loc); loc.connect(to); to.connect(ac.destination);
      osc.start(t0); osc.stop(het + 0.05);
      osc.onended = () => { try { to.disconnect(); } catch (e) {} };  // ngắt hẳn, kẻo kêu nhiều thì trình duyệt nặng dần
    } catch (e) {}
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
  // Đồ chơi (do_choi.js) điền các hàm này: đang bật đồ chơi nào không, chạm có đang dùng để điều khiển đồ chơi không
  const doChoi = { dangChoi: () => false, dieuKhien: () => false, keoLen: () => false };
  let dauVuot = null, lanNguoc = 0, vuotBatDau = 0, daNoiNhoi = false, lanChopCham = 0;
  function vuot(ev, vung) {
    if (dangDoi()) return;
    const pos = viTriKhung(ev);
    if (viTriTruoc) quangVuot += Math.hypot(pos.x - viTriTruoc.x, pos.y - viTriTruoc.y);
    else dauVuot = pos;
    viTriTruoc = pos;
    if (quangVuot < 40) return;
    // Bấm/chạm rồi kéo ngược lên trên lưng = vuốt ngược lông (rê chuột không bấm thì không tính, kẻo lỡ tay)
    if (bam && vung === 'lung' && face.dataset.e !== 'ngu' && boHuongVuot(pos.x - dauVuot.x, pos.y - dauVuot.y) === 'nguoc') {
      nguocLong(); return;
    }
    // rê chuột vuốt ve cũng là đang chơi: Bơ đang thức thì đừng ngủ gật giữa chừng (đang ngủ thì rừ rừ trong mơ)
    if (face.dataset.e !== 'ngu' && typeof scheduleSleep === 'function') scheduleSleep();
    const loai = vung === 'cam' ? 'gai_cam' : 'vuot';
    if (!vuotDangChay) {
      vuotDangChay = loai; dem(loai); vuotBatDau = Date.now(); daNoiNhoi = false;
      const h = new Date().getHours();
      noi(loai === 'vuot' && (h >= 22 || h < 5) && Math.random() < 0.5 ? 'khuya' : loai);
    }
    giu(loai === 'gai_cam' ? 'gai-cam' : 'vuot', 700);
    if (loai === 'vuot') tim(pos.x, pos.y - 10);
    // vuốt lâu liền một mạch → Bơ nhồi bột (dẫm sữa) như mèo con, mắt lim dim
    if (loai === 'vuot' && face.dataset.e !== 'ngu' && boNhoiBot((Date.now() - vuotBatDau) / 1000)) {
      giu('nhoi', 900);
      if (!daNoiNhoi) { daNoiNhoi = true; dem('nhoi'); noi('nhoi', true); }
    }
    grgr(true);
    clearTimeout(vuotTat);
    vuotTat = setTimeout(() => {
      // vuốt xong một lượt dài: Bơ mở mắt nhìn mình, chớp thật chậm một cái
      if (vuotDangChay === 'vuot' && face.dataset.e !== 'ngu' && !dangDoi() && !svg.classList.contains('be')
          && boChopCham((Date.now() - vuotBatDau - 700) / 1000, Date.now() - lanChopCham)) {
        lanChopCham = Date.now(); setTimeout(() => giu('chop-cham', 1700), 250);
      }
      vuotDangChay = false; quangVuot = 0; viTriTruoc = null; grgr(false);
    }, 700);
  }
  function nguocLong() {
    clearTimeout(vuotTat); vuotDangChay = false; quangVuot = 0; viTriTruoc = null; grgr(false);
    svg.classList.remove('vuot', 'gai-cam', 'nhoi');
    giu('nguoc-long', 1100);
    if (Date.now() - lanNguoc > 4000) { lanNguoc = Date.now(); noi('nguoc', true); }
  }
  let lanChamChan = 0;
  // Chữ "Bốp!" bật ra chỗ hai bàn tay chạm nhau
  function bop(x, y, chu) {
    const t = document.createElement('span');
    t.className = 'tim bop'; t.textContent = chu || 'Bốp!';
    t.style.left = x + 'px'; t.style.top = y + 'px';
    khung.appendChild(t);
    setTimeout(() => t.remove(), 1200);
  }
  function cham(ev, vung, vuaNgu) {
    if (vuaNgu) { noi('thuc', true); return; }  // đang ngủ: chạm là tỉnh (hop_thoai.js lo), Bơ lầm bầm
    if (dangDoi()) return;
    if (typeof speaking !== 'undefined' && speaking) return;  // đang đọc to: chạm là để Bơ im (hop_thoai.js)
    if (vung === 'tai_trai' || vung === 'tai_phai') {
      giu(vung === 'tai_trai' ? 'giat-tai-trai' : 'giat-tai-phai', 450); noi('tai'); keu('ngan');
    } else if (vung === 'bung' || vung === 'lung') {
      mocChoc = boDemChoc(mocChoc, Date.now());
      dem('choc');
      if (mocChoc.length >= 5) {
        mocChoc = [];
        svg.classList.remove('lan'); giu('doi', 4500); noi('doi', true);
        setTimeout(() => { noi('lanh', true); giu('lanh', 1200); }, 4600);
      } else { giu('giat', 500); noi('choc'); }
    } else if (vung === 'duoi') {
      if (svg.classList.contains('bep')) return;  // đang nằm bẹp: đuôi quấn quanh người, không ở chỗ này
      giu('giat-duoi', 1000); noi('duoi'); keu('ngan');
    } else if (vung === 'chan') {
      const kieu = boChamChan(lanChamChan, Date.now());
      if (kieu === 'dap_tay') {
        lanChamChan = 0; svg.classList.remove('rut-chan'); giu('dap-tay', 1100); const dauTien = dem('dap_tay').dap_tay === 1;  /* lần đập tay đầu tiên trong ngày: đọc to; các lần sau chỉ kêu meo */
        noi('dap_tay', true, dauTien); if (!dauTien) keu('vui');
        setTimeout(() => {  // chữ "Bốp!" ngay trên bàn chân vừa giơ (khung vẽ 182,66)
          const m = svg.getScreenCTM(), r = khung.getBoundingClientRect(); if (!m) return;
          const q = new DOMPoint(182, 66).matrixTransform(m); bop(q.x - r.left, q.y - r.top);
        }, 180);
      } else {
        lanChamChan = Date.now(); giu('rut-chan', 350);
        setTimeout(() => { if (lanChamChan && Date.now() - lanChamChan >= 440) noi('chan'); }, 460);  // chờ xem có chạm lần hai không
      }
    } else if (vung === 'cam') {
      giu('gai-cam', 900); noi('gai_cam');
    } else if (vung === 'dau') {
      const q = toaDo(ev), ct = q && boChiTietDau(q.x, q.y);
      if (ct === 'mui') {  // boop mũi: nhắm tịt mắt, chun mũi, chữ "Boop!" ngay chóp mũi
        svg.classList.remove('nung-ma-trai', 'nung-ma-phai'); giu('boop', 700); dem('boop'); noi('boop', true); keu('ngan');
        const m = svg.getScreenCTM(), r = khung.getBoundingClientRect();
        if (m) { const d = new DOMPoint(126, 64).matrixTransform(m); bop(d.x - r.left, d.y - r.top, 'Boop!'); }
      } else if (ct) {  // nựng má: Bơ nghiêng đầu dụi vào phía đó, má hồng đậm, rừ rừ ngắn
        svg.classList.remove('nung-ma-trai', 'nung-ma-phai', 'boop'); giu(ct === 'ma_trai' ? 'nung-ma-trai' : 'nung-ma-phai', 1300); dem('ma'); noi('ma');
        if (!vuotDangChay) { grgr(true); setTimeout(() => { if (!vuotDangChay) grgr(false); }, 1100); }
      } else { giu('vuot', 900); const p = viTriKhung(ev); tim(p.x, p.y - 10); noi('vuot'); }
    }
  }
  // Nhấn giữ lên lưng/bụng (không kéo) khoảng 0,7 giây → Bơ lăn qua lăn lại nũng nịu
  let henLan = null, henBe = null;
  // Bế yên một lúc (không lắc lên xuống) → Bơ thả lỏng trên tay: lim dim, rừ rừ
  let henEm = null, nhacCuoi = 0, keyB = false;
  function choEm() {
    clearTimeout(henEm);
    if (svg.classList.contains('em')) { svg.classList.remove('em'); grgr(false); }
    henEm = setTimeout(() => {
      if (!svg.classList.contains('be')) return;
      svg.classList.add('em'); grgr(true); noi('em', true);
    }, 2500);
  }
  function nhac(k) {
    svg.style.setProperty('--nhac', k);
    if (!svg.classList.contains('be')) {
      svg.classList.add('be'); svg.classList.remove('vuot', 'gai-cam', 'lan', 'bep', 'nhoi');
      clearTimeout(vuotTat); vuotDangChay = false; grgr(false);
      const dauTien = dem('be').be === 1;  // lần bế đầu tiên trong ngày: đọc to; các lần sau chỉ kêu "mrr?"
      noi('be', true, dauTien); if (!dauTien) keu('ngan');
      nhacCuoi = k; choEm();
    } else if (Math.abs(k - nhacCuoi) > 0.15) { nhacCuoi = k; choEm(); }  // lắc lên xuống: Bơ chưa yên tâm
  }
  function thaBe() {
    clearTimeout(henEm);
    if (svg.classList.contains('em')) { svg.classList.remove('em'); grgr(false); }
    if (!svg.classList.contains('be')) return;
    svg.classList.remove('be'); svg.style.removeProperty('--nhac');
    giu('roi', 450); setTimeout(() => noi('tha', true), 250);
    if (typeof scheduleSleep === 'function') scheduleSleep();
  }
  face.addEventListener('pointerdown', ev => {
    const b = bam = { t: Date.now(), x: ev.clientX, y: ev.clientY, di: 0, ngu: face.dataset.e === 'ngu' };
    viTriTruoc = null; quangVuot = 0;
    try { face.setPointerCapture(ev.pointerId); } catch (e) {}
    clearTimeout(henLan);
    const p = toaDo(ev), vung = p && boVungCham(p.x, p.y);
    // Nhấn giữ đầu ~0,4 giây (không kéo) → sẵn sàng bế; kéo lên là nhấc Bơ
    if (!b.ngu && !doChoi.dieuKhien() && vung === 'dau') {
      henBe = setTimeout(() => { if (bam === b && b.di < 10 && !dangDoi()) b.sanBe = true; }, 400);
    }
    if (!b.ngu && !doChoi.dieuKhien() && (vung === 'bung' || vung === 'lung')) {
      henLan = setTimeout(() => {
        if (bam !== b || b.di >= 10 || dangDoi() || (typeof speaking !== 'undefined' && speaking)) return;
        giu('lan', 3200); noi('lan', true);
      }, 700);
    }
  });
  face.addEventListener('pointermove', ev => {
    if (doChoi.dieuKhien() || doChoi.keoLen()) return;  // đang kéo cuộn len ngang qua Bơ: không tính là vuốt
    if (bam) bam.di = Math.max(bam.di, Math.hypot(ev.clientX - bam.x, ev.clientY - bam.y));
    if (bam && bam.sanBe) {  // đang bế: kéo lên cao bao nhiêu thì nhấc bấy nhiêu, không tính là vuốt
      const k = boDoNhac(ev.clientX - bam.x, ev.clientY - bam.y);
      if (k > 0 || svg.classList.contains('be')) { nhac(k); return; }
    }
    // kéo ngón tay, hoặc rê chuột (không cần bấm) trên đầu/lưng/cằm = vuốt ve
    if (!bam && ev.pointerType !== 'mouse') return;
    const p = toaDo(ev); if (!p) return;
    const vung = boVungCham(p.x, p.y);
    if (vung === 'dau' || vung === 'lung' || vung === 'cam') vuot(ev, vung);
  });
  let vuaKeo = false;  // lần bấm vừa rồi là kéo/vuốt hay giữ lâu (không phải chạm nhanh) → hop_thoai.js không bảo Bơ im
  face.addEventListener('pointerup', ev => {
    const b = bam; bam = null; clearTimeout(henLan); clearTimeout(henBe); thaBe();
    vuaKeo = !!b && (b.di >= 10 || Date.now() - b.t >= 500);
    if (!b || doChoi.dieuKhien()) return;  // đang chơi laser/lông vũ: chạm là để điều khiển đồ chơi
    if (b.di < 10 && Date.now() - b.t < 500) {
      const p = toaDo(ev); if (p) cham(ev, boVungCham(p.x, p.y), b.ngu);
    }
  });
  face.addEventListener('pointercancel', () => { bam = null; clearTimeout(henLan); clearTimeout(henBe); thaBe(); });
  // Mất ngón tay giữa chừng (chuyển tab, cuộc gọi đến, trình duyệt giành lại cú chạm): thả Bơ xuống, không để kẹt trên không
  face.addEventListener('lostpointercapture', () => { if (svg.classList.contains('be') && !keyB) { bam = null; clearTimeout(henBe); thaBe(); } });
  document.addEventListener('visibilitychange', () => { if (document.hidden) { keyB = false; thaBe(); } });
  window.addEventListener('blur', () => { keyB = false; thaBe(); });
  // ---- Ngửi tay: giữ yên ngón tay/chuột trước mũi ~0,9 giây → Bơ rướn đầu ngửi, rồi cọ má vào tay ----
  let henNgui = null, moc = null, nguiCuoi = 0;
  function theoMui(ev) {
    const p = toaDo(ev);
    if (!p || !boGanMui(p.x, p.y)) { clearTimeout(henNgui); moc = null; return; }
    if (moc && Math.hypot(p.x - moc.x, p.y - moc.y) < 8) return;  // vẫn đang giữ yên: để hẹn giờ chạy tiếp
    moc = p; clearTimeout(henNgui);
    henNgui = setTimeout(nguiTay, 900);
  }
  function nguiTay() {
    moc = null;
    if (Date.now() - nguiCuoi < 8000 || face.dataset.e === 'ngu' || dangDoi() || doChoi.dangChoi() ||
        (typeof speaking !== 'undefined' && speaking) || svg.classList.contains('lan')) return;
    nguiCuoi = Date.now(); conChoi();
    giu('ngui', 1300);
    setTimeout(() => { if (!dangDoi()) { giu('co-ma', 1600); grgr(true); setTimeout(() => { if (!vuotDangChay) grgr(false); }, 1500);  /* đang được vuốt thì cứ rừ rừ tiếp */ noi('ngui', true); } }, 1200);
  }
  face.addEventListener('pointerdown', theoMui);
  face.addEventListener('pointermove', ev => { if (bam || ev.pointerType === 'mouse') theoMui(ev); });
  face.addEventListener('pointerup', ev => { if (ev.pointerType !== 'mouse') { clearTimeout(henNgui); moc = null; } });
  face.addEventListener('pointerleave', () => { clearTimeout(henNgui); moc = null; });
  face.addEventListener('pointercancel', () => { clearTimeout(henNgui); moc = null; });

  // Bàn phím: Tab tới Bơ rồi bấm Enter = xoa đầu, phím cách = gãi cằm (đang ngủ thì Bơ tỉnh)
  face.tabIndex = 0;
  // T = chạm tai (trái/phải ngẫu nhiên), D = đập tay, N = boop mũi, B = bế Bơ lên (giữ phím = bế lâu, thả phím = thả Bơ)
  face.addEventListener('keyup', ev => { if ((ev.key || '').toLowerCase() === 'b') { keyB = false; thaBe(); } });
  face.addEventListener('blur', () => { keyB = false; thaBe(); });
  face.addEventListener('keydown', ev => {
    const k = ev.key.length === 1 ? ev.key.toLowerCase() : ev.key;
    if (k === 'b' && !ev.ctrlKey && !ev.metaKey && !ev.altKey) {
      ev.preventDefault();
      if (ev.repeat || face.dataset.e === 'ngu' || dangDoi() || doChoi.dangChoi()) return;
      if (typeof boNgungDoc === 'function' && boNgungDoc()) return;
      keyB = true; nhac(1); return;
    }
    const vung = { Enter: 'dau', ' ': 'cam', t: Math.random() < 0.5 ? 'tai_trai' : 'tai_phai', d: 'chan', n: 'dau' }[k];
    if (!vung || ev.ctrlKey || ev.metaKey || ev.altKey) return;
    ev.preventDefault();
    if (ev.repeat) return;
    if (typeof boNgungDoc === 'function' && boNgungDoc()) return;  // đang đọc to: phím = bảo Bơ im, như chạm
    const r = face.getBoundingClientRect(), m = svg.getScreenCTM();
    // N = boop mũi: "chạm" đúng chóp mũi (khung vẽ 100,88); các phím khác chạm giữa đầu như cũ
    const giua = k === 'n' && m ? (q => ({ clientX: q.x, clientY: q.y }))(new DOMPoint(100, 88).matrixTransform(m)) : { clientX: r.left + r.width / 2, clientY: r.top + r.height * 0.3 };
    if (vung === 'chan') lanChamChan = Date.now();  // D = như chạm nhanh hai lần
    cham(giua, vung, face.dataset.e === 'ngu');  // hop_thoai.js tự đánh thức khi có phím bấm
  });
  face.addEventListener('pointerleave', () => { if (!bam) { viTriTruoc = null; } });

  // ---- Cho ăn: không có thanh "đói", cho bao nhiêu cũng được; ăn nhiều quá thì Bơ bảo no ----
  // Bấm nút = cho món đang chọn. Nhấn giữ (hoặc chuột phải, phím mũi tên lên) = mở menu chọn cá / sữa / pate.
  const nutCa = document.getElementById('choAn');
  const menuAn = document.getElementById('menuAn');
  let dangAn = false, monAn = 'ca';
  try { monAn = boMonAn(localStorage.getItem('bo_mon_an')); } catch (e) {}
  function veNutAn() {
    const m = BO_MON_AN[monAn];
    nutCa.innerHTML = m.svg;
    const nhan = 'Cho Bơ ăn ' + m.ten.toLowerCase() + ' (nhấn giữ để chọn món)';
    nutCa.setAttribute('aria-label', nhan); nutCa.title = nhan;
    if (menuAn) menuAn.querySelectorAll('button').forEach(b => b.setAttribute('aria-checked', b.dataset.mon === monAn ? 'true' : 'false'));
  }
  function choAn(mon) {
    if (dangAn || dangDoi()) return;
    dangAn = true;
    const d = dem('cho_an');
    if (d.cho_an > 5) { noi('no', true); giu('liem-mep', 1200); setTimeout(() => { dangAn = false; }, 1200); return; }
    const m = BO_MON_AN[boMonAn(mon)];
    const ca = document.createElement('span');
    ca.className = 'ca-an'; ca.innerHTML = m.svg;
    khung.appendChild(ca);
    giu('an', 2600); tiengAn(boMonAn(mon));
    setTimeout(() => {
      ca.remove(); giu('liem-mep', 1300); noi(m.cau, true);
      if (mon === 'sua') giu('dinh-sua', 3200);  // râu dính sữa một lúc
      if (mon === 'pate') { const r = face.getBoundingClientRect(), k = khung.getBoundingClientRect();  // món khoái nhất: tim bay
        [0.3, 0.7, 0.5].forEach((fx, i) => setTimeout(() => { timCuoi = 0; tim(r.left - k.left + r.width * fx, r.top - k.top + r.height * 0.25); }, i * 250)); }
    }, 2600);
    setTimeout(() => { dangAn = false; }, 3900);
  }
  function moMenuAn(banPhim) {
    if (!menuAn) return;
    menuAn.hidden = false; nutCa.setAttribute('aria-expanded', 'true');
    if (banPhim) (menuAn.querySelector('[aria-checked="true"]') || menuAn.querySelector('button')).focus();
  }
  function dongMenuAn(veNut) {
    if (!menuAn || menuAn.hidden) return;
    menuAn.hidden = true; nutCa.setAttribute('aria-expanded', 'false');
    if (veNut) nutCa.focus();
  }
  if (menuAn) {
    for (const [id, m] of Object.entries(BO_MON_AN)) {
      const b = document.createElement('button');
      b.type = 'button'; b.dataset.mon = id; b.setAttribute('role', 'menuitemradio');
      b.innerHTML = m.svg + '<span>' + m.ten + '</span>';
      b.addEventListener('click', () => {
        monAn = id; try { localStorage.setItem('bo_mon_an', id); } catch (e) {}
        veNutAn(); dongMenuAn(false); choAn(id);
      });
      menuAn.appendChild(b);
    }
    menuAn.addEventListener('keydown', ev => {
      const ds = [...menuAn.querySelectorAll('button')], i = ds.indexOf(document.activeElement);
      if (ev.key === 'Escape') { ev.preventDefault(); ev.stopPropagation(); dongMenuAn(true); }
      else if (/^Arrow(Down|Up|Left|Right)$/.test(ev.key)) {  // menu dọc (thường) hay ngang (màn hình thấp): mũi tên nào cũng đi được
        ev.preventDefault(); ds[(i + (ev.key === 'ArrowDown' || ev.key === 'ArrowRight' ? 1 : ds.length - 1)) % ds.length].focus();
      } else if (ev.key === 'Tab') dongMenuAn(false);
    });
    document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && !menuAn.hidden) dongMenuAn(menuAn.contains(document.activeElement)); });
    document.addEventListener('pointerdown', ev => { if (!menuAn.hidden && !menuAn.contains(ev.target) && ev.target !== nutCa && !nutCa.contains(ev.target)) dongMenuAn(false); });
  }
  veNutAn();
  // Nhấn giữ nút ~0,5 giây = mở menu; thả sớm = cho ăn như thường
  let giuAnTimer = null, vuaMoMenu = false, lanBamNut = 0;
  nutCa.addEventListener('pointerdown', ev => {
    lanBamNut = Date.now();
    if (ev.button !== 0) return;
    vuaMoMenu = false; clearTimeout(giuAnTimer);
    giuAnTimer = setTimeout(() => { vuaMoMenu = true; moMenuAn(false); }, 500);
  });
  ['pointerup', 'pointerleave', 'pointercancel'].forEach(t => nutCa.addEventListener(t, () => clearTimeout(giuAnTimer)));
  nutCa.addEventListener('contextmenu', ev => { ev.preventDefault(); clearTimeout(giuAnTimer); vuaMoMenu = true; moMenuAn(Date.now() - lanBamNut > 1000); });  /* phím menu trên bàn phím → đưa focus vào menu */
  nutCa.addEventListener('keydown', ev => { if (ev.key === 'ArrowUp' || ev.key === 'ArrowDown') { ev.preventDefault(); moMenuAn(true); } });
  nutCa.addEventListener('click', () => {
    if (vuaMoMenu) { vuaMoMenu = false; return; }  // vừa nhấn giữ mở menu: không cho ăn
    if (menuAn && !menuAn.hidden) { dongMenuAn(false); return; }
    choAn(monAn);
  });


  // ---- Bơ hóng chuyện: đang gõ tin thì nhìn xuống khung chat; ngừng gõ 2 giây thì thôi ----
  const oChat = document.getElementById('input');
  if (oChat && oChat.form) oChat.form.addEventListener('submit', () => svg.classList.remove('hong'));
  // Bơ để ý tin vừa gửi: nói tới cá thì liếm mép, nói thương/yêu thì tim bay, nói buồn ngủ thì ngáp lây (nghe lúc "bắt" — trước khi app.js xóa ô chữ)
  document.addEventListener('submit', ev => {
    if (!oChat || ev.target !== oChat.form) return;
    const kieu = boPhanUngTin(oChat.value);
    if (!kieu || dangDoi()) return;
    setTimeout(() => {
      if (kieu === 'ca') { giu('liem-mep', 1400); return; }
      if (kieu === 'ngap') { if (window.meo && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) meo.lan('ngap', 2200); return; }
      const r = face.getBoundingClientRect(), k = khung.getBoundingClientRect();
      [[0.3, 0.25], [0.7, 0.2], [0.5, 0.05]].forEach(([fx, fy], i) => setTimeout(() => {
        timCuoi = 0; tim(r.left - k.left + r.width * fx, r.top - k.top + r.height * fy);
      }, i * 380));
      giu('vuot', 900);
    }, 150);
  }, true);
  if (oChat) oChat.addEventListener('input', () => {
    if (face.dataset.e === 'ngu' || !oChat.value.trim()) { svg.classList.remove('hong'); return; }
    giu('hong', 2000);
  });

  // ---- Mắt nhìn theo ngón tay/chuột (ngoài lúc chơi laser); đứng yên 3 giây thì thôi nhìn ----
  let nhinTat = null, nhinCho = false, nhinEv = null;
  function nhinTheo() {
    nhinCho = false;
    const ev = nhinEv;
    if (!ev || doChoi.dangChoi() || !nhin || face.dataset.e === 'ngu' || dangDoi()) return;
    const m = svg.getScreenCTM(); if (!m) return;
    const p = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(m.inverse());
    if (Math.hypot(p.x - 100, p.y - 74) > 600) { nhin.removeAttribute('transform'); return; }  // xa quá: kệ
    const [tx, ty] = boHuongNhin(p.x - 100, p.y - 74);
    nhin.setAttribute('transform', `translate(${tx} ${ty})`);
    clearTimeout(nhinTat);
    nhinTat = setTimeout(() => { if (!doChoi.dangChoi()) nhin.removeAttribute('transform'); }, 3000);
  }
  document.addEventListener('pointermove', ev => {
    if (ev.pointerType !== 'mouse' && !bam) return;  // điện thoại: chỉ khi đang chạm vào Bơ
    nhinEv = ev;
    if (!nhinCho) { nhinCho = true; requestAnimationFrame(nhinTheo); }
  }, { passive: true });

  // ---- Lắc điện thoại → Bơ chóng mặt. Android: chạy luôn (tắt được trong Cài đặt). iPhone: phải bấm bật trong Cài đặt để máy hỏi cho phép ----
  const lacNhan = document.getElementById('lacNhan'), lacBat = document.getElementById('lacBat');
  const canHoi = window.DeviceMotionEvent && typeof DeviceMotionEvent.requestPermission === 'function';
  let lacMoc = [], lacTruoc = null, lacCuoi = 0, dangNgheLac = false;
  function khiLac(ev) {
    const a = ev.accelerationIncludingGravity; if (!a) return;
    const kq = boLac(lacMoc, Date.now(), boDoGiat(lacTruoc, a));
    lacTruoc = { x: a.x, y: a.y, z: a.z }; lacMoc = kq.moc;
    if (!kq.lac || Date.now() - lacCuoi < 5000 || document.hidden) return;
    lacMoc = []; lacCuoi = Date.now();
    if (face.dataset.e === 'ngu' || dangDoi()) return;
    conChoi(); svg.classList.remove('lan'); giu('chong-mat', 2600); noi('chong_mat', true);
  }
  function ngheLac(bat) {
    if (bat === dangNgheLac) return;
    dangNgheLac = bat; lacTruoc = null; lacMoc = [];
    bat ? window.addEventListener('devicemotion', khiLac) : window.removeEventListener('devicemotion', khiLac);
  }
  if (window.DeviceMotionEvent && lacNhan && lacBat && ('ontouchstart' in window || navigator.maxTouchPoints > 0)) {
    let luu = null; try { luu = localStorage.getItem('bo_lac'); } catch (e) {}
    lacNhan.hidden = false;
    lacBat.checked = canHoi ? luu === '1' : luu !== '0';  // iPhone: quyền cấp theo lần mở trang, nên đã bật thì thử nghe luôn
    if (lacBat.checked) ngheLac(true);
    // iPhone: quyền có thể mất sau khi tải lại trang → lần chạm Bơ đầu tiên hỏi lại (đã cho phép rồi thì máy không hiện hộp hỏi)
    if (canHoi && lacBat.checked) face.addEventListener('pointerdown', () => {
      DeviceMotionEvent.requestPermission().then(kq => { if (kq !== 'granted') ngheLac(false); }).catch(() => {});
    }, { once: true });
    lacBat.addEventListener('change', () => {
      const bat = lacBat.checked;
      try { localStorage.setItem('bo_lac', bat ? '1' : '0'); } catch (e) {}
      if (!bat) { ngheLac(false); return; }
      if (!canHoi) { ngheLac(true); return; }
      DeviceMotionEvent.requestPermission().then(kq => {
        if (kq === 'granted') ngheLac(true);
        else { lacBat.checked = false; try { localStorage.setItem('bo_lac', '0'); } catch (e) {} }
      }).catch(() => { lacBat.checked = false; });
    });
  }

  // ---- Gợi ý trò chưa thử: mở web khoảng 40 giây, Bơ đang rảnh thì nói một câu gợi ý (tối đa 1 lần/ngày, chỉ chữ) ----
  setTimeout(function goiY() {
    const ban = face.dataset.e === 'ngu' || dangDoi() || doChoi.dangChoi() || document.hidden ||
      (typeof speaking !== 'undefined' && speaking) || (document.getElementById('input') || {}).value ||
      document.querySelector('dialog[open]') || !bong.hidden;
    if (ban) { setTimeout(goiY, 30000); return; }  // đang bận: lát nữa thử lại
    let ngay = ''; try { ngay = localStorage.getItem('bo_goi_y_ngay') || ''; } catch (e) {}
    const k = boGoiY(docDaThu(), ngay, homNay(), !!(lacBat && lacBat.checked));
    if (!k) return;
    try { localStorage.setItem('bo_goi_y_ngay', homNay()); } catch (e) {}
    giu('nghieng', 1200); hienBong(BO_GOI_Y[k], 6000);
  }, 40000);

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

  const conChoi = () => { if (typeof scheduleSleep === 'function') scheduleSleep(); };  // đang chơi: đừng nằm bẹp/ngủ gật
  // Cho do_choi.js (và các file khác) dùng chung
  window.boChoi = { dem, lucMo, noi, keu, vuaKeo: () => vuaKeo, giu, dangDoi, conChoi, doChoi, face, khung, svg, nhin, header: khung.closest('header') || khung };
})();
