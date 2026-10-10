// Các hộp thoại và tiện ích: trí nhớ, ngủ gật, tìm, "?", ghim, tính cách, màu mặt, phím tắt.
const mem = document.getElementById('mem'), factsEl = document.getElementById('facts');
async function delFact(content) {
  await fetch('/api/facts', { method: 'DELETE', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ content }) });
}
// Lỡ tay xóa → bấm "Hoàn tác" để Bơ nhớ lại (thêm lại vào cuối danh sách)
let undoTimer = null;
function showUndo(f) {
  const bar = document.getElementById('undoBar');
  clearTimeout(undoTimer);
  bar.innerHTML = '';
  const t = document.createElement('span'), b = document.createElement('button');
  t.textContent = 'Đã xóa: ' + f + ' ';
  b.type = 'button'; b.className = 'link'; b.textContent = 'Hoàn tác';
  b.onclick = async () => {
    await fetch('/api/facts', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ content: f }) });
    bar.hidden = true; loadFacts();
  };
  bar.append(t, b); bar.hidden = false;
  undoTimer = setTimeout(() => { bar.hidden = true; }, 10000);
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
    b.onclick = async () => { await delFact(f); await loadFacts(); showUndo(f); };
    const e = document.createElement('button');
    e.textContent = 'Sửa'; e.type = 'button'; e.className = 'edit'; e.setAttribute('aria-label', 'Sửa: ' + f);
    e.onclick = async () => {
      const moi = prompt('Sửa điều Bơ nhớ:', f);
      if (moi === null || moi.trim() === f) return;
      const r = await fetch('/api/facts', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ cu: f, moi }) });
      if (!r.ok) { try { alert((await r.json()).detail); } catch (x) { alert('Không sửa được'); } }
      loadFacts();
    };
    li.append(span, e, b); factsEl.appendChild(li);
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
    const lap = x.lap === 'ngay' ? ' (mỗi ngày)' : x.lap === 'tuan' ? ' (mỗi tuần)' : '';
    li.textContent = x.luc.slice(11) + ' ' + x.luc.slice(8, 10) + '/' + x.luc.slice(5, 7) + ' — ' + x.viec + lap + ' ';
    b.textContent = 'Xóa'; b.type = 'button'; b.className = 'link'; b.setAttribute('aria-label', 'Xóa lời nhắc: ' + x.viec);
    b.onclick = async () => { await fetch('/api/nhac/' + x.id, { method: 'DELETE' }); loadReminders(); };
    const e = document.createElement('button');
    e.textContent = 'Sửa'; e.type = 'button'; e.className = 'link'; e.setAttribute('aria-label', 'Sửa lời nhắc: ' + x.viec);
    e.onclick = () => editReminder(li, x);
    li.append(e, document.createTextNode(' '), b); remsEl.appendChild(li);
  });
}
// Sửa lời nhắc ngay trong danh sách: việc, ngày giờ, lặp lại
function editReminder(li, x) {
  li.innerHTML = '';
  const f = document.createElement('form'); f.className = 'rem-edit';
  const viec = document.createElement('input'); viec.type = 'text'; viec.maxLength = 200; viec.value = x.viec;
  viec.setAttribute('aria-label', 'Việc cần nhắc');
  const luc = document.createElement('input'); luc.type = 'datetime-local'; luc.value = x.luc.replace(' ', 'T');
  luc.setAttribute('aria-label', 'Ngày giờ nhắc');
  const lap = document.createElement('select'); lap.setAttribute('aria-label', 'Lặp lại');
  [['', 'Một lần'], ['ngay', 'Mỗi ngày'], ['tuan', 'Mỗi tuần']].forEach(([v, t]) => {
    const o = document.createElement('option'); o.value = v; o.textContent = t; if ((x.lap || '') === v) o.selected = true; lap.appendChild(o);
  });
  const err = document.createElement('span'); err.className = 'err';
  const save = document.createElement('button'); save.type = 'submit'; save.textContent = 'Lưu';
  const cancel = document.createElement('button'); cancel.type = 'button'; cancel.className = 'link'; cancel.textContent = 'Hủy';
  cancel.onclick = () => loadReminders();
  f.onsubmit = async (ev) => {
    ev.preventDefault(); err.textContent = '';
    try {
      const r = await fetch('/api/nhac/' + x.id, { method: 'PUT', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ viec: viec.value, luc: luc.value, lap: lap.value }) });
      if (r.ok) { loadReminders(); return; }
      const d = await r.json().catch(() => ({}));
      err.textContent = typeof d.detail === 'string' ? d.detail : 'Không lưu được';
    } catch (e2) { err.textContent = 'Mất mạng, thử lại nha.'; }
  };
  const row = document.createElement('div'); row.className = 'row'; row.append(err, cancel, save);
  f.append(viec, luc, lap, row); li.appendChild(f); viec.focus();
}
const daysEl = document.getElementById('days');
async function loadDays() {
  daysEl.innerHTML = '';
  let list = [];
  try { const r = await fetch('/api/ngay-dac-biet'); if (r.ok) list = await r.json(); } catch (e) {}
  if (!list.length) { const li = document.createElement('li'); li.textContent = 'Chưa có. Thử kể: "sinh nhật mình 5/3".'; daysEl.appendChild(li); }
  list.forEach(x => {
    const li = document.createElement('li'), b = document.createElement('button');
    li.textContent = x.ngay + (x.am_lich ? ' (âm lịch)' : '') + ' — ' + x.viec + ' ';
    b.textContent = 'Xóa'; b.type = 'button'; b.className = 'link'; b.setAttribute('aria-label', 'Xóa ngày: ' + x.viec);
    b.onclick = async () => { await fetch('/api/ngay-dac-biet/' + x.id, { method: 'DELETE' }); loadDays(); };
    li.appendChild(b); daysEl.appendChild(li);
  });
}
document.getElementById('addFactForm').addEventListener('submit', async (ev) => {
  ev.preventDefault();
  const inp = document.getElementById('newFact'), text = inp.value.trim();
  if (!text) return;
  const r = await fetch('/api/facts', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ content: text }) });
  if (r.ok) inp.value = '';
  loadFacts();
});
document.getElementById('openMem').onclick = () => { loadFacts(); loadDays(); loadReminders(); mem.showModal(); };
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

// ---- Ngủ gật: 3 phút không ai đụng tới thì Bơ nhắm mắt; chạm/gõ/nói là tỉnh ----
var SLEEP_AFTER = 3 * 60 * 1000;
var idleTimer = null;
function scheduleSleep() {
  clearTimeout(idleTimer);
  idleTimer = setTimeout(() => { if (!send.disabled && !speaking) express('ngu'); }, SLEEP_AFTER);
}
function wake() {
  if (face.dataset.e === 'ngu') express('binh_thuong'); else scheduleSleep();
}
['pointerdown', 'keydown', 'focusin'].forEach(ev => document.addEventListener(ev, wake, { passive: true }));
scheduleSleep();

// Chạm vào mặt Bơ khi đang đọc to → Bơ im ngay
function stopSpeaking() {
  if (!speaking || !window.speechSynthesis) return false;
  speakSeq++; speechSynthesis.cancel();
  speaking = false; face.classList.remove('talking'); resumeListening();
  return true;
}
face.addEventListener('click', stopSpeaking);

// ---- Tìm trong chuyện cũ ----
const searchDlg = document.getElementById('search'), searchInput = document.getElementById('searchInput');
const searchList = document.getElementById('searchList');
function boKhongDau(s) {
  return s.toLowerCase().replace(/đ/g, 'd').normalize('NFD').replace(/[̀-ͯ]/g, '');
}
// Tô vàng chỗ khớp (so không dấu, nhưng vẫn hiện chữ gốc có dấu)
function highlight(li, text, q) {
  text = text.normalize('NFC');
  // bỏ dấu từng chữ một để vị trí khớp trên chữ gốc không bị lệch
  const plain = Array.from(text).map(ch => boKhongDau(ch).charAt(0) || ch).join('');
  const chars = Array.from(text), qq = boKhongDau(q).trim().replace(/\s+/g, ' ');
  const at = qq ? plain.replace(/\s/g, ' ').indexOf(qq) : -1;
  if (at < 0) { li.appendChild(document.createTextNode(text)); return; }
  const m = document.createElement('mark');
  m.textContent = chars.slice(at, at + qq.length).join('');
  li.append(chars.slice(0, at).join(''), m, chars.slice(at + qq.length).join(''));
}
let searchTimer = null, searchSeq = 0;
async function runSearch() {
  const q = searchInput.value, id = ++searchSeq;
  // chưa gõ gì → hiện các tin đã ghim
  const showPinned = boKhongDau(q).trim().length < 2;
  let list = [];
  try {
    const r = await fetch(showPinned ? '/api/ghim' : '/api/tim?q=' + encodeURIComponent(q));
    if (r.ok) list = await r.json();
  } catch (e) {}
  if (id !== searchSeq) return;  // đã gõ tiếp, bỏ kết quả cũ
  searchList.innerHTML = '';
  if (showPinned) {
    const li = document.createElement('li');
    li.textContent = list.length ? 'Tin đã ghim:' : 'Chưa ghim tin nào. Chạm vào một tin nhắn để ghim.';
    searchList.appendChild(li);
  } else if (!list.length) { const li = document.createElement('li'); li.textContent = 'Không thấy.'; searchList.appendChild(li); }
  list.forEach(m => {
    const li = document.createElement('li'), s = document.createElement('small');
    s.textContent = (m.role === 'user' ? 'Bạn' : 'Bơ') + ' · ' + timeLabel(m.created_at);
    li.appendChild(s); highlight(li, m.content, q); searchList.appendChild(li);
  });
}
searchInput.addEventListener('input', () => { clearTimeout(searchTimer); searchTimer = setTimeout(runSearch, 300); });
document.getElementById('openSearch').onclick = () => { searchDlg.showModal(); searchInput.focus(); runSearch(); };
document.getElementById('closeSearch').onclick = () => searchDlg.close();

// ---- Việc cần làm ----
const todoDlg = document.getElementById('todo'), todosEl = document.getElementById('todos');
const todoErr = document.getElementById('todoErr');
async function loadTodos() {
  let list = [];
  try { const r = await fetch('/api/viec'); if (r.ok) list = await r.json(); } catch (e) {}
  todosEl.innerHTML = '';
  if (!list.length) { const li = document.createElement('li'); li.textContent = 'Chưa có việc nào.'; todosEl.appendChild(li); }
  list.forEach(x => {
    const li = document.createElement('li'), lab = document.createElement('label');
    const cb = document.createElement('input'), span = document.createElement('span'), b = document.createElement('button');
    if (x.xong) li.className = 'xong';
    cb.type = 'checkbox'; cb.checked = x.xong;
    span.textContent = x.viec;
    cb.onchange = async () => {
      todoErr.hidden = true;
      try {
        const r = await fetch('/api/viec/' + x.id, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ xong: cb.checked }) });
        if (!r.ok) { try { todoErr.textContent = (await r.json()).detail; } catch (e2) { todoErr.textContent = 'Không đổi được'; } todoErr.hidden = false; }
      } catch (e) { todoErr.textContent = 'Mất mạng, thử lại nha.'; todoErr.hidden = false; }
      loadTodos();
    };
    b.textContent = 'Xóa'; b.type = 'button'; b.setAttribute('aria-label', 'Xóa việc: ' + x.viec);
    b.onclick = async () => {
      try { await fetch('/api/viec/' + x.id, { method: 'DELETE' }); } catch (e) { todoErr.textContent = 'Mất mạng, thử lại nha.'; todoErr.hidden = false; }
      loadTodos();
    };
    lab.append(cb, span); li.append(lab, b); todosEl.appendChild(li);
  });
}
document.getElementById('openTodo').onclick = () => { todoErr.hidden = true; todoDlg.showModal(); loadTodos(); };
document.getElementById('closeTodo').onclick = () => todoDlg.close();
document.getElementById('addTodoForm').addEventListener('submit', async (ev) => {
  ev.preventDefault();
  const inp = document.getElementById('newTodo'), text = inp.value.trim();
  if (!text) return;
  todoErr.hidden = true;
  try {
    const r = await fetch('/api/viec', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ viec: text }) });
    if (r.ok) inp.value = '';
    else { try { todoErr.textContent = (await r.json()).detail; } catch (x) { todoErr.textContent = 'Không thêm được'; } todoErr.hidden = false; }
  } catch (e) { todoErr.textContent = 'Mất mạng, thử lại nha.'; todoErr.hidden = false; }
  loadTodos();
});

// ---- Bơ làm được gì? ----
const helpDlg = document.getElementById('help');
const statsEl = document.getElementById('stats');
document.getElementById('openHelp').onclick = async () => {
  helpDlg.showModal(); statsEl.textContent = '';
  try {
    const s = await (await fetch('/api/thong-ke')).json();
    statsEl.textContent = s.quen_tu
      ? 'Bơ và bạn quen nhau ' + s.so_ngay_quen + ' ngày (từ ' + s.quen_tu + '), trò chuyện ' + s.so_ngay_tro_chuyen
        + ' ngày, ' + s.so_tin.toLocaleString('vi-VN') + ' tin nhắn. Bơ đang nhớ ' + s.so_dieu_nho + ' điều về bạn.'
      : 'Bơ và bạn mới quen thôi. Nhắn gì đó đi!';
  } catch (e) {}
  showMoods();
  loadSettings();
  const hl = document.getElementById('healthList'); hl.innerHTML = '';
  try {
    const d = await (await fetch('/api/suc-khoe')).json();
    d.kiem_tra.forEach(k => {
      const li = document.createElement('li');
      li.textContent = (k.muc === 'ok' ? '✓ ' : k.muc === 'canh_bao' ? '! ' : '✗ ') + k.ten + ': ' + k.ghi_chu;
      hl.appendChild(li);
    });
  } catch (e) {}
};
// ---- Cài đặt (thành phố, giờ yên lặng, tổng kết tuần): lưu trên máy chủ, ưu tiên hơn .env ----
const settingsMsg = document.getElementById('settingsMsg');
function fillSettings(d) {
  if (!d || !d.hien_tai) return;
  document.getElementById('setCity').value = d.hien_tai.thanh_pho || '';
  document.getElementById('setQuiet').value = d.hien_tai.gio_yen_lang || '';
  document.getElementById('setRecap').checked = !!d.hien_tai.tong_ket_tuan;
  document.getElementById('setHoliday').checked = !!d.hien_tai.chuc_le;
  quietRange = d.hien_tai.gio_yen_lang || '';  // áp dụng ngay cho giọng đọc
}
function settingsNote(text) { settingsMsg.textContent = text; settingsMsg.hidden = !text; }
async function loadSettings() {
  settingsNote('');
  try { const r = await fetch('/api/cai-dat'); if (r.ok) fillSettings(await r.json()); } catch (e) {}
}
async function sendSettings(method, body) {
  try {
    const r = await fetch('/api/cai-dat', { method, headers: { 'Content-Type': 'application/json' }, body: body && JSON.stringify(body) });
    const d = await r.json().catch(() => ({}));
    if (!r.ok) { settingsNote(typeof d.detail === 'string' ? d.detail : 'Không lưu được'); return; }
    fillSettings(d); settingsNote(method === 'DELETE' ? 'Đã về như file .env.' : 'Đã lưu, áp dụng ngay.');
  } catch (e) { settingsNote('Mất mạng, thử lại nha.'); }
}
document.getElementById('settingsForm').addEventListener('submit', (ev) => {
  ev.preventDefault();
  sendSettings('PUT', {
    thanh_pho: document.getElementById('setCity').value,
    gio_yen_lang: document.getElementById('setQuiet').value,
    tong_ket_tuan: document.getElementById('setRecap').checked,
    chuc_le: document.getElementById('setHoliday').checked,
  });
});
document.getElementById('resetSettings').onclick = () => {
  if (confirm('Bỏ cài đặt đã chỉnh trên web, dùng lại giá trị trong file .env?')) sendSettings('DELETE');
};

// Tâm trạng 7 ngày: mỗi ngày một biểu tượng (Bơ đoán từ tin nhắn). Chưa có ngày nào thì ẩn.
const MOOD_ICON = { vui: '😊', binh_thuong: '🙂', buon: '😢', met: '😩', lo: '😟', gian: '😠' };
const MOOD_NAME = { vui: 'vui', binh_thuong: 'bình thường', buon: 'buồn', met: 'mệt', lo: 'lo lắng', gian: 'bực bội' };
const THU_NGAN = ['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'];
async function showMoods() {
  const box = document.getElementById('moods');
  box.hidden = true; box.innerHTML = '';
  try {
    const days = await (await fetch('/api/tam-trang')).json();
    if (!Array.isArray(days) || !days.some(d => d.tam_trang)) return;
    const title = document.createElement('span'); title.className = 'title';
    title.textContent = 'Tâm trạng của bạn 7 ngày qua (Bơ đoán):';
    box.appendChild(title);
    days.forEach(d => {
      const el = document.createElement('span'); el.className = 'day';
      const [y, m, dd] = d.ngay.split('-').map(Number);
      const thu = THU_NGAN[new Date(y, m - 1, dd).getDay()];
      const icon = document.createElement('b');
      icon.textContent = MOOD_ICON[d.tam_trang] || '·';
      const label = d.tam_trang ? (MOOD_NAME[d.tam_trang] || d.tam_trang) : 'không nói chuyện';
      el.title = thu + ' ' + dd + '/' + m + ': ' + label;
      el.setAttribute('aria-label', el.title);
      el.appendChild(icon); el.appendChild(document.createTextNode(thu));
      box.appendChild(el);
    });
    box.hidden = false;
  } catch (e) {}
}
document.getElementById('closeHelp').onclick = () => helpDlg.close();

// ---- Ghim tin nhắn: chạm vào bong bóng → hiện nút "Ghim" / "Bỏ ghim" ----
log.addEventListener('click', (ev) => {
  if (ev.target.closest('button')) return;
  const bubble = ev.target.closest('.msg[data-id]');
  if (!bubble) return;
  const old = log.querySelector('.pin-btn');
  if (old) { const same = old.parentElement === bubble; old.remove(); if (same) return; }
  const id = bubble.dataset.id, pinned = bubble.classList.contains('pinned');
  const b = document.createElement('button');
  b.type = 'button'; b.className = 'snooze pin-btn'; b.textContent = pinned ? 'Bỏ ghim' : 'Ghim tin này';
  b.onclick = async () => {
    b.disabled = true;
    try {
      const r = await fetch('/api/ghim/' + id, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ghim: !pinned }) });
      if (!r.ok) throw new Error();
      log.querySelectorAll('.msg[data-id="' + id + '"]').forEach(m => m.classList.toggle('pinned', !pinned));
      b.remove();
    } catch (e) { b.disabled = false; b.textContent = 'Lỗi, bấm lại'; }
  };
  bubble.appendChild(b);
});

// ---- Sửa tính cách Bơ ----
const personaDlg = document.getElementById('persona'), personaText = document.getElementById('personaText');
const personaNote = document.getElementById('personaNote');
const PERSONA_HINT = personaNote.textContent;
async function loadPersona() {
  personaText.value = 'Đang tải...'; personaText.disabled = true;
  try {
    const d = await (await fetch('/api/tinh-cach')).json();
    personaText.value = d.noi_dung;
    personaNote.textContent = PERSONA_HINT + (d.tu_sua ? ' (Đang dùng bản bạn tự sửa.)' : ' (Đang dùng bản mặc định.)');
  } catch (e) { personaText.value = ''; personaNote.textContent = 'Không tải được.'; }
  personaText.disabled = false;
}
document.getElementById('openPersona').onclick = () => { personaDlg.showModal(); loadPersona(); };
document.getElementById('closePersona').onclick = () => personaDlg.close();
document.getElementById('savePersona').onclick = async () => {
  try {
    const r = await fetch('/api/tinh-cach', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ noi_dung: personaText.value }) });
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || 'Lỗi');
    personaDlg.close(); statusEl.textContent = 'Đã lưu tính cách mới';
    setTimeout(() => { if (statusEl.textContent === 'Đã lưu tính cách mới') statusEl.textContent = ''; }, 3000);
  } catch (e) { alert('Không lưu được: ' + e.message); }
};
document.getElementById('resetPersona').onclick = async () => {
  if (!confirm('Bỏ bản tự sửa, dùng lại tính cách mặc định?')) return;
  await fetch('/api/tinh-cach', { method: 'DELETE' }); loadPersona();
};

// ---- Màu mặt Bơ (lưu trên máy này) ----
const FACE_COLORS = [['', 'Vàng (mặc định)'], ['#a8d672', 'Xanh bơ'], ['#ffb3c1', 'Hồng'], ['#9fd3ff', 'Xanh dương'],
  ['#ffb26b', 'Cam'], ['#d3b8ff', 'Tím']];
function applyFaceColor(c) {
  if (c) document.documentElement.style.setProperty('--face', c);
  else document.documentElement.style.removeProperty('--face');
}
let faceColor = '';
try { faceColor = localStorage.getItem('bo_mau') || ''; } catch (e) {}
if (!FACE_COLORS.some(x => x[0] === faceColor)) faceColor = '';
applyFaceColor(faceColor);
const colorsEl = document.getElementById('colors');
function renderColors() {
  colorsEl.innerHTML = '';
  FACE_COLORS.forEach(([c, name]) => {
    const b = document.createElement('button');
    b.type = 'button'; b.setAttribute('role', 'radio'); b.setAttribute('aria-checked', c === faceColor);
    b.setAttribute('aria-label', name); b.title = name;
    b.style.background = c || '#ffd36e';
    b.onclick = () => {
      faceColor = c; applyFaceColor(c); renderColors();
      try { localStorage.setItem('bo_mau', c); } catch (e) {}
    };
    colorsEl.appendChild(b);
  });
}
renderColors();

// ---- Phím tắt: Esc = Bơ ngừng đọc (hộp đang mở thì trình duyệt tự đóng), Ctrl/Cmd+K = tìm ----
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !document.querySelector('dialog[open]')) { if (stopSpeaking()) e.preventDefault(); return; }
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
    if (e.isComposing || document.querySelector('dialog[open]:not(#search)')) return;  // đang gõ dấu / hộp khác đang mở
    e.preventDefault();
    if (!searchDlg.open) document.getElementById('openSearch').click();
  }
});

// Tải xong hết các file JS mới cho gửi tin (nút Gửi tắt sẵn trong HTML)
send.disabled = false;

// ---- Bản nháp: chữ đang gõ dở được giữ lại khi tải lại trang (lưu trên máy này) ----
try { const d = localStorage.getItem('bo_nhap'); if (d && !input.value) input.value = d; } catch (e) {}
let draftTimer = null;
function saveDraft() {
  clearTimeout(draftTimer);
  draftTimer = setTimeout(() => { try { localStorage.setItem('bo_nhap', input.value); } catch (e) {} }, 300);
}
input.addEventListener('input', saveDraft);
form.addEventListener('submit', () => { clearTimeout(draftTimer); try { localStorage.removeItem('bo_nhap'); } catch (e) {} });
