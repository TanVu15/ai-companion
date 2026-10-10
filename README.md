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

## Đổi tính cách

Sửa file `persona.md` rồi gửi tin nhắn mới. Không cần khởi động lại.

## Cấu trúc

```
app/brain.py    Bộ não: ghép tính cách + trí nhớ + lịch sử, hỏi Claude, đọc JSON
app/memory.py   Trí nhớ: SQLite lưu tin nhắn và điều đáng nhớ (data/companion.db)
app/main.py     Máy chủ web (FastAPI)
web/index.html  Giao diện chat + khuôn mặt
persona.md      Tính cách
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
