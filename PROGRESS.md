# Nhật ký tiến độ

## Cách dừng / góp ý (dành cho Tân)
- **Dừng tự chạy:** tạo file tên `STOP` ở thư mục gốc repo (trên github.com: Add file → Create new file → gõ `STOP` → Commit). Xóa file đó để chạy lại. Hoặc nhắn Claude "dừng".
- **Góp ý:** ghi vào file `FEEDBACK.md`, phiên sau Claude sẽ xử lý trước.
- **Lấy bản mới về máy:** `git pull` trong thư mục dự án rồi chạy lại `run.bat`.

## Cần Tân quyết định
- (chưa có)

## 2026-10-11 – Giai đoạn 1 xong
- Dựng toàn bộ khung: bộ não (Claude Haiku), trí nhớ SQLite, web chat có khuôn mặt biểu cảm.
- 13 test tự động qua hết (dùng bộ não giả).
- Chưa test với API thật (máy làm việc của Claude không gọi được API ra ngoài) → Tân chạy thử trên máy.
- Tân chọn chế độ "làm liền, báo sau": Claude tự chạy mỗi giờ, làm tiếp giai đoạn 2 mà không chờ duyệt.

- Tân chốt tên **Bơ**, tính cách vui tính, năng động → đã viết lại persona.md.

## 2026-10-10 – Giai đoạn 2 xong
- **Bộ câu hỏi thử tính cách:** 10 tình huống trong `tinh_huong.json` (chào, nhớ tên, buồn, khoe, mệt, chuyện nghiêm trọng, hỏi điều không biết...). Chạy `python -m app.thu_tinh_cach` → in câu trả lời của Bơ + điểm từng câu + tổng điểm. Tốn ~10 câu API, dùng trí nhớ tạm nên không làm bẩn dữ liệu thật.
- **Xem/xóa trí nhớ:** dưới khuôn mặt có nút "Bơ nhớ gì về mình?" → hiện danh sách, bấm "Xóa" từng dòng hoặc "Xóa hết".
- 20 test tự động qua hết.

**Tân cần thử:** `git pull`, chạy thử bộ chấm điểm với API key thật và gửi tổng điểm/câu trả lời lạ vào FEEDBACK.md; mở web bấm nút xem trí nhớ.

**Tiếp theo:** Giai đoạn 3, việc "Tóm tắt các cuộc trò chuyện cũ".
