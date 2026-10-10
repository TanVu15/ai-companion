// Khung chat của Bơ: gửi tin, bong bóng, khuôn mặt, lịch sử. Các phần khác: giong_noi.js, khoi_dong.js, hop_thoai.js
// Mọi lệnh gửi máy chủ Bơ đều kèm header X-Bo (máy chủ chặn lệnh thiếu header này, chống trang lạ phá dữ liệu)
const _fetch = window.fetch.bind(window);
window.fetch = (url, opts = {}) => {
  if (typeof url === 'string' && url.startsWith('/api/')) opts = { ...opts, headers: { ...(opts.headers || {}), 'X-Bo': '1' } };
  return _fetch(url, opts);
};
const log = document.getElementById('log'), form = document.getElementById('form');
const input = document.getElementById('input'), send = document.getElementById('send');
const face = document.getElementById('face'), statusEl = document.getElementById('status');

function timeLabel(t) {
  // t dạng "YYYY-MM-DD HH:MM:SS" (giờ máy chủ); không có thì là bây giờ
  const d = t ? new Date(t.replace(' ', 'T')) : new Date();
  if (isNaN(d)) return '';
  const hm = d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const days = Math.round((today - new Date(d).setHours(0, 0, 0, 0)) / 86400000);
  return days <= 0 ? hm : days === 1 ? 'hôm qua ' + hm : d.toLocaleDateString('vi-VN') + ' ' + hm;
}
function makeMsg(role, text, t, id, pinned) {
  const d = document.createElement('div');
  d.className = 'msg ' + role + (pinned ? ' pinned' : ''); d.textContent = text;
  if (id) d.dataset.id = id;
  if (role !== 'error') {
    const s = document.createElement('span'); s.className = 'time'; s.textContent = timeLabel(t);
    d.appendChild(s);
  }
  return d;
}
// Tin của Bơ có thể là 2–3 bong bóng; giờ chỉ hiện ở bong bóng cuối
function makeMsgs(role, text, t, id, pinned) {
  if (role !== 'assistant') return [makeMsg(role, text, t, id, pinned)];
  const parts = boTachTin(text);
  return parts.map((p, i) => {
    const d = makeMsg(role, p, t, id, pinned);
    if (i < parts.length - 1) d.querySelector('.time').remove();
    return d;
  });
}
function add(role, text, t, id, pinned) {
  const ds = makeMsgs(role, text, t, id, pinned);
  ds.forEach(d => log.appendChild(d)); log.scrollTop = log.scrollHeight;
  return ds[ds.length - 1];
}
const wait = ms => new Promise(r => setTimeout(r, ms));
// Bơ "gõ" từng bong bóng một, có dấu ba chấm ở giữa
// Mọi lời của Bơ xếp hàng: lời nhắc/lời chào/câu trả lời không chen vào giữa các bong bóng của nhau
let boQueue = Promise.resolve();
function addBo(text, id) {
  boQueue = boQueue.then(() => addBoNow(text, id)).catch(() => {});
  return boQueue;
}
async function addBoNow(text, id) {
  const bubbles = makeMsgs('assistant', text, null, id);
  for (let i = 0; i < bubbles.length; i++) {
    if (i > 0) {
      const dots = document.createElement('div');
      dots.className = 'msg assistant typing'; dots.setAttribute('aria-label', 'Bơ đang gõ');
      dots.innerHTML = '<span></span><span></span><span></span>';
      log.appendChild(dots); log.scrollTop = log.scrollHeight;
      await wait(Math.min(1400, 400 + bubbles[i].textContent.length * 15));
      dots.remove();
    }
    log.appendChild(bubbles[i]); log.scrollTop = log.scrollHeight;
  }
}
function express(emotion, action) {
  face.dataset.e = emotion || 'binh_thuong';
  face.className = 'face';
  void face.offsetWidth;
  if (action && action !== 'khong') face.classList.add('a-' + action);
  if (emotion !== 'ngu' && typeof scheduleSleep === 'function') scheduleSleep();  // đổi mặt = đang thức
}
let oldestId = null, noMore = false, loadingOld = false;
async function loadHistory() {
  try {
    const r = await fetch('/api/history');
    if (!r.ok) return;
    const list = await r.json();
    list.forEach(m => add(m.role, m.content, m.created_at, m.id, m.ghim));
    const lastBo = list.filter(m => m.role === 'assistant' && m.cam_xuc).pop();
    if (lastBo) express(lastBo.cam_xuc);  // mở lại web: Bơ giữ vẻ mặt lúc nói câu cuối
    if (list.length) oldestId = list[0].id; else { noMore = true; showChips(); }
    if (list.length < 50) noMore = true;
  } catch (e) {}
}
// Lần đầu (chưa có tin nhắn nào): vài câu gợi ý, bấm là gửi
const STARTERS = ['Chào Bơ! Mình tên là ...', 'Kể mình nghe chuyện gì vui đi', '8h tối nay nhắc mình gọi mẹ nha', 'Bơ làm được những gì?'];
function showChips() {
  const box = document.createElement('div');
  box.className = 'chips'; box.id = 'chips';
  STARTERS.forEach(t => {
    const b = document.createElement('button');
    b.type = 'button'; b.textContent = t;
    b.onclick = () => {
      input.value = t;
      if (t.endsWith('...')) { input.value = t.slice(0, -3); input.focus(); return; }  // để Tân tự gõ tên
      form.requestSubmit();
    };
    box.appendChild(b);
  });
  log.appendChild(box);
}
async function loadOlder() {
  if (noMore || loadingOld || oldestId === null) return;
  loadingOld = true;
  try {
    const r = await fetch('/api/history?before_id=' + oldestId);
    const list = r.ok ? await r.json() : [];
    if (list.length < 50) noMore = true;
    if (list.length) {
      oldestId = list[0].id;
      const before = log.scrollHeight, frag = document.createDocumentFragment();
      list.forEach(m => makeMsgs(m.role, m.content, m.created_at, m.id, m.ghim).forEach(d => frag.appendChild(d)));
      log.prepend(frag);
      log.scrollTop += log.scrollHeight - before;  // giữ nguyên chỗ đang đọc
    }
  } catch (e) {}
  loadingOld = false;
}
log.addEventListener('scroll', () => { if (log.scrollTop < 40) loadOlder(); });
function addError(text, retry) {
  add('error', text);
  if (!retry) return;
  const b = document.createElement('button');
  b.type = 'button'; b.className = 'retry'; b.textContent = 'Thử lại';
  b.onclick = () => { b.closest('.msg').remove(); retry(); };
  log.lastChild.appendChild(b);
}
async function sendText(text, userBubble) {
  send.disabled = true;
  statusEl.textContent = 'Bơ đang nghĩ...'; express('suy_nghi');
  const ctrl = new AbortController(), timer = setTimeout(() => ctrl.abort(), 150000);
  try {
    const r = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text }), signal: ctrl.signal });
    let data = {};
    try { data = await r.json(); } catch (e) {}
    if (!r.ok) throw new Error(data.detail || 'Máy chủ trả lỗi ' + r.status);
    if (userBubble && data.id_nguoi_dung) userBubble.dataset.id = data.id_nguoi_dung;
    try { if (localStorage.getItem('bo_nhap') === text && !input.value) localStorage.removeItem('bo_nhap'); } catch (x) {}
    express(data.cam_xuc, data.hanh_dong); speak(data.noi); await addBo(data.noi, data.id);
  } catch (e) {
    const msg = e.name === 'AbortError' ? 'Bơ nghĩ lâu quá, thử lại nha.'
      : e instanceof TypeError ? 'Không kết nối được máy chủ. Máy chủ còn chạy không?' : e.message;
    addError(msg, () => sendText(text, userBubble)); express('buon');
    // Gửi lỗi: giữ tin vào bản nháp, lỡ tải lại trang thì tin vẫn nằm trong ô nhập để gửi lại
    try { if (!input.value) localStorage.setItem('bo_nhap', text); } catch (x) {}
  } finally {
    clearTimeout(timer);
    send.disabled = false; statusEl.textContent = ''; input.focus();
    if (handsFree) resumeListening();
  }
}
form.addEventListener('submit', (ev) => {
  ev.preventDefault();
  const text = input.value.trim();
  if (!text || send.disabled) return;
  const chips = document.getElementById('chips'); if (chips) chips.remove();
  const bubble = add('user', text); input.value = '';
  if (/nhắc/i.test(text)) askNotify();
  sendText(text, bubble);
});
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
});
