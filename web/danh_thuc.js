// Nhận ra tiếng gọi "Bơ ơi" (từ đánh thức) trong câu nhận dạng giọng nói.
// Trả về: null nếu không gọi Bơ; "" nếu chỉ gọi mà chưa nói gì; còn lại là phần nói sau tiếng gọi.
// Máy nghe tiếng Việt hay nhầm dấu ("bờ ơi", "bơ ới"), nên chấp nhận vài cách viết gần giống.
const BO_GOI = /(?:^|[\s,.!?])(?:(?:ê|này|hey|hây)\s+b[ơờởớo](?=$|[\s,.!?])|b[ơờởớo]\s+[ơờớở]i(?=$|[\s,.!?]))[\s,.!?]*/;

function boDanhThuc(text) {
  const t = (text || '').normalize('NFC');
  const m = BO_GOI.exec(t.toLowerCase());
  if (!m) return null;
  return t.slice(m.index + m[0].length).trim();
}

if (typeof module !== 'undefined') module.exports = { boDanhThuc };
