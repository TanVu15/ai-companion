# Hướng dẫn cho Claude khi làm dự án này

## Dự án
Chatbot "người bạn" AI (tên tạm: Bơ). Làm bộ não trước (phần mềm), sau gắn phần cứng.
Chủ dự án: Tân (TanVu15). Giao tiếp tiếng Việt, đơn giản, giải thích thuật ngữ.

## Nguyên tắc
- Bộ não KHÔNG phụ thuộc giao diện: luôn trả về JSON {noi, cam_xuc, hanh_dong, ghi_nho}.
  Giao diện (web hôm nay, phần cứng sau này) chỉ đọc JSON đó.
- Không gọi API thật trong test. Dùng FakeClient trong tests/test_brain.py.
- Không bao giờ commit .env hay data/.
- Giữ chi phí thấp: model Haiku, giới hạn lịch sử và số câu trả lời mỗi ngày.

## Quy trình mỗi phiên
1. Đọc PROGRESS.md, rồi lấy việc chưa xong đầu tiên trong TASKS.md.
2. Làm việc đó, chạy `python -m pytest -q` cho đến khi qua hết.
3. Commit (tin nhắn commit tiếng Việt, ngắn gọn), cập nhật TASKS.md và PROGRESS.md.
4. Hết một giai đoạn thì DỪNG, ghi "Chờ nghiệm thu" vào PROGRESS.md, không tự sang giai đoạn sau.

## Chạy
- `run.bat` (Windows) hoặc `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
- `DEMO=1` trong .env để chạy không cần API key.
