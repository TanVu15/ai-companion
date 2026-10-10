// Giọng nói: Bơ đọc to, micro, rảnh tay, chọn giọng. Chạy sau app.js (dùng biến chung của app.js).
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
  voiceOn = !voiceOn; showVoice(); showPick();
  try { localStorage.setItem('bo_voice', voiceOn ? '1' : '0'); } catch (e) {}
  if (!voiceOn && window.speechSynthesis) { speechSynthesis.cancel(); speaking = false; face.classList.remove('talking'); }
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
