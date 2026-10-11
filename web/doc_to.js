// Xử lý chữ trước khi hiện/đọc.
// Chuẩn bị chữ trước khi đọc to: bỏ emoji, ký hiệu định dạng, đường link (đọc lên nghe rất kỳ).
function boChuDeDoc(text) {
  return (text || '')
    .normalize('NFC')
    .replace(/https?:\/\/\S+/g, ' ')                         // đường link
    .replace(/\p{Extended_Pictographic}|\p{Emoji_Modifier}|‍|️/gu, ' ') // emoji
    .replace(/[*_~`#>|\[\]{}<>^]/g, ' ')                     // ký hiệu định dạng
    .replace(/(^|\s)[:;=]-?[)(DPpOo3]+(?=\s|$)/g, ' ')       // mặt cười kiểu chữ :) :D
    .replace(/([!?.,])\1+/g, '$1')                           // "!!!" → "!"
    .replace(/\s+/g, ' ')
    .replace(/\s+([!?.,])/g, '$1')
    .trim();
}

// Tách câu trả lời dài thành 2–3 tin nhắn nhỏ, như người thật nhắn tin. Câu ngắn thì giữ nguyên.
function boTachTin(text, toiDa = 3) {
  const t = (text || '').trim();
  if (t.length < 60) return t ? [t] : [];
  // Tách sau dấu câu + khoảng trắng ("3.5 triệu" không bị tách). Không dùng lookbehind vì Safari cũ không hiểu.
  const raw = t.split(/([.!?…]+)\s+/), cau = [];
  for (let i = 0; i < raw.length; i += 2) cau.push((raw[i] + (raw[i + 1] || '')).trim());
  cau.splice(0, cau.length, ...cau.filter(Boolean));
  if (cau.length < 2) return [t];
  // gộp câu quá ngắn ("Ừa.", "Wow!") vào câu kế tiếp cho tự nhiên
  const gom = [];
  for (const c of cau) {
    if (gom.length && gom[gom.length - 1].length < 15) gom[gom.length - 1] += ' ' + c;
    else gom.push(c);
  }
  while (gom.length > toiDa) gom.splice(toiDa - 1, 2, gom[toiDa - 1] + ' ' + gom[toiDa]);
  return gom;
}

// Tách chữ để đọc bằng giọng AI: đoạn đầu là câu đầu tiên (tạo nhanh, đỡ chờ), các đoạn sau gộp lại tới khoảng `dai` chữ.
// Câu quá dài (không có dấu câu) thì cắt ở dấu phẩy/khoảng trắng gần nhất.
function boTachCauDoc(text, dai = 220) {
  const t = (text || '').replace(/\s+/g, ' ').trim();
  if (!t) return [];
  const raw = t.split(/([.!?…]+)\s+/), cau = [];
  for (let i = 0; i < raw.length; i += 2) cau.push((raw[i] + (raw[i + 1] || '')).trim());
  const nho = [];
  for (let c of cau.filter(Boolean)) {
    while (c.length > dai) {
      let k = Math.max(c.lastIndexOf(', ', dai), c.lastIndexOf(' ', dai));
      if (k < dai / 3) { nho.push(c.slice(0, dai)); c = c.slice(dai); continue; }  // không có chỗ ngắt: cắt cứng
      nho.push(c.slice(0, k + (c[k] === ',' ? 1 : 0)).trim()); c = c.slice(k + 1).trim();
    }
    if (c) nho.push(c);
  }
  const out = [nho[0]];
  for (const c of nho.slice(1)) {
    if (out.length > 1 && out[out.length - 1].length + c.length + 1 <= dai) out[out.length - 1] += ' ' + c;
    else out.push(c);
  }
  return out;
}

// Các giọng tiếng Việt của máy, và giọng đang chọn (giọng đã lưu nếu còn, không thì giọng tiếng Việt đầu tiên)
function boGiongViet(voices) {
  return (voices || []).filter(v => v.lang && v.lang.toLowerCase().replace('_', '-').startsWith('vi'));
}
function boChonGiong(voices, tenDaLuu) {
  const vi = boGiongViet(voices);
  return vi.find(v => v.name === tenDaLuu) || vi[0] || null;
}
// Bấm nút "Giọng" → sang giọng kế tiếp (hết thì quay lại đầu)
function boGiongKe(voices, tenHienTai) {
  const vi = boGiongViet(voices);
  if (!vi.length) return null;
  const i = vi.findIndex(v => v.name === tenHienTai);
  return vi[(i + 1) % vi.length];
}

// Giờ yên lặng dạng "23-6" (qua nửa đêm) hoặc "13-14". Sai định dạng / trống → không yên lặng.
function boGioYenLang(gio, khoang) {
  const m = /^\s*(\d{1,2})\s*-\s*(\d{1,2})\s*$/.exec(khoang || '');
  if (!m) return false;
  const a = +m[1], b = +m[2];
  if (a > 23 || b > 24 || a === b) return false;
  return a < b ? gio >= a && gio < b : gio >= a || gio < b;
}

if (typeof module !== 'undefined') module.exports = { boChuDeDoc, boTachTin, boTachCauDoc, boGiongViet, boChonGiong, boGiongKe, boGioYenLang };
