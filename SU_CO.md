# Gặp sự cố thì làm gì

Đầu tiên bấm nút **"?"** trên web → mục **Tình trạng** (hoặc mở http://localhost:8000/api/suc-khoe): cho biết đang thiếu gì (API key, tính cách, thư mục dữ liệu, thời tiết…).

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
| Bơ nhớ sai điều gì đó | AI ghi nhầm | "Bơ nhớ gì về mình?" → Sửa hoặc Xóa dòng sai (lỡ xóa thì bấm "Hoàn tác"). Hoặc nhắn Bơ "không phải, mình…" |
| Sửa tính cách xong Bơ nói chuyện lạ | Bản tự sửa thiếu ý | Nút "Tính cách" → "Về mặc định". Bản cũ hơn nằm ở `data/persona_tu_sua.<ngày giờ>.md` |
| Bơ không biết thời tiết | Chưa đặt hoặc gõ sai `THANH_PHO` | Thêm `THANH_PHO=Da Nang` vào `.env`, chạy lại. Nút "?" → Tình trạng báo "không tìm thấy thành phố" thì thử tên tiếng Anh (Hanoi, Ho Chi Minh City) |
| Không thấy nút "Giọng: …" | Máy chỉ có 1 giọng tiếng Việt | Bình thường. Edge thường có nhiều giọng tiếng Việt hơn Chrome |
| Đêm khuya lời nhắc không đọc to | Giờ yên lặng (mặc định 23h–6h) | Đổi `GIO_YEN_LANG` trong `.env`, để trống để tắt |
| Dải tâm trạng đoán sai (đang vui mà hiện 😢) | Bơ chỉ đoán qua chữ | Không sao, chỉ là ước chừng. Nhắn rõ hơn ("hôm nay vui lắm") là ngày đó đổi theo |
| Bơ cứ an ủi dù mình hết buồn rồi | Mấy hôm trước buồn nên Bơ được dặn nhẹ nhàng | Nhắn một câu vui là Bơ thôi ngay trong ngày |
| Bơ ghi nhầm "việc cần làm" (hoặc không ghi) | AI hiểu nhầm nhờ nhắc với nhờ ghi | Nút "Việc cần làm" → Xóa hoặc tự thêm. Có giờ cụ thể ("8h tối...") thì Bơ đặt lời nhắc thay vì ghi việc |
| Bỏ đánh dấu việc thì báo "đang có trong danh sách rồi" | Đã có việc y hệt chưa xong | Bình thường, giữ một việc là đủ |
| Hôm trước ngày đặc biệt Bơ không nhắc | Hôm đó không mở web (hoặc mở trước 8h sáng), hoặc Tân vừa mới kể ngày đó | Đúng ngày Bơ vẫn chúc |
| Lỡ đổi màu mặt Bơ | — | Nút "?" → Màu mặt Bơ → chọn "Vàng (mặc định)" |
| Mới `git pull` mà web vẫn cũ | Cửa sổ `run.bat` cũ còn chạy | Tắt cửa sổ đó, chạy lại `run.bat` (nó tự cài thêm thư viện mới nếu có). Vẫn lỗi thư viện thì xóa thư mục `.venv` rồi chạy lại |
| Hỏi mật khẩu mãi | Gõ sai `APP_PASSWORD` | Mật khẩu phân biệt hoa/thường, tên đăng nhập gõ gì cũng được |

## Vẫn không được?

1. Mở `data/loi.log` (nhật ký lỗi, không chứa tin nhắn hay API key), chép khoảng 20 dòng cuối.
2. Dán vào `FEEDBACK.md` kèm vài chữ mô tả đang làm gì thì bị lỗi.
3. Lần chạy sau Claude sẽ đọc và sửa trước mọi việc khác.
