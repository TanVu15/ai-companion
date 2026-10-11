# Hướng phát triển: Mèo Bơ

Tân chốt ngày 2026-10-11. **Đây là ưu tiên số 1.** Mọi phiên tự chạy đọc file này trước.

## Bơ là ai
Bơ là **một con mèo béo**, tròn ủm, lười mà lanh, sống trên màn hình của Tân.
Không còn là "khuôn mặt tròn" nữa. Bơ có cả thân: đầu, tai, mắt, ria, miệng, bụng, chân, đuôi.
Bơ biết nói chuyện (bộ não giữ nguyên), **nói bằng giọng thật**, và **phản ứng khi được chạm vào**.

Mục tiêu cảm xúc: mở web lên là thấy vui, muốn chọc Bơ một cái. Dễ thương kiểu "pet ảo",
nhưng KHÔNG gây áp lực: không có chỉ số đói chết, không phạt khi Tân bỏ đi vài ngày,
không dụ Tân ở lại lâu. Bỏ đi lâu thì quay lại Bơ chỉ mừng rỡ.

## Ba trụ cột
1. **Nhân vật mèo sống động** – vẽ bằng SVG + CSS (không dùng ảnh ngoài, không thư viện nặng),
   tách từng bộ phận để chuyển động riêng. Luôn "sống": thở, vẫy đuôi, chớp mắt, thỉnh thoảng ngáp/liếm chân.
2. **Chạm & chơi** – vuốt ve, chọc, gãi cằm, cho ăn, chơi cuộn len/tia laser. Phần lớn KHÔNG gọi API (miễn phí, tức thì).
3. **Giọng nói AI miễn phí** – `edge-tts` (giọng Microsoft Edge tiếng Việt, không cần tài khoản),
   chạy ở máy chủ trên máy Tân, web phát file mp3. Lỗi thì tự quay về giọng của trình duyệt.

## Ràng buộc kỹ thuật (không được phá)
- Bộ não vẫn trả JSON `{noi, cam_xuc, hanh_dong, ...}`. Mèo chỉ là "cơ thể" mới đọc JSON đó.
  Ánh xạ 7 cảm xúc + 6 hành động hiện có sang tư thế mèo. Thêm cảm xúc/hành động mới thì thêm cả vào config + test.
- Cổng thiết bị (`/api/thiet-bi/...`) giữ nguyên: sau này có thể làm mèo robot thật.
- Điện thoại là màn hình chính: mọi thứ phải đẹp và bấm được trên màn hình 375px.
- Tôn trọng `prefers-reduced-motion`: giảm chuyển động khi máy yêu cầu.
- Test không gọi mạng: giả lập edge-tts, giả lập API Claude như cũ.

## Kiểm tra giao diện (bắt buộc với mọi thay đổi ở web/)
Máy làm việc có sẵn Chromium + Playwright. Sau mỗi thay đổi giao diện:
1. Chạy máy chủ với `DEMO=1`, chụp ảnh ở 390×800 (điện thoại) và 1100×800 (máy tính).
2. **Tự mở ảnh ra xem** (công cụ Read đọc được ảnh). Thấy vỡ, xấu, đè chữ thì sửa rồi chụp lại.
3. Lưu ảnh đẹp nhất vào `docs/anh/` (ví dụ `meo-vui.png`, `meo-ngu.png`) và nhắc tên ảnh trong PROGRESS.md
   để Tân xem ngay trên GitHub mà không cần chạy.

## Tạm dừng
Không thêm tính năng mới ngoài hướng này (không thêm lịch, thói quen, nhắc việc, thời tiết...).
Chỉ sửa lỗi ở các tính năng cũ khi Tân báo trong FEEDBACK.md hoặc khi đụng tới.
