# Nhật ký tiến độ

## Cách dừng / góp ý (dành cho Tân)
- **Dừng tự chạy:** tạo file tên `STOP` ở thư mục gốc repo (trên github.com: Add file → Create new file → gõ `STOP` → Commit). Xóa file đó để chạy lại. Hoặc nhắn Claude "dừng".
- **Góp ý:** ghi vào file `FEEDBACK.md`, phiên sau Claude sẽ xử lý trước.
- **Lấy bản mới về máy:** `git pull` trong thư mục dự án rồi chạy lại `run.bat`.

## Cần Tân quyết định
- **Dùng Bơ ngoài nhà bằng cách nào?** Tailscale (riêng tư, cần tạo tài khoản miễn phí, cài app trên iPhone) hay Cloudflare Tunnel (link công khai, không cần cài trên điện thoại). Hướng dẫn cả hai trong `DUA_LEN_MANG.md`. Claude khuyên Tailscale. Cách nào cũng phải đặt `APP_PASSWORD`.
- **Ngân sách tháng:** `.env.example` đặt sẵn `MONTHLY_USD_LIMIT=5` (5 đô/tháng). File `.env` cũ của Tân chưa có dòng này nên đang không giới hạn. Tân tự chọn mức và thêm vào `.env`.
- **Phần cứng:** mua linh kiện nào (ESP32 loại nào, màn hình, loa, servo) — cần tiền, Claude không tự làm.
- **Nghe/nói trên thiết bị thật:** ESP32 không tự nhận dạng tiếng Việt được. Cần chọn: (a) điện thoại/máy tính làm "tai" rồi gửi chữ cho thiết bị, hoặc (b) dịch vụ nhận dạng/đọc giọng trả phí. Cần Tân chọn.

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


## 2026-10-10 – Giai đoạn 4: dùng Bơ ngoài nhà
- **Mật khẩu:** đặt `APP_PASSWORD=...` trong `.env` → mở web sẽ hỏi mật khẩu (tên gõ gì cũng được). Để trống thì như cũ.
- **Hướng dẫn** `DUA_LEN_MANG.md`: 2 cách (Tailscale / Cloudflare Tunnel), không cần mở cổng modem. Cần Tân chọn cách (xem mục "Cần Tân quyết định").
- 41 test qua hết.

**Tân cần thử:** đặt `APP_PASSWORD` trong `.env`, chạy lại `run.bat`, mở web xem có hỏi mật khẩu không.

## 2026-10-10 – Giai đoạn 4 xong (báo cáo)
- Làm được: Bơ tự thử lại khi mất mạng + báo lỗi dễ hiểu + nút "Thử lại"; mật khẩu `APP_PASSWORD`; hướng dẫn dùng ngoài nhà `DUA_LEN_MANG.md`.
- Còn lại "dùng thử 1 tuần" là việc của Tân: dùng hằng ngày, ghi điều gì chưa ổn vào `FEEDBACK.md`.
- **Tân cần thử:** tắt Wi-Fi gửi tin xem nút "Thử lại"; đặt mật khẩu; chọn Tailscale hay Cloudflare.

## 2026-10-10 – Giai đoạn 5: giọng nói (bắt đầu)
- Nút **micro** cạnh nút Gửi: nói tiếng Việt, ngừng một chút là tự gửi. Nút **"Giọng nói: bật/tắt"**: Bơ đọc to câu trả lời, miệng mấp máy khi nói. Máy nhớ lựa chọn bật/tắt.
- Dùng tính năng có sẵn của trình duyệt → miễn phí, không cần tài khoản. Giọng hơi "máy"; giọng tự nhiên hơn cần dịch vụ trả phí (để sau, cần Tân quyết định).
- Micro chỉ dùng được trên `localhost` hoặc link `https` (trình duyệt chặn trên `http://192.168...`).
- 42 test qua hết.

**Tân cần thử:** mở http://localhost:8000 trên Chrome/Edge, bật "Giọng nói", bấm micro và nói "chào Bơ".

## 2026-10-10 – Giai đoạn 5: chế độ rảnh tay
- Nút **"Rảnh tay"**: Bơ nghe liên tục, chỉ trả lời khi nghe "Bơ ơi" / "Ê Bơ" (máy nghe nhầm "bờ ới" vẫn nhận). Gọi "Bơ ơi" rồi ngừng → mặt Bơ ngạc nhiên, chờ 8 giây cho câu tiếp theo. Nói "quả bơ" thì không bị đánh thức.
- Lúc Bơ đang đọc câu trả lời thì tạm ngừng nghe để không tự nghe giọng mình.
- Hiện chỉ hoạt động khi tab web đang mở (trình duyệt không cho nghe ngầm). Phần cứng sau này sẽ làm thật.
- 44 test qua hết (test từ đánh thức cần Node.js, máy không có thì tự bỏ qua).

**Tân cần thử:** Chrome/Edge trên máy tính → bật "Giọng nói" và "Rảnh tay", nói "Bơ ơi, kể chuyện vui đi".

## 2026-10-10 – Giai đoạn 5 xong (báo cáo): giọng nói
- Khi đọc to, Bơ bỏ emoji, ký hiệu (`**`, `#`), đường link, ":)" → không còn đọc "mặt cười" hay "sao sao". Chữ trên màn hình vẫn giữ nguyên.
- Nút **"Tốc độ đọc: vừa / nhanh / chậm"** (hiện khi bật Giọng nói), máy nhớ lựa chọn.
- Cả giai đoạn: micro, đọc to, rảnh tay "Bơ ơi", dọn chữ, chỉnh tốc độ. Tất cả miễn phí, chạy trong trình duyệt.
- 45 test qua hết.

**Tân cần thử:** bật Giọng nói, bấm "Tốc độ đọc" vài lần nghe thử; chat câu nào Bơ trả lời có emoji xem đọc có mượt không.

## 2026-10-10 – Giai đoạn 6 xong (báo cáo): chuẩn bị phần cứng
- **Cổng thiết bị:** `POST /api/thiet-bi/chat` (gửi chữ, nhận `{noi, cam_xuc, hanh_dong}`) và `POST /api/thiet-bi/chao` (Bơ mở lời hỏi thăm). Bảo vệ bằng khóa riêng `DEVICE_KEY` trong .env; để trống = tắt.
- `?khong_dau=1` → bỏ dấu tiếng Việt và emoji cho màn hình nhỏ ("Chào Tân" → "Chao Tan").
- `THIET_BI.md`: cách gọi, bảng cảm xúc → mặt, hành động → servo, khung code ESP32 (chưa thử trên máy thật).
- 50 test qua hết.

**Tân cần thử (không cần phần cứng):** đặt `DEVICE_KEY=thu123` trong .env, chạy lại, rồi gõ lệnh `curl` trong THIET_BI.md (đổi IP thành `localhost`).

## 2026-10-10 – Giai đoạn 7: theo dõi chi phí
- Mỗi câu gọi API được ghi số token (chat, tóm tắt, gộp trí nhớ). Nút **"Chi phí"** trên web hiện: hôm nay, tháng này (đô la + quy ra tiền Việt ước chừng), và số câu Bơ đã trả lời so với giới hạn ngày.
- Giá dùng để tính đặt trong .env (`PRICE_INPUT_PER_MTOK=1`, `PRICE_OUTPUT_PER_MTOK=5`, theo giá Haiku Claude biết). Tân nên so với trang giá Anthropic và số tiền thật trên console.
- 52 test qua hết.

**Tân cần thử:** chat vài câu rồi bấm "Chi phí".

## 2026-10-10 – Giai đoạn 7: sao lưu trí nhớ
- Trong "Bơ nhớ gì về mình?" có **"Tải bản sao lưu"** (file `bo-sao-luu-NGÀY.json`: tin nhắn, tóm tắt, điều đáng nhớ, chuyện cần hỏi thăm) và **"Nạp bản sao lưu"** (thay toàn bộ trí nhớ hiện tại, có hỏi lại trước).
- File hỏng/không phải của Bơ → báo lỗi, trí nhớ cũ giữ nguyên.
- Dùng khi đổi máy tính, hoặc trước khi thử nghiệm gì đó.
- 54 test qua hết.

**Tân cần thử:** tải bản sao lưu, xóa 1 điều Bơ nhớ, rồi nạp lại file xem điều đó quay lại không.

## 2026-10-10 – Giai đoạn 7: giờ tin nhắn + tin cũ
- Mỗi tin nhắn có giờ nhỏ bên dưới ("14:05", "hôm qua 21:30", "08/10/2026 09:00").
- Mở web hiện 50 tin gần nhất; kéo lên đầu thì tự tải thêm 50 tin cũ hơn, không bị nhảy chỗ đang đọc.
- 55 test qua hết.

## 2026-10-10 – Giai đoạn 7 xong (báo cáo): tiện ích
- Bộ chấm điểm tính cách thêm 2 tình huống (tổng 12): Bơ có ghi lại "chiều nay đi phỏng vấn" để hỏi sau không; Bơ có tự hỏi "hôm qua tập chân sao rồi?" khi được chào không.
- Cả giai đoạn: nút Chi phí, sao lưu/khôi phục trí nhớ, giờ tin nhắn + tải tin cũ, thêm tình huống chấm điểm.
- 57 test qua hết.

**Tân cần thử:** `python -m app.thu_tinh_cach` (12 câu API) và gửi tổng điểm vào FEEDBACK.md.

## 2026-10-10 – Giai đoạn 8: gửi cùng lúc
- Hai tin tới cùng lúc (ví dụ điện thoại và máy tính) thì Bơ trả lời lần lượt, lịch sử không bị xen lẫn.
- 58 test qua hết.

## 2026-10-10 – Giai đoạn 8: ngân sách tháng
- `MONTHLY_USD_LIMIT` trong .env: tiêu (ước tính) tới mức này thì Bơ báo "hết ngân sách" và nghỉ tới tháng sau, không gọi API nữa. 0 = không giới hạn.
- Nút "Chi phí" hiện thêm ngân sách tháng và đã dùng bao nhiêu %.
- 59 test qua hết.

**Tân cần thử:** thêm dòng `MONTHLY_USD_LIMIT=5` (hoặc mức Tân muốn) vào `.env`.

## 2026-10-10 – Giai đoạn 8: tự kiểm tra cấu hình
- Mở web mà thiếu API key / thiếu persona.md / không ghi được dữ liệu → hiện ngay dòng đỏ giải thích, ví dụ "API key: Chưa có ANTHROPIC_API_KEY trong .env".
- Xem chi tiết ở http://localhost:8000/api/suc-khoe (có cả cảnh báo nhẹ: chưa đặt mật khẩu, chưa đặt ngân sách). Không tốn tiền API.
- 61 test qua hết.

## 2026-10-10 – Giai đoạn 8: biểu tượng trên màn hình chính
- Bơ có biểu tượng mặt cười vàng. Trên iPhone: Safari → Chia sẻ → "Thêm vào MH chính" → mở như ứng dụng, toàn màn hình.
- 62 test qua hết.

**Tân cần thử:** thêm Bơ vào màn hình chính iPhone (chung Wi-Fi), mở từ biểu tượng.

## 2026-10-10 – Giai đoạn 8 xong (báo cáo): nhắc việc
- Nhắn "8h tối nhắc mình gọi mẹ" → Bơ ghi lời nhắc (mục nội bộ `nhac` trong JSON). Tới giờ Bơ tự nhắn "Tới giờ rồi nè: gọi mẹ!", vẫy tay, đọc to nếu bật giọng. Có thông báo của trình duyệt nếu Tân cho phép và đang ở tab khác. Nhắc không tốn câu API.
- Xem/xóa lời nhắc sắp tới trong "Bơ nhớ gì về mình?". Lời nhắc có trong file sao lưu. Thiết bị hỏi qua `/api/thiet-bi/nhac`.
- Giới hạn: chỉ nhắc khi máy tính đang chạy Bơ và web đang mở.
- Cả giai đoạn 8: xử lý 2 tin cùng lúc, ngân sách tháng, tự kiểm tra cấu hình, biểu tượng màn hình chính, nhắc việc.
- 67 test qua hết.

**Tân cần thử:** nhắn "2 phút nữa nhắc mình uống nước", để yên trang web, chờ Bơ nhắc.

## 2026-10-10 – Giai đoạn 9: rà soát lỗi (review độc lập) và sửa
- **Bảo mật:** trước đây một trang web lạ mở trên cùng máy có thể lén gửi lệnh xóa sạch trí nhớ của Bơ. Giờ mọi lệnh thay đổi dữ liệu phải có header `X-Bo` mà trang lạ không gắn được; nạp sao lưu chỉ nhận JSON.
- **Nhắc việc:** nhắc trễ (lúc đó không mở web) thì nói rõ "Lúc 20:00 bạn nhờ Bơ nhắc… Trễ rồi nhưng vẫn nhắc"; lời nhắc không còn làm Bơ quên hỏi thăm.
- **Nhanh hơn:** tóm tắt/gộp trí nhớ chạy sau khi đã trả lời, không bắt chờ → bớt cảnh trình duyệt hết giờ chờ rồi bấm "Thử lại" bị gửi 2 lần.
- **Đọc JSON chắc hơn:** AI lỡ viết thêm chữ sau JSON, hoặc JSON bị cắt, thì vẫn lấy đúng câu nói, không hiện cả đống ký hiệu.
- **Giọng nói:** sửa lỗi rảnh tay bật micro lại khi Bơ còn đang nói; tắt rảnh tay không còn tự gửi chữ đang gõ dở; nút micro không bị kẹt sau lỗi quyền micro.
- **Sao lưu:** nạp sao lưu không bị việc khác ghi xen vào; file thiếu giờ vẫn nạp đúng.
- 74 test qua hết.
