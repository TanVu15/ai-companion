// Chi phí, lời chào khi mở web, lời nhắc theo giờ, kiểm tra sức khỏe, rồi khởi động trang.
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
    if (r.ok && data.noi) { express(data.cam_xuc, data.hanh_dong); speak(data.noi); await addBo(data.noi, data.id); }
  } catch (e) {}
}
// ---- Lời nhắc: hỏi máy chủ mỗi 30 giây (chỉ khi web đang mở) ----
async function pollReminders() {
  try {
    const r = await fetch('/api/nhac');
    if (!r.ok) return;
    for (const x of await r.json()) {
      await addBo(x.noi, x.id); express(x.cam_xuc, x.hanh_dong); speak(x.noi);
      if (x.viec) addSnooze(x.viec);
      if (window.Notification && Notification.permission === 'granted' && document.hidden) new Notification('Bơ', { body: x.noi, icon: '/web/icon-180.png' });
    }
  } catch (e) {}
}
setInterval(pollReminders, 30000);
// Trang để mở lâu (qua nửa đêm, qua 17h Chủ nhật): mỗi 10 phút hỏi xem có dịp gì để Bơ mở lời không
// (chỉ sinh nhật/kỷ niệm, tổng kết tuần — không có dịp thì không tốn câu API nào)
setInterval(async () => {
  if (send.disabled || speaking || document.hidden) return;  // tab ẩn thì để dành, mở lại mới chúc
  try {
    const r = await fetch('/api/chao?chi_dip=1', { method: 'POST' });
    const data = await r.json();
    if (r.ok && data.noi) { express(data.cam_xuc, data.hanh_dong); speak(data.noi); await addBo(data.noi, data.id); }
  } catch (e) {}
}, 10 * 60 * 1000);
// Nút "Nhắc lại sau 10 phút" ngay dưới lời nhắc vừa tới
function addSnooze(viec) {
  const bubble = log.lastElementChild;
  if (!bubble) return;
  const b = document.createElement('button');
  b.type = 'button'; b.className = 'retry snooze'; b.textContent = 'Nhắc lại sau 10 phút';
  b.onclick = async () => {
    b.disabled = true;
    try {
      const r = await fetch('/api/nhac/hoan', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ viec, phut: 10 }) });
      if (!r.ok) throw new Error();
      b.replaceWith(Object.assign(document.createElement('span'), { className: 'time', textContent: 'Ok, 10 phút nữa Bơ nhắc lại' }));
    } catch (e) { b.disabled = false; b.textContent = 'Lỗi, bấm lại'; }
  };
  bubble.appendChild(b);
}
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
