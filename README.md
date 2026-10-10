# Bơ – người bạn AI

Chatbot trò chuyện có tính cách, có trí nhớ và có khuôn mặt biểu cảm. Đây là phần "bộ não"; sau này sẽ gắn vào phần cứng (micro, loa, màn hình, động cơ).

## Chạy trên Windows

1. Cài [Python 3.11+](https://www.python.org/downloads/) (nhớ tick "Add Python to PATH").
2. Tải code về: `git clone https://github.com/TanVu15/ai-companion.git`
3. Nhấp đúp `run.bat`. Lần đầu nó tự cài thư viện và tạo file `.env`.
4. Mở file `.env`, dán API key vào dòng `ANTHROPIC_API_KEY=`, rồi chạy lại `run.bat`.
5. Mở trình duyệt: http://localhost:8000

**Chưa có API key?** Đặt `DEMO=1` trong `.env` để xem giao diện trước. Bot sẽ chỉ nhắc lại lời bạn và đổi biểu cảm liên tục.

**Dùng trên iPhone:** điện thoại và máy tính phải chung wifi. Gõ `ipconfig` trên máy tính để xem địa chỉ IPv4 (ví dụ 192.168.1.5), rồi trên iPhone mở `http://192.168.1.5:8000`. Nếu không vào được, cho phép Python qua Windows Firewall.

**Đưa Bơ ra màn hình chính iPhone:** mở trang Bơ bằng Safari → nút Chia sẻ (ô vuông có mũi tên) → "Thêm vào MH chính". Bơ có biểu tượng riêng và mở toàn màn hình như một ứng dụng.

**Dùng khi ra ngoài (không chung wifi):** xem [DUA_LEN_MANG.md](DUA_LEN_MANG.md). Nhớ đặt `APP_PASSWORD` trong `.env` trước.

**Gặp lỗi?** Xem [SU_CO.md](SU_CO.md).

## Nói chuyện bằng giọng

- **Bơ đọc to câu trả lời:** bấm "Giọng nói: tắt" dưới khuôn mặt để bật. Dùng giọng có sẵn của máy (iPhone và Windows thường có giọng tiếng Việt; không có thì máy đọc giọng khác).
- **Bắt Bơ im:** chạm vào khuôn mặt khi Bơ đang đọc.
- **Nói thay vì gõ:** bấm nút micro cạnh nút Gửi, nói xong ngừng một chút là tự gửi. Chạy tốt nhất trên Chrome, Edge, Safari.
- **Rảnh tay:** bấm "Rảnh tay: tắt" để bật. Bơ nghe liên tục nhưng chỉ trả lời khi được gọi: "Bơ ơi, hôm nay trời đẹp ghê" hoặc gọi "Bơ ơi" trước rồi nói trong 8 giây. Lúc Bơ đang nói thì tạm ngừng nghe.
- Nút micro chỉ hiện khi mở bằng `http://localhost:8000` hoặc link `https://...` (trình duyệt chặn micro trên địa chỉ `http://192.168...`). Trên iPhone muốn dùng micro thì dùng link https ở [DUA_LEN_MANG.md](DUA_LEN_MANG.md) (Cách 2), hoặc dùng nút micro trên bàn phím iPhone để đọc chính tả.

## Nhờ Bơ nhắc việc

Nhắn kiểu "8h tối nhắc mình gọi mẹ" hoặc "30 phút nữa nhắc mình tắt bếp". Tới giờ Bơ nhắn (và đọc to nếu bật giọng nói).
Nhắc lặp lại cũng được: "mỗi ngày 7h sáng nhắc mình uống nước", "tối thứ Hai hằng tuần 8h nhắc mình họp nhóm".
Dưới lời nhắc có nút "Nhắc lại sau 10 phút".
Chỉ nhắc được khi **máy tính đang chạy Bơ và trang web đang mở**. Xem/xóa lời nhắc trong "Bơ nhớ gì về mình?".

## Những thứ khác Bơ làm được

- **Nút "?"**: danh sách mẹo dùng + Bơ và bạn đã quen bao nhiêu ngày.
- **Hỏi thăm chuyện cũ:** kể "tối nay đi đá bóng" → hôm sau mở web Bơ tự hỏi. 2 ngày không chat thì Bơ chào "lâu quá không gặp".
- **Ngày đặc biệt:** kể "sinh nhật mình 5/3" → đúng ngày Bơ chúc (mỗi năm một lần).
- **Tổng kết tuần:** tối Chủ nhật (từ 17h) mở web, Bơ điểm lại tuần qua. Tắt bằng `WEEKLY_RECAP=0`.
- **Tìm chuyện cũ:** nút "Tìm", gõ không dấu cũng được.
- **Ghim tin nhắn:** chạm vào một tin → "Ghim tin này". Xem lại ở nút "Tìm" (khi chưa gõ gì).
- **Sao lưu:** trong "Bơ nhớ gì về mình?" → tải bản sao lưu (.json, nạp lại được) hoặc tải trò chuyện (.txt, để đọc).
- **Chi phí:** nút "Chi phí". Đặt `MONTHLY_USD_LIMIT` trong `.env` để giới hạn tiền mỗi tháng.

## Nối phần cứng (ESP32)

Xem [THIET_BI.md](THIET_BI.md): đặt `DEVICE_KEY` trong `.env`, thiết bị gửi chữ tới `/api/thiet-bi/chat` và nhận JSON cảm xúc/hành động.

## Đổi tính cách

Bấm nút **"Tính cách"** trên web, sửa rồi bấm "Lưu" — áp dụng từ tin nhắn sau. Bản bạn sửa lưu riêng ở `data/persona.md` (git pull không đè, bản trước giữ ở `data/persona.md.truoc`). Bấm "Về mặc định" để dùng lại `persona.md` gốc của dự án.

## Thử tính cách (chấm điểm)

Bơ trả lời 15 tình huống trong `tinh_huong.json` (buồn, mệt, khoe thành tích, hỏi điều không biết, hỏi thăm chuyện cũ, sinh nhật, nhắc mỗi ngày...) và được chấm điểm tự động. Tốn khoảng 15 câu API (rất rẻ), không đụng vào trí nhớ thật.

```
.venv\Scripts\activate
python -m app.thu_tinh_cach
```

Muốn thêm tình huống thì sửa `tinh_huong.json`.

## Cấu trúc

```
app/brain.py    Bộ não: ghép tính cách + trí nhớ + lịch sử, hỏi Claude, đọc JSON
app/memory.py   Trí nhớ: SQLite lưu tin nhắn và điều đáng nhớ (data/companion.db)
app/main.py     Máy chủ web (FastAPI)
web/index.html  Giao diện chat + khuôn mặt (HTML + CSS)
web/app.js      Phần chạy của giao diện: gửi tin, giọng nói, trí nhớ, chi phí, lời nhắc
web/danh_thuc.js, web/doc_to.js   Từ đánh thức "Bơ ơi", dọn chữ trước khi đọc to
persona.md      Tính cách
app/thu_tinh_cach.py + tinh_huong.json   Bộ câu hỏi thử tính cách
tests/          Test bằng bộ não giả, không tốn tiền API
```

Mỗi câu trả lời của bộ não có dạng:

```json
{ "noi": "...", "cam_xuc": "vui", "hanh_dong": "gat_dau", "ghi_nho": ["..."] }
```

`cam_xuc` và `hanh_dong` hiện điều khiển khuôn mặt trên web; sau này sẽ điều khiển phần cứng.

## Chạy test

```
pip install -r requirements.txt
python -m pytest -q
```
