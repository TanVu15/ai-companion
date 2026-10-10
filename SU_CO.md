# Gặp sự cố thì làm gì

Đầu tiên mở http://localhost:8000/api/suc-khoe: trang này cho biết đang thiếu gì (API key, persona, thư mục dữ liệu…).

| Hiện tượng | Nguyên nhân hay gặp | Cách sửa |
|---|---|---|
| Nhấp `run.bat` thì cửa sổ tắt ngay | Chưa cài Python, hoặc lúc cài không tick "Add Python to PATH" | Cài lại Python và tick ô đó. Mở cmd gõ `python --version` để kiểm tra |
| Web hiện dòng đỏ "API key: Chưa có…" | `.env` chưa có key | Mở `.env`, dán key vào `ANTHROPIC_API_KEY=`, chạy lại `run.bat` |
| "API key sai hoặc hết hạn" | Key gõ thiếu hoặc đã bị xóa trên console | Tạo key mới ở console.anthropic.com |
| "Tài khoản API hết tiền rồi" | Hết tín dụng | Nạp thêm ở console.anthropic.com |
| "Tháng này Bơ tiêu hết ngân sách" | Chạm `MONTHLY_USD_LIMIT` | Tăng con số trong `.env` hoặc chờ tháng sau |
| "Hôm nay mình nói nhiều quá rồi" | Chạm `DAILY_LIMIT` (300 câu/ngày) | Tăng con số trong `.env` |
| "Mất mạng rồi…" / "Máy chủ AI đang quá tải" | Wi-Fi chập chờn, hoặc Anthropic bận | Bơ đã tự thử lại 3 lần. Chờ chút rồi bấm "Thử lại" |
| "Không kết nối được máy chủ" | Cửa sổ `run.bat` đã bị tắt | Chạy lại `run.bat` |
| iPhone không vào được `http://192.168…:8000` | Khác Wi-Fi, hoặc Windows Firewall chặn | Cùng Wi-Fi; khi Windows hỏi thì cho phép Python. Gõ `ipconfig` để xem IP đúng |
| Không thấy nút micro | Trình duyệt chỉ cho dùng micro ở `localhost` hoặc `https` | Dùng trên máy tính, hoặc link https ở DUA_LEN_MANG.md |
| Bấm micro báo "chưa cho dùng micro" | Đã bấm "Chặn" lúc trình duyệt hỏi | Bấm biểu tượng ổ khóa cạnh địa chỉ web → cho phép Micro |
| Bơ đọc giọng không phải tiếng Việt | Máy chưa có giọng tiếng Việt | Windows: Cài đặt → Thời gian & ngôn ngữ → Giọng nói → thêm Tiếng Việt |
| Lời nhắc không kêu | Lúc đó web không mở, hoặc máy tính tắt/ngủ | Để trang Bơ mở. Nhắc trễ thì Bơ vẫn báo khi mở lại web |
| Bơ nhớ sai điều gì đó | AI ghi nhầm | "Bơ nhớ gì về mình?" → Xóa dòng sai. Hoặc nhắn Bơ "không phải, mình…" |
| Mới `git pull` mà web vẫn cũ | Cửa sổ `run.bat` cũ còn chạy | Tắt cửa sổ đó, chạy lại `run.bat` (nó tự cài thêm thư viện mới nếu có). Vẫn lỗi thư viện thì xóa thư mục `.venv` rồi chạy lại |
| Hỏi mật khẩu mãi | Gõ sai `APP_PASSWORD` | Mật khẩu phân biệt hoa/thường, tên đăng nhập gõ gì cũng được |

## Vẫn không được?

1. Mở `data/loi.log` (nhật ký lỗi, không chứa tin nhắn hay API key), chép khoảng 20 dòng cuối.
2. Dán vào `FEEDBACK.md` kèm vài chữ mô tả đang làm gì thì bị lỗi.
3. Lần chạy sau Claude sẽ đọc và sửa trước mọi việc khác.
