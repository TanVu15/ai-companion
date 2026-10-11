// Giọng nói: Bơ đọc to, micro, rảnh tay, chọn giọng. Chạy sau app.js (dùng biến chung của app.js).
// ---- Giọng nói: giọng AI miễn phí (edge-tts qua máy chủ), dự phòng bằng giọng có sẵn của trình duyệt ----
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
  voiceOn = !voiceOn; showVoice(); showPick();
  try { localStorage.setItem('bo_voice', voiceOn ? '1' : '0'); } catch (e) {}
  if (!voiceOn) boNgungDoc();
};
let voiceName = '';
try { voiceName = localStorage.getItem('bo_giong') || ''; } catch (e) {}
const pickBtn = document.getElementById('pickVoiceBtn');
function allVoices() { return window.speechSynthesis ? speechSynthesis.getVoices() : []; }
function viVoice() { return boChonGiong(allVoices(), voiceName); }
// Chỉ hiện nút "Giọng" khi bật giọng nói và máy có từ 2 giọng tiếng Việt trở lên
function showPick() {
  const n = boGiongViet(allVoices()).length, v = viVoice();
  pickBtn.hidden = !voiceOn || n < 2;
  if (v) pickBtn.textContent = 'Giọng: ' + v.name.replace(/^Microsoft |^Google /, '').slice(0, 24);
}
if (window.speechSynthesis) speechSynthesis.addEventListener && speechSynthesis.addEventListener('voiceschanged', showPick);
pickBtn.onclick = () => {
  const v = boGiongKe(allVoices(), (viVoice() || {}).name);
  if (!v) return;
  voiceName = v.name; showPick();
  try { localStorage.setItem('bo_giong', voiceName); } catch (e) {}
  speak('Bơ nói giọng này nha');
};
showPick();
let speakSeq = 0;
let quietRange = '';  // lấy từ /api/suc-khoe lúc mở trang
// Bơ tự nói (lời nhắc, lời chào): đêm khuya trong giờ yên lặng thì chỉ hiện chữ, không đọc to
function speakAuto(text) {
  if (boGioYenLang(new Date().getHours(), quietRange)) return;
  speak(text);
}
// Đọc to: ưu tiên giọng AI miễn phí (edge-tts, máy chủ trả mp3); lỗi/không mạng → giọng của trình duyệt.
let aiLoiDen = 0, daBaoLoi = false, amThanh = null;
function speak(text) {
  text = boChuDeDoc(text);
  if (!voiceOn || !text) return;
  const id = ++speakSeq;  // chỉ lần đọc mới nhất được báo "đọc xong"
  if (handsFree) pauseListening();  // đừng để micro nghe giọng của chính Bơ
  dungAmThanh();
  if (window.speechSynthesis) speechSynthesis.cancel();
  speaking = true;
  if (Date.now() < aiLoiDen) { speakTrinhDuyet(text, id); return; }
  docAI(boTachCauDoc(text), id).catch(e => {
    if (id !== speakSeq) return;
    if (e && e.name === 'NotAllowedError') { xongDoc(id); return; }  // máy chặn tự phát tiếng khi chưa chạm trang: không phải lỗi giọng AI
    aiLoiDen = Date.now() + 5 * 60 * 1000;  // 5 phút sau mới thử lại giọng AI
    if (!daBaoLoi) { daBaoLoi = true; baoNho('Giọng AI chưa dùng được (cần mạng), Bơ tạm dùng giọng của trình duyệt.'); }
    speakTrinhDuyet(e && e.conLai ? e.conLai : text, id);
  });
}
function baoNho(msg) {
  if (statusEl.textContent) return;
  statusEl.textContent = msg;
  setTimeout(() => { if (statusEl.textContent === msg) statusEl.textContent = ''; }, 6000);
}
function layGiong(t) {
  return fetch('/api/giong', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: t }) })
    .then(r => { if (!r.ok) throw new Error('giong ' + r.status); return r.blob(); });
}
// Đọc lần lượt từng đoạn; trong lúc đọc đoạn này thì tải sẵn đoạn sau. Lỗi giữa chừng → báo phần còn lại cho giọng trình duyệt
async function docAI(doan, id) {
  let tiep = layGiong(doan[0]);
  for (let i = 0; i < doan.length; i++) {
    let blob;
    try { blob = await tiep; } catch (e) { e.conLai = doan.slice(i).join(' '); throw e; }
    if (id !== speakSeq) return;
    if (i + 1 < doan.length) { tiep = layGiong(doan[i + 1]); tiep.catch(() => {}); }
    try { await phat(blob, id); } catch (e) { e.conLai = doan.slice(i).join(' '); throw e; }
    if (id !== speakSeq) return;
  }
  xongDoc(id);
}
function phat(blob, id) {
  return new Promise((ok, loi) => {
    const url = URL.createObjectURL(blob), a = new Audio(url);
    let xong = false;
    const ket = (err) => {
      if (xong) return; xong = true;
      URL.revokeObjectURL(url); if (amThanh === a) amThanh = null; ngungMieng();
      err ? loi(err) : ok();
    };
    a.playbackRate = RATES[rateIdx][1];
    a.onended = () => ket();
    a.onerror = () => ket(new Error('không phát được'));
    a._dung = () => { a.pause(); ket(); };
    amThanh = a;
    a.play().then(() => {
      if (id !== speakSeq) { a._dung(); return; }
      face.classList.add('talking'); theoMieng(a);
      // phòng khi trình duyệt quên báo "phát xong"
      const giay = isFinite(a.duration) ? a.duration / a.playbackRate : 20;
      setTimeout(() => ket(), (giay + 3) * 1000);
    }).catch(ket);
  });
}
function dungAmThanh() { if (amThanh) amThanh._dung(); }
function xongDoc(id) {
  if (id !== speakSeq) return;
  speaking = false; face.classList.remove('talking'); resumeListening();
}
// Dừng đọc ngay (chạm vào mèo, Esc, bấm micro). Trả về true nếu đang đọc
function boNgungDoc() {
  if (!speaking) return false;
  speakSeq++; dungAmThanh();
  if (window.speechSynthesis) speechSynthesis.cancel();
  speaking = false; face.classList.remove('talking'); resumeListening();
  return true;
}
// Miệng mèo mấp máy theo âm lượng thật của file đang phát (Web Audio). Máy chưa cho dùng Web Audio thì dùng
// chuyển động có sẵn trong CSS. Chỉ nối Web Audio khi nó đang chạy, kẻo âm thanh bị nuốt mất.
let acMieng = null, doAm = null, vongMieng = 0;
function theoMieng(a) {
  try {
    acMieng = acMieng || new (window.AudioContext || window.webkitAudioContext)();
    if (acMieng.state !== 'running') { acMieng.resume(); return; }
    if (!doAm) { doAm = acMieng.createAnalyser(); doAm.fftSize = 512; doAm.connect(acMieng.destination); }
    acMieng.createMediaElementSource(a).connect(doAm);
  } catch (e) { return; }
  face.classList.add('noi-that');
  const buf = new Uint8Array(doAm.fftSize);
  const ve = () => {
    doAm.getByteTimeDomainData(buf);
    let tong = 0;
    for (const v of buf) tong += (v - 128) * (v - 128);
    const to = Math.min(1.2, Math.sqrt(tong / buf.length) / 22);
    face.style.setProperty('--mo', (0.15 + to).toFixed(2));
    vongMieng = requestAnimationFrame(ve);
  };
  cancelAnimationFrame(vongMieng); ve();
}
function ngungMieng() {
  cancelAnimationFrame(vongMieng); face.classList.remove('noi-that'); face.style.removeProperty('--mo');
}
// Giọng có sẵn của trình duyệt (dự phòng)
function speakTrinhDuyet(text, id) {
  if (!window.speechSynthesis) { xongDoc(id); return; }
  showPick();  // Safari cũ không báo "voiceschanged": cập nhật nút chọn giọng mỗi lần đọc
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'vi-VN'; u.rate = RATES[rateIdx][1]; const v = viVoice(); if (v) u.voice = v;
  u.onstart = () => face.classList.add('talking');
  u.onend = u.onerror = () => xongDoc(id);  // lần đọc cũ bị ngắt thì xongDoc tự bỏ qua
  speaking = true; speechSynthesis.speak(u);
  // Phòng khi trình duyệt quên báo "đọc xong" → rảnh tay không bị kẹt
  setTimeout(() => { if (speaking) xongDoc(id); }, 3000 + text.length * 150);
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
    boNgungDoc();
    input.value = ''; micSession = true; micBtn.classList.add('on'); statusEl.textContent = 'Bơ đang nghe...';
    startRec();
  };
  handsBtn.onclick = () => {
    handsFree = !handsFree; paused = false; awaitUntil = 0; micSession = false; showHands();
    micBtn.disabled = handsFree;
    if (listening) rec.abort(); else if (handsFree) startRec();
  };
}
