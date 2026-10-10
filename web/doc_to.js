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

if (typeof module !== 'undefined') module.exports = { boChuDeDoc };
