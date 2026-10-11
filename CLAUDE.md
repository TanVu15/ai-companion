# Hướng dẫn cho Claude khi làm dự án này

## Dự án
Bơ – một con **mèo béo** AI biết trò chuyện, nói bằng giọng thật và phản ứng khi được chạm vào.
**Đọc HUONG_PHAT_TRIEN.md trước tiên** – đó là hướng Tân đã chốt và là ưu tiên số 1.
Chủ dự án: Tân (TanVu15). Giao tiếp tiếng Việt, đơn giản, giải thích thuật ngữ.

## Nguyên tắc
- Bộ não KHÔNG phụ thuộc giao diện: luôn trả về JSON {noi, cam_xuc, hanh_dong, ghi_nho}.
  Giao diện (web hôm nay, phần cứng sau này) chỉ đọc JSON đó.
- Không gọi API thật trong test. Dùng FakeClient trong tests/test_brain.py.
- Không bao giờ commit .env hay data/.
- Giữ chi phí thấp: model Haiku, giới hạn lịch sử và số câu trả lời mỗi ngày.

## Chế độ tự chạy (Tân chọn ngày 2026-10-11: "làm liền, báo sau")
Một tác vụ hẹn giờ chạy mỗi giờ, mỗi lần làm khoảng 50 phút. Mỗi lần chạy là một phiên mới, không nhớ phiên trước,
nên mọi thứ cần biết phải nằm trong repo.

0. Nếu repo có file `STOP` ở thư mục gốc → không làm gì, kết thúc ngay.
1. `git pull`. Đọc PROGRESS.md, lấy việc chưa xong đầu tiên trong TASKS.md
   (bỏ qua dòng "Chờ Tân nghiệm thu" — đó chỉ là ghi chú để Tân duyệt sau).
2. Làm LIÊN TỤC hết việc này sang việc kia (Tân yêu cầu ngày 2026-10-11: chạy đến khi hết hạn mức,
   reset thì chạy tiếp). Mỗi việc: chạy `python -m pytest -q` cho đến khi qua hết, không commit code test đỏ.
   Dừng khi đã làm khoảng 50 phút trong một lần chạy (lần chạy giờ sau sẽ tiếp tục).
3. Commit (tiếng Việt, ngắn gọn), cập nhật TASKS.md và PROGRESS.md, `git push`.
4. Hết một giai đoạn: viết báo cáo ngắn trong PROGRESS.md (làm gì, Tân cần thử gì),
   rồi làm tiếp giai đoạn sau. Không dừng chờ duyệt.
5. Nếu Tân góp ý trong file FEEDBACK.md, ưu tiên xử lý góp ý trước việc mới.
6. Chỉ làm việc thuộc hướng trong HUONG_PHAT_TRIEN.md (mèo, chạm & chơi, giọng nói).
   KHÔNG tự thêm tính năng ngoài hướng đó (Tân đã thấy agent tự thêm quá nhiều thứ: lịch, thói quen, thời tiết...).
   Hết việc trong TASKS.md: tự thêm việc mới nhưng chỉ để làm mèo/tương tác/giọng hay hơn, hoặc rà soát và sửa lỗi.
   Việc cần phần cứng, cần tiền, cần tài khoản mới hay cần Tân quyết định → ghi vào
   mục "Cần Tân quyết định" trong PROGRESS.md và không làm.
7. Một phiên bị dừng giữa chừng (hết lượt dùng) là bình thường: phiên sau đọc PROGRESS.md
   và `git status` để làm tiếp. Luôn commit từng bước nhỏ.

## Giao diện
Mọi thay đổi ở web/: chụp ảnh bằng Playwright (điện thoại 390×800 + máy tính), tự mở ảnh xem, sửa đến khi đẹp,
lưu ảnh vào docs/anh/. Chi tiết trong HUONG_PHAT_TRIEN.md.
Sửa chạm & chơi (choi.js, do_choi.js, meo.js) xong thì chạy `python scripts/thu_cham.py` (bấm thử mọi trò trên trình duyệt thật, phải ĐẠT hết).

## Chạy
- `run.bat` (Windows) hoặc `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
- `DEMO=1` trong .env để chạy không cần API key.
