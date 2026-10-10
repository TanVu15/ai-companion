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
- [x] Gộp/sửa điều đáng nhớ bị trùng hoặc lỗi thời
- [x] Bơ chủ động hỏi thăm chuyện cũ (ví dụ: "hôm qua tập chân sao rồi?")

## Giai đoạn 4 – Hoàn thiện
- [x] Xử lý lỗi mạng, thử lại
- [x] Hướng dẫn đưa lên mạng để dùng ngoài nhà (DUA_LEN_MANG.md + mật khẩu APP_PASSWORD)
- Chờ Tân: dùng thử 1 tuần, ghi góp ý vào FEEDBACK.md (không chặn việc khác)

## Giai đoạn 5 – Giọng nói (chỉ phần mềm, dùng sẵn của trình duyệt, miễn phí)
- [x] Bấm micro để nói, Bơ đọc to câu trả lời (bật/tắt, nhớ lựa chọn)
- [x] Chế độ rảnh tay: nghe liên tục, gọi "Bơ ơi" mới trả lời
- [x] Câu trả lời dễ đọc to: bỏ ký hiệu/emoji khi đọc, đọc nhanh/chậm chỉnh được

## Giai đoạn 6 – Chuẩn bị cho phần cứng (chỉ phần mềm)
- [x] Tài liệu "giao tiếp với thiết bị" (THIET_BI.md): thiết bị gửi chữ, nhận JSON {noi, cam_xuc, hanh_dong}
- [x] Endpoint gọn cho thiết bị nhỏ (ESP32): trả JSON ngắn, có khóa thiết bị riêng

## Giai đoạn 7 – Tiện ích (chỉ phần mềm, Claude tự thêm)
- [x] Theo dõi chi phí: đếm token mỗi ngày, ước tính tiền, xem trên web
- [x] Sao lưu / khôi phục trí nhớ (tải file về, nạp lại)
- [x] Hiện giờ gửi tin nhắn, tải thêm tin cũ khi kéo lên
- [x] Thêm tình huống "hỏi thăm chuyện cũ" vào bộ chấm điểm tính cách

## Giai đoạn 8 – Ổn định & tiện dùng (chỉ phần mềm, Claude tự thêm)
- [x] An toàn khi 2 tin gửi cùng lúc (điện thoại + máy tính)
- [x] Giới hạn chi phí theo tiền mỗi tháng (ngoài giới hạn số câu/ngày)
- [x] Kiểm tra sức khỏe /api/suc-khoe: báo thiếu API key, thiếu persona, dung lượng dữ liệu
- [x] Thêm Bơ vào màn hình chính iPhone (biểu tượng, mở toàn màn hình)
- [x] Nhắc việc theo giờ ("8h tối nhắc mình gọi mẹ"), báo khi web đang mở

## Giai đoạn 9 – Rà soát & gọn gàng (chỉ phần mềm, Claude tự thêm)
- [x] Rà soát toàn bộ code tìm lỗi (một lượt review độc lập), sửa lỗi tìm được
- [x] Tách JS của web ra file riêng cho dễ sửa (index.html đang dài)
- [x] Bơ biết thứ trong tuần và buổi (sáng/trưa/tối) để chào hợp lúc

## Giai đoạn 10 – Dễ bảo trì (chỉ phần mềm, Claude tự thêm)
- [x] Tự chạy test trên GitHub mỗi lần đẩy code (GitHub Actions)
- [x] Ghi lỗi ra file `data/loi.log` để Tân gửi khi gặp sự cố
- [x] Hướng dẫn khắc phục sự cố thường gặp (SU_CO.md)

## Giai đoạn 11 – Khuôn mặt sống động (chỉ phần mềm, Claude tự thêm)
- [x] Mở lại web: Bơ giữ vẻ mặt của câu nói cuối
- [x] Ngủ gật khi 3 phút không ai đụng tới, chạm là tỉnh

## Giai đoạn 12 – Trò chuyện tự nhiên (chỉ phần mềm, Claude tự thêm)
- [x] Câu trả lời dài tách thành 2–3 bong bóng, có "Bơ đang gõ..." ở giữa
- [x] Lâu không gặp (2 ngày) thì Bơ chủ động chào dù không có chuyện để hỏi
- [x] Chạm vào mặt Bơ để Bơ ngừng đọc to

## Giai đoạn 13 – Xem lại chuyện cũ (chỉ phần mềm, Claude tự thêm)
- [x] Tìm trong lịch sử trò chuyện (gõ không dấu vẫn tìm được)
- [x] Ngày đặc biệt: Tân kể sinh nhật/kỷ niệm → đúng ngày Bơ chúc
- [x] Tải lịch sử trò chuyện về thành file chữ (.txt) để đọc lại

## Giai đoạn 14 – Lời nhắc tiện hơn (chỉ phần mềm, Claude tự thêm)
- [x] Lời nhắc lặp lại: "7h sáng mỗi ngày nhắc mình uống nước", "tối thứ Hai hằng tuần..."
- [x] Nút "Nhắc lại sau 10 phút" ngay dưới lời nhắc
- [x] Rà soát code lần 3 (review độc lập phần mới: tìm, ngày đặc biệt, lời nhắc lặp), sửa lỗi tìm được

## Giai đoạn 15 – Bạn đồng hành (chỉ phần mềm, Claude tự thêm)
- [x] Nút "?" – Bơ làm được gì: liệt kê mẹo dùng (không tốn API)
- [x] Ghim tin nhắn đáng nhớ, xem lại danh sách ghim
- [x] Tổng kết tuần: tối Chủ nhật mở web, Bơ điểm lại tuần qua (1 câu API/tuần)

## Giai đoạn 16 – Chăm chút (chỉ phần mềm, Claude tự thêm)
- [x] Bộ chấm điểm tính cách: thêm tình huống sinh nhật, nhắc mỗi ngày
- [x] "Bơ và bạn": đã quen bao nhiêu ngày, bao nhiêu tin nhắn (trong nút "?")
- [x] Cập nhật README cho các tính năng mới
- [x] Rà soát code lần 4 (ghim, tổng kết tuần), sửa lỗi tìm được

## Giai đoạn 17 – Tự tay chỉnh Bơ (chỉ phần mềm, Claude tự thêm)
- [x] Sửa tính cách Bơ ngay trên web (lưu riêng trong data/, có nút về mặc định)
- [x] Dịp đặc biệt (sinh nhật, tổng kết tuần) kiểm tra cả khi trang đang mở
- [x] Kiểm tra giao diện trên màn hình điện thoại nhỏ (chụp ảnh tự động), sửa chỗ vỡ

## Sau này
- Giọng nói tự nhiên hơn (dịch vụ đọc/nghe trả phí) – cần Tân quyết định
- Phần cứng ESP32: micro, loa, màn hình mặt, servo
