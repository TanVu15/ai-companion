# Danh sách việc

## Giai đoạn 1 – Khung + trò chuyện + trí nhớ cơ bản
- [x] Cấu trúc dự án, cấu hình .env, run.bat
- [x] Bộ não gọi Claude, trả JSON (lời nói, cảm xúc, hành động, ghi nhớ)
- [x] Trí nhớ SQLite: lịch sử chat + điều đáng nhớ
- [x] Giao diện web chat + khuôn mặt biểu cảm (7 cảm xúc, 5 hành động)
- [x] Chế độ DEMO không cần API key
- [x] Giới hạn chi phí (lịch sử 20 tin, 300 câu/ngày)
- [x] Test tự động (13 test)
- Chờ Tân chạy thử trên máy (không chặn việc khác)

## Giai đoạn 2 – Tính cách
- [x] persona.md: Bơ, vui tính, năng động (Tân chốt 2026-10-11)
- [x] Bộ câu hỏi thử tính cách (10 tình huống) để chấm điểm "giống người"
- [x] Trang cài đặt nhỏ: xem/xóa những điều Bơ đã nhớ
- Chờ Tân nghiệm thu: chạy `python -m app.thu_tinh_cach`, bấm "Bơ nhớ gì về mình?" (không chặn việc khác)

## Giai đoạn 3 – Trí nhớ dài hạn
- [x] Tóm tắt các cuộc trò chuyện cũ thay vì chỉ giữ 20 tin gần nhất
- [ ] Gộp/sửa điều đáng nhớ bị trùng hoặc lỗi thời
- [ ] Bơ chủ động hỏi thăm chuyện cũ (ví dụ: "hôm qua tập chân sao rồi?")

## Giai đoạn 4 – Hoàn thiện
- [ ] Xử lý lỗi mạng, thử lại
- [ ] Hướng dẫn đưa lên mạng để dùng ngoài nhà
- [ ] Dùng thử 1 tuần, sửa theo góp ý

## Sau này
- Giọng nói (nghe + nói), từ khóa đánh thức
- Phần cứng ESP32: micro, loa, màn hình mặt, servo
