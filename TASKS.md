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
- [x] Rà soát code lần 20, sửa lỗi tìm được

## Giai đoạn 41 – Hỏi nhanh thêm & tổng kết thói quen (chỉ phần mềm, Claude tự thêm)
- [x] Hỏi nhanh thời tiết ("hôm nay trời thế nào?", "mai có mưa không?") dùng dữ liệu đã lấy sẵn, miễn phí
- [x] Tổng kết tuần tối Chủ nhật nhắc tới thói quen (khen/động viên theo số ngày đã làm)
- [x] Nút "Thói quen": số ngày làm trong tháng này của từng thói quen
- [x] Rà soát code lần 21, sửa lỗi tìm được

## Giai đoạn 42 – Nhắc mỗi vài tiếng (chỉ phần mềm, Claude tự thêm)
- [x] "Cứ 2 tiếng nhắc mình uống nước" → nhắc mỗi N tiếng (1–12), tự nghỉ trong giờ yên lặng; sửa được trên web; không đưa vào lịch .ics
- [x] Nói "thôi khỏi nhắc uống nước nữa" → Bơ xóa lời nhắc đó (huy_nhac); chấm điểm thêm tình huống (29)
- [x] Rà soát code lần 22, sửa lỗi tìm được

## Giai đoạn 43 – Chạy thật với API (chỉ phần mềm, Claude tự thêm sau khi chạy thử trên máy Tân)
- [x] Ép model trả đúng khuôn JSON (structured outputs): hết cảnh Bơ trả lời chữ thường làm mất cảm xúc, điều ghi nhớ, lời nhắc
- [x] Giá tính chi phí lấy theo model (Haiku 5.5: 0,10 / 0,50 đô), nút "?" báo khi .env ghi giá lệch
- [x] Sửa lỗi Bơ hỏi lại mãi một chuyện (model chép cả ghi chú "(kể hôm qua)" nên không gạch được chuyện đã hỏi thăm)
- [x] Lời dặn chắc hơn: không bịa số đường dây nóng (chỉ 115), không hứa "đi cùng", nhất định chúc ngày đặc biệt, chuyện hỏi thăm ghi ngày cụ thể, không chép việc vặt vào điều nhớ lâu dài
- [x] Bộ chấm điểm: kiểm tra chặt hơn (gạch được chuyện hỏi thăm thật, không bịa số điện thoại...), báo số token đã dùng
- [x] Giảm tiền mỗi câu: gom lời dặn cố định lên đầu để dùng prompt caching (câu thứ hai trở đi trong 5 phút rẻ hơn ~5 lần), đã đo bằng API thật
- [x] Rà soát code lần 23 (phần mới của giai đoạn 43), sửa lỗi tìm được

## Giai đoạn 44 – Tin cậy khi dùng thật (chỉ phần mềm, Claude tự thêm)
- [x] Dưới câu trả lời hiện dòng nhỏ "✓ Bơ đã ghi: nhắc 20:00 12/10: Gọi mẹ · việc cần làm: Mua sữa..." để Tân biết Bơ ghi thật (model đôi khi hứa nhắc mà không ghi); mở lại web vẫn thấy, có trong sao lưu
- [x] Chạy thử bằng API thật các lời Bơ tự mở đầu (hỏi thăm, lâu không gặp, tổng kết tuần, chúc lễ 20/10, sinh nhật, mốc 100 ngày); sửa: Bơ tự mở lời thì không ghi gì mới, hỏi thăm xong không ghi lại chuyện đó, tin cũ được ghi chú ngày gửi
- [x] Gộp trí nhớ: khi dọn "điều Bơ nhớ" thì bỏ luôn việc vặt / chuyện đã qua lỡ ghi vào; AI xóa quá tay thì giữ nguyên bản cũ
- [x] Rà soát code lần 24, sửa lỗi tìm được

## Giai đoạn 46 – Mèo Bơ ra đời (ƯU TIÊN, xem HUONG_PHAT_TRIEN.md)
- [x] Vẽ mèo béo bằng SVG trong file riêng (web/meo.js hoặc web/meo.svg): đầu, 2 tai, mắt, ria, miệng, bụng, 4 chân, đuôi – mỗi bộ phận có id/class để CSS chuyển động riêng. Màu mặc định cam/kem; giữ nút chọn màu cũ (đổi màu lông)
- [x] Thay khuôn mặt tròn bằng mèo ở đầu trang (điện thoại: mèo chiếm khoảng 1/3 màn hình, khung chat bên dưới)
- [x] Ánh xạ 7 cảm xúc sang mèo: vui (mắt cong ^^, đuôi dựng), hào hứng (nhún nhảy), bình thường, suy nghĩ (nghiêng đầu, tai xoay), ngạc nhiên (mắt tròn, lông xù nhẹ), buồn (tai cụp, đuôi rủ), thương (má hồng, mắt lim dim)
- [x] Ánh xạ 6 hành động: gật đầu, lắc đầu, nghiêng đầu, nhảy, vẫy tay (vẫy chân trước), không
- [x] "Sống" khi rảnh: thở (bụng phập phồng), đuôi đung đưa, chớp mắt ngẫu nhiên, thỉnh thoảng ngáp/liếm chân
- [x] Ngủ gật (đã có, 3 phút) → mèo cuộn tròn ngủ, "zzz" bay lên; chạm là tỉnh, vươn vai
- [x] Đang "Bơ đang gõ..." → mèo ngoe nguẩy đuôi nhìn lên; đang đọc to → miệng mấp máy
- [x] Chụp ảnh từng cảm xúc (điện thoại + máy tính), tự xem, lưu vào docs/anh/; cập nhật README (ảnh mèo ở đầu)

## Giai đoạn 47 – Chạm & chơi với Bơ (không tốn API)
- [x] Vuốt ve: rê chuột / kéo ngón tay trên lưng-đầu → mèo nhắm mắt, kêu "rừ rừ" (âm thanh tạo bằng Web Audio, không cần file), tim bay lên
- [x] Chọc bụng → giật mình; chọc liên tục 5 lần → giận dỗi quay lưng vài giây rồi làm lành
- [x] Gãi cằm → ngửa cổ sướng; chạm tai → tai giật
- [x] Nút "Cho ăn" (con cá): mèo chạy tới ăn, liếm mép. Không có thanh "đói", không bắt buộc cho ăn
- [x] Đồ chơi: cuộn len / chấm laser đi theo ngón tay, mèo đuổi theo vồ
- [x] Mỗi tương tác thỉnh thoảng có câu ngắn có sẵn ("meo~ thêm chút nữa đi") hiện bong bóng nhỏ, không lưu vào lịch sử chat
- [x] Bơ "nhớ" nhẹ: hôm nay được vuốt mấy lần, cho ăn chưa → gửi kèm 1 dòng ngắn cho bộ não để Bơ nhắc tới khi hợp ("hôm nay bạn gãi cằm Bơ 5 lần đó nha")
- [x] Chụp ảnh/kiểm tra trên màn hình điện thoại: chạm không bị nhầm với cuộn trang

## Giai đoạn 48 – Bơ nói bằng giọng AI miễn phí (edge-tts)
- [x] Thêm `edge-tts` vào requirements. Endpoint `/api/giong` nhận chữ → trả mp3; lưu đệm theo nội dung trong data/am_thanh/ (xóa bớt khi quá 200 file)
- [x] Giọng mặc định `vi-VN-HoaiMyNeural`, chỉnh cao độ hơi cao cho dễ thương; chọn được `vi-VN-NamMinhNeural`, tốc độ, cao độ trong Cài đặt
- [x] Web phát mp3 thay cho giọng trình duyệt khi bật "Giọng nói"; edge-tts lỗi/không mạng → tự dùng giọng trình duyệt, báo nhỏ một lần
- [x] Miệng mèo mấp máy theo âm lượng thật của file đang phát (Web Audio analyser)
- [x] Câu dài: tách câu, đọc câu đầu ngay để đỡ chờ
- [x] Test giả lập edge-tts (không gọi mạng). Ghi "Tân cần thử" vì máy làm việc của Claude không gọi được Microsoft

## Giai đoạn 49 – Trò chuyện bằng giọng mượt
- [x] Nút micro to "bấm giữ để nói" ngay dưới mèo (kiểu bộ đàm), thả ra là gửi
- [x] Khi đang nói chuyện bằng giọng: dặn bộ não trả lời ngắn hơn (1–2 câu), không ký hiệu
- [x] Mèo nghiêng tai lắng nghe khi micro đang bật

## Giai đoạn 50 – Gọn & chắc (Claude tự thêm, trong hướng mèo/chạm/giọng)
- [x] Gọn đầu trang trên điện thoại: gom các nút chữ (nhớ, việc, nhật ký, thói quen, tìm, chi phí, tính cách...) vào nút "☰ Thêm", chỉ để lại Giọng nói / Rảnh tay → mèo + khung chat rộng hơn
- [x] Nút "?" → Tình trạng: báo giọng AI dùng được không (đã thử gần nhất lúc nào, lỗi gì)
- [x] Rà soát code giai đoạn 46–49 (mèo, chạm & chơi, giọng AI, giữ để nói), sửa lỗi tìm được

## Giai đoạn 51 – Bơ sống động hơn (Claude tự thêm, trong hướng mèo/chạm)
- [x] Mắt Bơ nhìn theo ngón tay/chuột khi rê gần (không chỉ lúc chơi laser); đứng yên 3 giây thì thôi nhìn
- [x] Mở web sau lâu (từ 1 ngày) → Bơ mừng rỡ: nhảy cẫng, bong bóng "Bạn về rồi!" (không trách, không gọi API)
- [x] Nhấn giữ lên lưng/bụng khoảng 1 giây → Bơ lăn qua lăn lại nũng nịu, co chân trước lên ngực
- [x] Theo giờ: khuya (sau 22h) Bơ lim dim, hay ngáp hơn; sáng sớm mở web thì Bơ vươn vai
- [x] Rà soát giai đoạn 51, sửa lỗi tìm được

## Giai đoạn 52 – Giọng có cảm xúc, đồ chơi cuộn len (Claude tự thêm, trong hướng mèo/chạm/giọng)
- [x] Giọng AI đổi nhẹ theo cảm xúc của câu: vui/hào hứng nhanh và cao hơn, buồn chậm và trầm hơn (giọng trình duyệt cũng vậy)
- [x] Đang bật "Giọng nói": vài câu chơi (mừng rỡ, ăn cá, dỗi, làm lành) được đọc to bằng giọng AI (câu ngắn, có sẵn → lưu đệm, gần như không tốn mạng)
- [x] Đồ chơi cuộn len: nút cuộn len (trên nút cá); kéo ném cuộn len, nó lăn và nảy, Bơ vồ đập văng khi len chạm người
- [x] Rà soát giai đoạn 52, sửa lỗi tìm được

## Giai đoạn 53 – Bơ hóng chuyện, giọng mẫu (Claude tự thêm, trong hướng mèo/chạm/giọng)
- [x] Bơ hóng chuyện: đang gõ tin → Bơ nhìn xuống khung chat, tai vểnh; ngừng gõ 2 giây thì thôi
- [x] Khuya (22h–5h) vuốt Bơ → câu riêng nhẹ nhàng ("khuya rồi, bạn ngủ sớm nha~"), không ép
- [x] Cài đặt giọng: nút mẫu nhanh "Mèo con" / "Mèo béo lười" / "Mặc định" (đặt sẵn tốc độ + cao độ)
- [x] README: cập nhật ảnh và mô tả chạm & chơi mới (lăn nũng, cuộn len, mừng rỡ)
- [x] Rà soát giai đoạn 53, sửa lỗi tìm được

## Giai đoạn 54 – Tư thế & bộ lông (Claude tự thêm, trong hướng mèo)
- [x] Rảnh 1 phút: Bơ nằm bẹp kiểu "ổ bánh mì" (giấu chân, đuôi quấn); 3 phút mới ngủ gật; có gì là ngồi dậy
- [x] Kiểu lông: mướp vằn, tam thể, mèo đen mắt vàng… chọn cạnh bảng màu lông (lưu trên máy)
- [x] Rà soát giai đoạn 54, sửa lỗi tìm được
- [x] Đổi màu/kiểu lông xong, đóng hộp → Bơ nhảy lên khoe "Bộ lông mới nè, Bơ đẹp hông?"
- [x] Bộ ảnh mèo (scripts/chup_meo.py) có thêm lăn, mừng, ổ bánh mì, hóng chuyện, lắng nghe

## Giai đoạn 55 – Thêm chút sống động (Claude tự thêm, trong hướng mèo/chạm/giọng)
- [x] Ngủ say thì thỉnh thoảng Bơ giật tai trong mơ hoặc trở mình
- [x] Bơ đang đọc to thì đuôi vẫy nhanh hơn, tai động nhẹ
- [x] Đồ chơi cần câu lông vũ: lông vũ lơ lửng trên đầu Bơ theo ngón tay, Bơ đứng lên vồ bằng hai chân trước
- [x] Rà soát giai đoạn 55, sửa lỗi tìm được

## Giai đoạn 56 – Ý tưởng tiếp (Claude tự thêm, trong hướng mèo/chạm/giọng)
- [x] Rà soát toàn bộ choi.js (đã dài ~500 dòng): tách đồ chơi (laser, cuộn len, lông vũ) ra file riêng web/do_choi.js cho dễ sửa, giữ nguyên hành vi, có test
- [x] Đồ chơi dùng được bằng bàn phím: phím mũi tên di chuyển laser/lông vũ, mũi tên hất cuộn len
- [x] Bơ phản ứng khi Tân nói "Bơ ơi" bằng rảnh tay: nghiêng đầu, bong bóng "Dạ? Bơ nghe nè!" (chỉ chữ, không đọc to để micro khỏi nghe nhầm)
- [x] Rà soát giai đoạn 56, sửa lỗi tìm được

## Giai đoạn 57 – Chạm tinh tế hơn (Claude tự thêm, trong hướng mèo/chạm)
- [x] Vuốt ngược lông (từ đuôi lên đầu, hướng ngược) → Bơ nhăn mặt, lông dựng nhẹ, "Ngược lông rồi á!"; vuốt xuôi mới rừ rừ (hàm tính hướng vuốt có test)
- [x] Chạm nhanh hai lần lên chân trước → Bơ giơ chân "đập tay" (high five), bong bóng "Đập tay nè!"
- [x] Rảnh lâu (trước khi nằm bẹp), thỉnh thoảng Bơ tự rửa mặt bằng chân hoặc ngó quanh (không gọi API, tôn trọng giảm chuyển động)
- [x] Rà soát giai đoạn 57, sửa lỗi tìm được

## Giai đoạn 58 – Đuôi & tiếng meo (Claude tự thêm, trong hướng mèo/chạm/giọng)
- [x] Chạm vào đuôi → đuôi giật vụt đi, Bơ quay đầu nhìn đuôi "Đuôi Bơ mà!" (vùng chạm 'duoi' có test)
- [x] Tiếng "meo" ngắn tạo bằng Web Audio (không cần file, không gọi mạng) khi chạm tai/đập tay/mừng rỡ; chỉ kêu khi bật "Giọng nói", giờ yên lặng thì im
- [x] Rà soát giai đoạn 58, sửa lỗi tìm được

## Giai đoạn 59 – Ngửi tay & cọ má (Claude tự thêm, trong hướng mèo/chạm)
- [x] Giữ yên ngón tay/chuột trước mũi Bơ khoảng 1 giây → Bơ rướn đầu ngửi (mũi phập phồng), rồi cọ má vào tay "Thơm tay bạn ghê~" (hàm nhận biết "giữ yên gần mũi" có test)
- [x] Bàn phím: thêm phím tắt cho chạm mới khi đang chọn Bơ (T = chạm tai, D = đập tay), ghi vào nhãn aria
- [x] Rà soát giai đoạn 59, sửa lỗi tìm được

## Giai đoạn 60 – Đẹp đều mọi bộ lông, rừ rừ ấm hơn (Claude tự thêm, trong hướng mèo/chạm/giọng)
- [x] Chụp các tư thế mới (ngược lông, đập tay, rửa mặt, ngửi, chạm đuôi) với lông tam thể / mèo đen / chế độ tối; sửa chỗ khó nhìn
- [x] Vuốt lâu thì tiếng rừ rừ to dần lên (vuốt ngắn thì nhỏ); điện thoại có rung thì rung rất nhẹ lúc bắt đầu rừ rừ (máy bật giảm chuyển động thì không rung)
- [ ] Rà soát giai đoạn 60, sửa lỗi tìm được

## Để sau (tạm dừng theo HUONG_PHAT_TRIEN.md)
Giai đoạn 45 – Chuyện hỏi thăm rõ ràng hơn (chỉ làm khi Tân báo lỗi liên quan):
- [ ] Xem / xóa "chuyện Bơ định hỏi thăm" trên web (trong "Bơ nhớ gì về mình?"), và báo trong dòng "✓ Bơ đã ghi: sẽ hỏi thăm ..."
- [ ] Người dùng bảo bỏ một lời nhắc mà model chép lại chính lời nhắc đó vào "nhac" trong cùng câu → không tạo lại (chặn bằng code, có test)
- [ ] Mấy ngày liền buồn mà Bơ vẫn chào với vẻ mặt "vui": thử lại bằng API thật 10 lần, siết lời dặn hoặc ép bằng code
- [ ] Rà soát code lần 25, sửa lỗi tìm được


## Sau này
- Giọng trả phí (ElevenLabs/OpenAI) – Tân đã chọn edge-tts miễn phí, chỉ cân nhắc lại nếu Tân yêu cầu
- Phần cứng: mèo robot nhỏ (ESP32 + màn hình mắt + servo đuôi/đầu) dùng chung bộ não
