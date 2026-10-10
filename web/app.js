// Giao diện chat của Bơ: gửi tin, khuôn mặt, giọng nói, trí nhớ, chi phí, lời nhắc.
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
function makeMsg(role, text, t) {
  const d = document.createElement('div');
  d.className = 'msg ' + role; d.textContent = text;
  if (role !== 'error') {
    const s = document.createElement('span'); s.className = 'time'; s.textContent = timeLabel(t);
    d.appendChild(s);
  }
  return d;
}
function add(role, text, t) {
  log.appendChild(makeMsg(role, text, t)); log.scrollTop = log.scrollHeight;
}
function express(emotion, action) {
  face.dataset.e = emotion || 'binh_thuong';
  face.className = 'face';
  void face.offsetWidth;
  if (action && action !== 'khong') face.classList.add('a-' + action);
}
let oldestId = null, noMore = false, loadingOld = false;
async function loadHistory() {
  try {
    const r = await fetch('/api/history');
    if (!r.ok) return;
    const list = await r.json();
    list.forEach(m => add(m.role, m.content, m.created_at));
    if (list.length) oldestId = list[0].id; else noMore = true;
    if (list.length < 50) noMore = true;
  } catch (e) {}
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
      list.forEach(m => frag.appendChild(makeMsg(m.role, m.content, m.created_at)));
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
async function sendText(text) {
  send.disabled = true;
  statusEl.textContent = 'Bơ đang nghĩ...'; express('suy_nghi');
  const ctrl = new AbortController(), timer = setTimeout(() => ctrl.abort(), 150000);
  try {
    const r = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text }), signal: ctrl.signal });
    let data = {};
    try { data = await r.json(); } catch (e) {}
    if (!r.ok) throw new Error(data.detail || 'Máy chủ trả lỗi ' + r.status);
    add('assistant', data.noi); express(data.cam_xuc, data.hanh_dong); speak(data.noi);
  } catch (e) {
    const msg = e.name === 'AbortError' ? 'Bơ nghĩ lâu quá, thử lại nha.'
      : e instanceof TypeError ? 'Không kết nối được máy chủ. Máy chủ còn chạy không?' : e.message;
    addError(msg, () => sendText(text)); express('buon');
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
  add('user', text); input.value = '';
  if (/nhắc/i.test(text)) askNotify();
  sendText(text);
});
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
});
// ---- Giọng nói: dùng sẵn của trình duyệt (miễn phí, không cần tài khoản) ----
let voiceOn = false, speaking = false;
try { voiceOn = localStorage.getItem('bo_voice') === '1'; } catch (e) {}
const voiceBtn = document.getElementById('voiceBtn'), micBtn = document.getElementById('mic');
const RATES = [['vừa', 1], ['nhanh', 1.25], ['chậm', 0.8]];
let rateIdx = 0;
try { rateIdx = Math.max(0, RATES.findIndex(r => r[0] === localStorage.getItem('bo_rate'))); } catch (e) {}
const rateBtn = document.getElementById('rateBtn');
function showVoice() {
  voiceBtn.textContent = 'Giọng nói: ' + (voiceOn ? 'bật' : 'tắt'); voiceBtn.setAttribute('aria-pressed', voiceOn);
  rateBtn.hidden = !voiceOn; rateBtn.textContent = 'Tốc độ đọc: ' + RATES[rateIdx][0];
}
rateBtn.onclick = () => {
  rateIdx = (rateIdx + 1) % RATES.length; showVoice();
  try { localStorage.setItem('bo_rate', RATES[rateIdx][0]); } catch (e) {}
  speak('Bơ đọc ' + RATES[rateIdx][0] + ' như này nha');
};
showVoice();
voiceBtn.onclick = () => {
  voiceOn = !voiceOn; showVoice();
  try { localStorage.setItem('bo_voice', voiceOn ? '1' : '0'); } catch (e) {}
  if (!voiceOn && window.speechSynthesis) { speechSynthesis.cancel(); speaking = false; face.classList.remove('talking'); }
};
function viVoice() {
  const all = window.speechSynthesis ? speechSynthesis.getVoices() : [];
  return all.find(v => v.lang && v.lang.toLowerCase().startsWith('vi')) || null;
}
let speakSeq = 0;
function speak(text) {
  text = boChuDeDoc(text);
  if (!voiceOn || !window.speechSynthesis || !text) return;
  const id = ++speakSeq;  // chỉ lần đọc mới nhất được báo "đọc xong"
  if (handsFree) pauseListening();  // đừng để micro nghe giọng của chính Bơ
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'vi-VN'; u.rate = RATES[rateIdx][1]; const v = viVoice(); if (v) u.voice = v;
  u.onstart = () => face.classList.add('talking');
  u.onend = u.onerror = () => {
    if (id !== speakSeq) return;  // lần đọc cũ bị ngắt thì bỏ qua
    speaking = false; face.classList.remove('talking'); resumeListening();
  };
  speaking = true; speechSynthesis.speak(u);
  // Phòng khi trình duyệt quên báo "đọc xong" → rảnh tay không bị kẹt
  setTimeout(() => { if (speaking) u.onend(); }, 3000 + text.length * 150);
}
const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
const handsBtn = document.getElementById('handsBtn');
let rec = null, listening = false, handsFree = false, paused = false, awaitUntil = 0, micSession = false;
function startRec() {
  if (!rec || listening) return;
  rec.continuous = handsFree; rec.interimResults = !handsFree;
  try { rec.start(); listening = true; } catch (e) {}
}
function showHands() {
  handsBtn.textContent = 'Rảnh tay: ' + (handsFree ? 'bật' : 'tắt'); handsBtn.setAttribute('aria-pressed', handsFree);
  statusEl.textContent = handsFree ? 'Gọi "Bơ ơi" để nói chuyện' : '';
}
// Đang gửi tin hoặc Bơ đang nói thì tạm ngừng nghe (để Bơ không tự nghe giọng mình)
function pauseListening() { paused = true; if (rec && listening) rec.abort(); }
function resumeListening() {
  if (!handsFree || !paused || speaking || send.disabled) return;
  paused = false; statusEl.textContent = 'Gọi "Bơ ơi" để nói chuyện'; startRec();
}
function handsHeard(text) {
  let cmd = Date.now() < awaitUntil ? text.trim() : boDanhThuc(text);
  if (cmd === null || send.disabled) return;
  if (cmd === '') { awaitUntil = Date.now() + 8000; express('ngac_nhien'); statusEl.textContent = 'Bơ nghe nè...'; return; }
  awaitUntil = 0; input.value = cmd; pauseListening(); form.requestSubmit();
}
if (Rec && window.isSecureContext) {
  micBtn.hidden = false; handsBtn.hidden = false;
  rec = new Rec(); rec.lang = 'vi-VN';
  rec.onresult = (ev) => {
    if (handsFree) {
      for (let i = ev.resultIndex; i < ev.results.length; i++)
        if (ev.results[i].isFinal) handsHeard(ev.results[i][0].transcript);
    } else {
      input.value = Array.from(ev.results).map(r => r[0].transcript).join('');
    }
  };
  rec.onend = () => {
    listening = false; micBtn.classList.remove('on');
    if (handsFree) { if (!paused) setTimeout(startRec, 300); return; }  // máy tự ngắt sau một lúc → nghe lại
    statusEl.textContent = '';
    // chỉ tự gửi khi người dùng vừa bấm micro (không gửi chữ đang gõ dở lúc tắt rảnh tay)
    if (micSession && input.value.trim() && !send.disabled) form.requestSubmit();
    micSession = false;
  };
  rec.onerror = (ev) => {
    if (ev.error === 'not-allowed') {
      handsFree = false; micBtn.disabled = false; showHands();
      addError('Trình duyệt chưa cho dùng micro. Bấm vào biểu tượng ổ khóa trên thanh địa chỉ để cho phép.');
    } else if (!['no-speech', 'aborted', 'network'].includes(ev.error)) addError('Không nghe được: ' + ev.error);
  };
  micBtn.onclick = () => {
    if (handsFree) return;
    if (listening) { rec.stop(); return; }
    if (window.speechSynthesis) speechSynthesis.cancel();
    input.value = ''; micSession = true; micBtn.classList.add('on'); statusEl.textContent = 'Bơ đang nghe...';
    startRec();
  };
  handsBtn.onclick = () => {
    handsFree = !handsFree; paused = false; awaitUntil = 0; micSession = false; showHands();
    micBtn.disabled = handsFree;
    if (listening) rec.abort(); else if (handsFree) startRec();
  };
}

const costDlg = document.getElementById('cost'), costList = document.getElementById('costList');
function money(usd) { return '$' + usd.toFixed(usd < 1 ? 4 : 2) + ' (~' + Math.round(usd * 25000).toLocaleString('vi-VN') + 'đ)'; }
document.getElementById('openCost').onclick = async () => {
  costList.innerHTML = '<li>Đang tải...</li>'; costDlg.showModal();
  try {
    const d = await (await fetch('/api/chi-phi')).json();
    const rows = [
      ['Hôm nay', d.hom_nay.calls + ' câu gọi API, ' + money(d.hom_nay.usd)],
      ['Tháng này', d.thang_nay.calls + ' câu gọi API, ' + money(d.thang_nay.usd)],
      ['Bơ đã trả lời hôm nay', d.da_tra_loi_hom_nay + ' / ' + d.gioi_han_ngay + ' câu (giới hạn ngày)'],
      ['Ngân sách tháng', d.ngan_sach_thang > 0
        ? money(d.ngan_sach_thang) + ' — đã dùng ' + Math.min(100, Math.round(d.thang_nay.usd / d.ngan_sach_thang * 100)) + '%'
        : 'không giới hạn (đặt MONTHLY_USD_LIMIT trong .env)'],
    ];
    costList.innerHTML = '';
    rows.forEach(([k, v]) => { const li = document.createElement('li'); li.textContent = k + ': ' + v; costList.appendChild(li); });
  } catch (e) { costList.innerHTML = '<li>Không tải được.</li>'; }
};
document.getElementById('closeCost').onclick = () => costDlg.close();

async function greet() {
  try {
    const r = await fetch('/api/chao', { method: 'POST' });
    const data = await r.json();
    if (r.ok && data.noi) { add('assistant', data.noi); express(data.cam_xuc, data.hanh_dong); speak(data.noi); }
  } catch (e) {}
}
// ---- Lời nhắc: hỏi máy chủ mỗi 30 giây (chỉ khi web đang mở) ----
async function pollReminders() {
  try {
    const r = await fetch('/api/nhac');
    if (!r.ok) return;
    for (const x of await r.json()) {
      add('assistant', x.noi); express(x.cam_xuc, x.hanh_dong); speak(x.noi);
      if (window.Notification && Notification.permission === 'granted' && document.hidden) new Notification('Bơ', { body: x.noi, icon: '/web/icon-180.png' });
    }
  } catch (e) {}
}
setInterval(pollReminders, 30000);
// Lần đầu Tân nhờ nhắc việc thì xin phép hiện thông báo (để thấy được cả khi đang ở tab khác)
function askNotify() {
  if (window.Notification && Notification.permission === 'default') Notification.requestPermission().catch(() => {});
}

async function checkHealth() {
  try {
    const d = await (await fetch('/api/suc-khoe')).json();
    if (d.ok) return true;
    d.kiem_tra.filter(c => c.muc === 'loi').forEach(c => add('error', c.ten + ': ' + c.ghi_chu));
    express('buon'); return false;
  } catch (e) { return true; }
}
loadHistory().then(checkHealth).then(async ok => { if (ok) { await greet(); pollReminders(); } });

const mem = document.getElementById('mem'), factsEl = document.getElementById('facts');
async function delFact(content) {
  await fetch('/api/facts', { method: 'DELETE', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ content }) });
}
async function loadFacts() {
  factsEl.innerHTML = '';
  let list = [];
  try { const r = await fetch('/api/facts'); if (r.ok) list = await r.json(); } catch (e) {}
  if (!list.length) { const li = document.createElement('li'); li.textContent = 'Bơ chưa nhớ gì cả.'; factsEl.appendChild(li); }
  list.forEach(f => {
    const li = document.createElement('li'), span = document.createElement('span'), b = document.createElement('button');
    span.textContent = f; b.textContent = 'Xóa'; b.type = 'button';
    b.setAttribute('aria-label', 'Xóa: ' + f);
    b.onclick = async () => { await delFact(f); loadFacts(); };
    li.append(span, b); factsEl.appendChild(li);
  });
}
const remsEl = document.getElementById('rems');
async function loadReminders() {
  remsEl.innerHTML = '';
  let list = [];
  try { const r = await fetch('/api/nhac/sap-toi'); if (r.ok) list = await r.json(); } catch (e) {}
  if (!list.length) { const li = document.createElement('li'); li.textContent = 'Chưa có. Thử nhắn: "8h tối nhắc mình gọi mẹ".'; remsEl.appendChild(li); }
  list.forEach(x => {
    const li = document.createElement('li'), b = document.createElement('button');
    li.textContent = x.luc.slice(11) + ' ' + x.luc.slice(8, 10) + '/' + x.luc.slice(5, 7) + ' — ' + x.viec + ' ';
    b.textContent = 'Xóa'; b.type = 'button'; b.className = 'link'; b.setAttribute('aria-label', 'Xóa lời nhắc: ' + x.viec);
    b.onclick = async () => { await fetch('/api/nhac/' + x.id, { method: 'DELETE' }); loadReminders(); };
    li.appendChild(b); remsEl.appendChild(li);
  });
}
document.getElementById('openMem').onclick = () => { loadFacts(); loadReminders(); mem.showModal(); };
document.getElementById('closeMem').onclick = () => mem.close();
document.getElementById('restoreFile').onchange = async (ev) => {
  const file = ev.target.files[0]; ev.target.value = '';
  if (!file || !confirm('Nạp bản sao lưu sẽ THAY toàn bộ trí nhớ và tin nhắn hiện tại. Tiếp tục?')) return;
  try {
    const r = await fetch('/api/khoi-phuc', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: await file.text() });
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || 'Lỗi');
    alert('Đã nạp xong!'); location.reload();
  } catch (e) { alert('Không nạp được: ' + e.message); }
};
document.getElementById('clearMem').onclick = async () => {
  if (!confirm('Xóa hết những điều Bơ đã nhớ?')) return;
  await fetch('/api/facts/all', { method: 'DELETE' }); loadFacts();
};
