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

if (typeof module !== 'undefined') module.exports = { boChuDeDoc, boTachTin, boGiongViet, boChonGiong, boGiongKe };
