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

## 2026-10-10 – Giai đoạn 3: tóm tắt chuyện cũ
- Cứ khi có thêm 20 tin nhắn cũ (ngoài 20 tin gần nhất), Bơ gom lại thành 1 đoạn tóm tắt ≤150 chữ, gộp với bản tóm tắt trước. Đoạn này được gửi kèm mỗi lần hỏi → Bơ nhớ chuyện xa hơn mà chi phí gần như không tăng (thêm 1 câu API mỗi 20 tin).
- Nếu tóm tắt bị lỗi (mạng...) thì bỏ qua, lần sau thử lại; câu trả lời của Bơ không bị ảnh hưởng.
- 22 test qua hết.

## 2026-10-10 – Giai đoạn 3: dọn điều đáng nhớ
- **Không ghi trùng:** "Thích tập gym" và "thích  tập gym." được coi là một (bỏ qua hoa/thường, khoảng trắng, dấu câu cuối).
- **Tự quên điều lỗi thời:** câu trả lời JSON của bộ não có thêm mục nội bộ `quen`. Ví dụ Tân kể "mới chuyển ra Đà Nẵng" → Bơ xóa "Sống ở Huế", ghi "Sống ở Đà Nẵng". Giao diện không bị ảnh hưởng (vẫn chỉ đọc noi/cam_xuc/hanh_dong).
- **Gộp định kỳ:** khi danh sách dài tới 30 điều (đổi bằng `FACTS_MERGE_AT` trong .env), Bơ nhờ AI gộp các điều trùng ý, giữ điều mới hơn khi mâu thuẫn. Tốn 1 câu API mỗi lần, và chỉ thử lại sau khi có thêm 10 điều mới. Kết quả lạ (rỗng, dài hơn) thì bỏ, giữ nguyên danh sách cũ.
- 27 test qua hết.

**Tân cần thử:** kể cho Bơ một chuyện rồi "đổi ý" (ví dụ "mình hết thích cà phê rồi"), bấm "Bơ nhớ gì về mình?" xem điều cũ đã biến mất chưa.


## 2026-10-10 – Giai đoạn 3 xong: Bơ chủ động hỏi thăm
- Khi Tân kể việc sắp làm ("chiều nay tập chân", "mai đi phỏng vấn"), Bơ ghi vào danh sách "chuyện nên hỏi thăm" (mục nội bộ `hoi_tham` trong JSON, giao diện không thấy).
- Sau ít nhất 3 giờ (`FOLLOWUP_MIN_HOURS`), chuyện đó được gửi kèm cho Bơ, ghi rõ "kể hôm qua / 2 ngày trước". Bơ hỏi tự nhiên một chuyện rồi đánh dấu đã hỏi (`da_hoi`). Quá 7 ngày thì bỏ.
- **Mở web sau ≥3 giờ không nói chuyện** (`GREET_AFTER_HOURS`) và có chuyện để hỏi → Bơ tự mở lời trước. Không có gì để hỏi thì im, không tốn câu API nào.
- Bơ giờ cũng biết ngày giờ hiện tại (để hiểu "hôm qua", "tối nay").
- 35 test qua hết.

**Tân cần thử:** kể "tối nay mình đi đá bóng", hôm sau mở lại web xem Bơ có tự hỏi "đá bóng sao rồi?" không.


## 2026-10-10 – Giai đoạn 4: xử lý lỗi mạng
- Mất mạng / máy chủ AI bận → Bơ tự thử lại tối đa 3 lần (chờ 1s, 2s, 4s). Đổi bằng `API_RETRIES`, `API_TIMEOUT` trong .env.
- Lỗi không đáng thử lại (sai API key, hết tiền) → báo ngay bằng câu dễ hiểu, ví dụ "API key sai hoặc hết hạn. Kiểm tra .env nha."
- Tin nhắn bị lỗi không nằm lại trong lịch sử; trên web có nút **"Thử lại"** cạnh dòng báo lỗi.
- Việc phụ (tóm tắt, gộp trí nhớ) lỗi thì bỏ qua, không bắt chờ.
- 39 test qua hết.

**Tân cần thử:** đang chat thì tắt Wi-Fi, gửi 1 tin → thấy báo lỗi + nút "Thử lại"; bật Wi-Fi lại rồi bấm.

**Tiếp theo:** Giai đoạn 4, việc "Hướng dẫn đưa lên mạng để dùng ngoài nhà".
