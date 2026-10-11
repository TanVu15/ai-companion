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

## Giai đoạn 18 – Bơ biết thêm thế giới (chỉ phần mềm, Claude tự thêm)
- [x] Thời tiết (Open-Meteo miễn phí, không cần tài khoản): đặt THANH_PHO trong .env
- [x] Kiểm tra sức khỏe báo thêm: thời tiết lấy được không, tính cách đang dùng bản nào
- [x] Rà soát code lần 5 (tính cách trên web, thời tiết, dịp đặc biệt), sửa lỗi tìm được

## Giai đoạn 19 – Cá nhân hóa giao diện (chỉ phần mềm, Claude tự thêm)
- [x] Chọn giọng đọc (khi máy có nhiều giọng tiếng Việt)
- [x] Chọn màu khuôn mặt Bơ (lưu trên máy)
- [x] Phím tắt: Esc để Bơ ngừng đọc / đóng hộp, Ctrl+K để tìm

## Giai đoạn 20 – Quản lý trí nhớ tốt hơn (chỉ phần mềm, Claude tự thêm)
- [x] Tự thêm điều cho Bơ nhớ và sửa điều Bơ nhớ sai (trong "Bơ nhớ gì về mình?")
- [x] Tách app.js thành vài file nhỏ theo chức năng (dễ sửa hơn)

## Giai đoạn 21 – Chăm chút tiếp (chỉ phần mềm, Claude tự thêm)
- [x] Rà soát code lần 6 (giọng đọc, màu mặt, phím tắt, sửa điều nhớ, tách file JS), sửa lỗi tìm được
- [x] Chi phí chia theo loại (trò chuyện / tóm tắt / gộp trí nhớ) và 7 ngày gần nhất
- [x] Hoàn tác khi lỡ xóa một điều Bơ nhớ

## Giai đoạn 22 – Dễ làm quen (chỉ phần mềm, Claude tự thêm)
- [x] Gợi ý câu mở đầu khi chưa có tin nhắn nào (bấm là gửi)
- [x] Giờ yên lặng: đêm khuya Bơ không tự đọc to lời nhắc/lời chào
- [x] Cập nhật SU_CO.md (thời tiết, tính cách tự sửa, giọng đọc)

## Giai đoạn 23 – Không mất chữ (chỉ phần mềm, Claude tự thêm)
- [x] Giữ bản nháp tin nhắn đang gõ dở khi tải lại trang / tắt trình duyệt
- [x] Tin gửi lỗi (mất mạng) vẫn giữ trong ô nhập để gửi lại khi tải lại trang

## Giai đoạn 24 – Hiểu tâm trạng (chỉ phần mềm, Claude tự thêm)
- [x] Bơ ghi tâm trạng của Tân mỗi tin; xem "Tâm trạng 7 ngày" trong nút "?"
- [x] Mấy ngày liền Tân buồn/mệt → Bơ quan tâm nhẹ nhàng hơn
- [x] Nhắc trước ngày đặc biệt 1 ngày ("mai là sinh nhật mẹ đó")
- [x] Rà soát code lần 7 (phần mới), sửa lỗi tìm được

## Giai đoạn 25 – Việc cần làm (chỉ phần mềm, Claude tự thêm)
- [x] Bơ ghi việc cần làm ("nhớ giúp mình mua sữa"), gạch khi Tân kể đã làm
- [x] Hộp "Việc cần làm" trên web: xem, đánh dấu xong, thêm, xóa
- [x] Bộ chấm điểm thêm tình huống (việc cần làm, Tân buồn); README cập nhật

## Giai đoạn 26 – Nhắc khéo & bảo trì (chỉ phần mềm, Claude tự thêm)
- [x] Việc cần làm để lâu (từ 3 ngày) → Bơ nhắc khéo khi hợp lúc
- [x] Cổng thiết bị: lấy danh sách việc cần làm (cho màn hình nhỏ sau này)
- [x] SU_CO.md thêm sự cố cho tâm trạng, việc cần làm, nhắc trước ngày đặc biệt
- [x] Rà soát code lần 8 (việc cần làm, chấm điểm, nhắc khéo), sửa lỗi tìm được

## Giai đoạn 27 – Cài đặt trên web (chỉ phần mềm, Claude tự thêm)
- [x] Hộp "Cài đặt": thành phố thời tiết, giờ yên lặng, tổng kết tuần (không cần sửa .env)
- [x] Sửa giờ / nội dung lời nhắc sắp tới ngay trên web
- [x] Rà soát code lần 9 (cài đặt, sửa lời nhắc), sửa lỗi tìm được

## Giai đoạn 28 – Âm lịch & ngày lễ (chỉ phần mềm, Claude tự thêm)
- [x] Đổi ngày dương → âm lịch (không cần mạng), kiểm tra với ngày Tết nhiều năm
- [x] Bơ biết ngày âm hôm nay, hôm nay/ngày mai là lễ gì (Tết, Trung thu, 20/10, 8/3...)
- [x] Ngày đặc biệt theo âm lịch ("giỗ ông 15/7 âm lịch")
- [x] Rà soát code lần 10 (âm lịch, ngày lễ), sửa lỗi tìm được

## Giai đoạn 29 – Lịch nhỏ (chỉ phần mềm, Claude tự thêm)
- [x] Dòng lịch dưới tên Bơ: thứ, ngày dương, ngày âm, lễ hôm nay
- [x] Cổng thiết bị /api/thiet-bi/hom-nay cho màn hình đồng hồ sau này
- [x] Chấm điểm thêm tình huống âm lịch, giỗ âm

## Giai đoạn 30 – Chúc ngày lễ (chỉ phần mềm, Claude tự thêm)
- [x] Ngày lễ (Tết, Trung thu, 20/10...) mở web là Bơ chủ động chúc (mỗi ngày lễ 1 lần, 1 câu API)

## Giai đoạn 31 – Đếm ngược & tự sao lưu (chỉ phần mềm, Claude tự thêm)
- [x] Đếm ngược ngày đặc biệt: danh sách hiện "còn X ngày", Bơ biết ngày đặc biệt trong 7 ngày tới
- [x] Tự sao lưu mỗi ngày vào data/sao_luu/ (giữ 7 bản gần nhất)
- [x] Rà soát code lần 11 (đếm ngược, tự sao lưu), sửa lỗi tìm được

## Giai đoạn 32 – Ngày lễ sắp tới & lịch điện thoại (chỉ phần mềm, Claude tự thêm)
- [x] Bơ biết ngày lễ sắp tới và Tết còn mấy ngày ("còn mấy ngày nữa Tết?")
- [x] Dòng lịch trên web + cổng thiết bị: ngày lễ / ngày đặc biệt sắp tới
- [x] Tải lịch .ics (ngày đặc biệt + lời nhắc) để thêm vào lịch điện thoại
- [x] Rà soát code lần 12, sửa lỗi tìm được

## Giai đoạn 33 – Lời nhắc linh hoạt (chỉ phần mềm, Claude tự thêm)
- [x] Nhắc thứ 2–6 ("ngày đi làm") và mỗi tháng ("ngày 5 hằng tháng"); sửa được trên web; lịch .ics theo kiểu mới
- [x] Sửa lỗi: so trùng không phân biệt hoa/thường với chữ có dấu ("Đi làm" = "đi làm")
- [x] Rà soát code lần 13, sửa lỗi tìm được

## Giai đoạn 34 – Nhật ký ngày (chỉ phần mềm, Claude tự thêm)
- [x] Tân kể chuyện trong ngày → Bơ ghi một dòng nhật ký; Bơ nhớ 3 ngày gần nhất ("hôm qua mình làm gì?")
- [x] Nút "Nhật ký" trên web: xem theo ngày, xóa dòng, xem cũ hơn; có trong bản sao lưu
- [x] Bộ chấm điểm thêm 3 tình huống (ghi nhật ký, không ghi chuyện vặt, nhắc thứ 2–6)
- [x] Rà soát code lần 14, sửa lỗi tìm được

## Giai đoạn 35 – Nhật ký tiện hơn (chỉ phần mềm, Claude tự thêm)
- [x] Tổng kết tuần dựa vào nhật ký (gọn, đúng ngày); ít nhật ký thì dùng tin nhắn như cũ
- [x] Tự ghi / sửa dòng nhật ký trên web, tải nhật ký (.txt)
- [x] Rà soát code lần 15, sửa lỗi tìm được

## Giai đoạn 36 – Kỷ niệm quen nhau & tìm nhật ký (chỉ phần mềm, Claude tự thêm)
- [x] Chuỗi ngày liền trò chuyện trong nút "?"
- [x] Tròn mốc quen nhau (7, 30, 100 ngày, mỗi năm...) Bơ chủ động nhắc (1 câu API mỗi mốc)
- [x] "Tìm" tìm cả trong nhật ký
- [x] Rà soát code lần 16, sửa lỗi tìm được

## Giai đoạn 37 – Thói quen hằng ngày (chỉ phần mềm, Claude tự thêm)
- [x] Bơ theo dõi thói quen ("theo dõi giúp mình thói quen đọc sách"), đánh dấu khi Tân kể đã làm
- [x] Nút "Thói quen" trên web: đánh dấu hôm nay, chuỗi ngày liền, số ngày/tuần; có trong sao lưu
- [x] Rà soát code lần 17, sửa lỗi tìm được

## Giai đoạn 38 – Tài liệu & cổng thiết bị (chỉ phần mềm, Claude tự thêm)
- [x] Cổng thiết bị /api/thiet-bi/thoi-quen; mục "Bơ làm được gì?" và SU_CO.md cập nhật tính năng mới
- [x] Tối (20:30) còn thói quen chưa làm → Bơ nhắc nhẹ một lần (miễn phí, không gọi API)
- [x] Rà soát code lần 18, sửa lỗi tìm được
- [x] Bộ chấm điểm thêm tình huống "nhờ theo dõi thói quen" (26 tình huống)
- [x] Chỉnh giờ nhắc thói quen trong "?" → Cài đặt (không cần sửa .env)

## Giai đoạn 39 – Trả lời nhanh không tốn API (chỉ phần mềm, Claude tự thêm)
- [x] "Mấy giờ rồi?", "hôm nay ngày mấy (âm)?", "còn mấy ngày Tết?", "mình còn việc gì cần làm?" → Bơ tự trả lời (miễn phí, cả khi hết ngân sách)
- [x] Mục "Bơ làm được gì?" và SU_CO.md nhắc tới trả lời nhanh; nút "?" → Tình trạng đếm số câu trả lời nhanh tháng này
- [x] Rà soát code lần 19, sửa lỗi tìm được

## Giai đoạn 40 – Thói quen rõ hơn (chỉ phần mềm, Claude tự thêm)
- [x] Nút "Thói quen": 30 ô vuông cho 30 ngày qua, bấm ô để tích bù ngày quên; "N/30 ngày · chuỗi dài nhất"
- [x] Kể "hôm qua mình có đọc sách" → Bơ tích bù hôm qua (thoi_quen_hom_qua); bộ chấm điểm thêm tình huống (27)
- [x] Hỏi nhanh "thói quen hôm nay?" → Bơ trả lời đã/chưa làm gì (miễn phí)
- [ ] Rà soát code lần 20, sửa lỗi tìm được

## Sau này
- Giọng nói tự nhiên hơn (dịch vụ đọc/nghe trả phí) – cần Tân quyết định
- Phần cứng ESP32: micro, loa, màn hình mặt, servo
