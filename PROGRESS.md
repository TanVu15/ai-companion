# Nhật ký tiến độ

## Cách dừng / góp ý (dành cho Tân)
- **Dừng tự chạy:** tạo file tên `STOP` ở thư mục gốc repo (trên github.com: Add file → Create new file → gõ `STOP` → Commit). Xóa file đó để chạy lại. Hoặc nhắn Claude "dừng".
- **Góp ý:** ghi vào file `FEEDBACK.md`, phiên sau Claude sẽ xử lý trước.
- **Lấy bản mới về máy:** `git pull` trong thư mục dự án rồi chạy lại `run.bat`.

## Tóm tắt nhanh lần chạy 2026-10-10 (19:39–20:20 UTC)
Xong giai đoạn 13 → 23 (128 test qua hết, 6 lượt rà soát độc lập đã sửa lỗi). Đáng thử nhất:
1. `git pull`, nhấp đúp `run.bat`. Bấm nút **"?"**: xem tình trạng, đổi màu mặt Bơ, xem mẹo dùng.
2. **Nhắc lặp lại:** "mỗi ngày 9h tối nhắc mình đánh răng"; lời nhắc tới có nút "Nhắc lại sau 10 phút".
3. **Sinh nhật:** "sinh nhật mình 5/3" → đúng ngày Bơ chúc. Tối Chủ nhật Bơ **tổng kết tuần**.
4. **Tìm** chuyện cũ (gõ không dấu, Ctrl+K), chạm vào tin để **ghim**.
5. **Tính cách**: sửa thẳng trên web; "Về mặc định" nếu lỡ hỏng.
6. **Thời tiết**: thêm `THANH_PHO=Da Nang` (thành phố của Tân) vào `.env` — miễn phí.
7. "Bơ nhớ gì về mình?": tự thêm/sửa điều Bơ nhớ, có "Hoàn tác"; tải trò chuyện (.txt).
Gặp lỗi: xem `SU_CO.md`, gửi mấy dòng cuối `data/loi.log` vào `FEEDBACK.md`.

## Tóm tắt lần chạy trước (18:44–19:21 UTC)
Xong giai đoạn 3 → 12: hỏi thăm chuyện cũ, nhắc việc, giọng nói + rảnh tay, chi phí + ngân sách, iPhone màn hình chính.

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

## 2026-10-10 – Giai đoạn 9: tách code giao diện
- Phần chạy của web chuyển từ `web/index.html` sang `web/app.js` (index.html chỉ còn khung + màu sắc). Trình duyệt luôn lấy bản mới sau khi `git pull`.
- 74 test qua hết.

## 2026-10-10 – Giai đoạn 9 xong (báo cáo)
- Bơ biết thứ trong tuần và buổi: "23:30 (khuya), thứ Bảy" → có thể hỏi "khuya rồi sao chưa ngủ?", "cuối tuần đi chơi đâu?".
- Cả giai đoạn: review độc lập tìm ra 10 lỗi, đã sửa hết các lỗi quan trọng; tách code giao diện; Bơ biết thứ/buổi.
- 75 test qua hết.

**Tân cần thử:** nhắn Bơ lúc khuya hoặc cuối tuần xem câu chào có hợp lúc không.

## 2026-10-10 – Giai đoạn 10: test tự động trên GitHub
- Mỗi lần có code mới trên GitHub, test tự chạy (tab "Actions" trên trang repo). Dấu ✓ xanh = ổn, ✗ đỏ = có lỗi.
- Ghi chú: có một commit lúc 19:09 lỡ đẩy lên khi 1 test cũ chưa sửa; 20 giây sau đã sửa. Từ giờ Claude chỉ commit khi test xanh (chạy test và commit chung một lệnh).

## 2026-10-10 – Giai đoạn 10: nhật ký lỗi
- Lỗi (mất mạng, sai key, tóm tắt hỏng...) được ghi vào `data/loi.log`: giờ, loại lỗi, vị trí trong code. **Không** ghi nội dung tin nhắn hay API key. Tự giới hạn tối đa ~3 MB.
- Gặp sự cố: mở file đó, chép mấy dòng cuối vào FEEDBACK.md.
- 76 test qua hết.

## 2026-10-10 – Giai đoạn 10 xong (báo cáo)
- `SU_CO.md`: bảng 17 sự cố hay gặp (run.bat tắt ngay, sai key, hết tiền, iPhone không vào được, không thấy micro, lời nhắc không kêu…) và cách sửa; cuối cùng là cách gửi `data/loi.log` vào FEEDBACK.md.
- Cả giai đoạn: test tự chạy trên GitHub (lần đầu đã ✓ xanh), nhật ký lỗi, hướng dẫn sự cố.
- **Lưu ý khi `git pull`:** chỉ cần tắt và chạy lại `run.bat`.

## 2026-10-10 – Giai đoạn 11: khuôn mặt sống động
- Cảm xúc được lưu cùng tin nhắn → tải lại web, Bơ vẫn giữ vẻ mặt lúc nói câu cuối (dữ liệu cũ tự nâng cấp, không mất gì).
- 3 phút không ai chạm/gõ → Bơ nhắm mắt "ngủ gật" (có "z z", thở nhẹ). Chạm, gõ hoặc Bơ nói là tỉnh. Sau này màn hình phần cứng cũng có thể làm vậy.
- 78 test qua hết.

**Tân cần thử:** để yên trang web 3 phút xem Bơ ngủ gật, rồi chạm vào.

## 2026-10-10 – Giai đoạn 12: nhắn như người thật
- Câu trả lời dài (từ 60 ký tự, nhiều câu) được tách thành 2–3 bong bóng; giữa các bong bóng có ba chấm nhảy "Bơ đang gõ". Câu siêu ngắn ("Ừa.") gộp với câu sau. Số như "3.5 triệu" không bị tách.
- Chỉ đổi cách hiện; bộ não và JSON giữ nguyên, Bơ vẫn đọc to cả câu một lần.
- 79 test qua hết.

## 2026-10-10 – Giai đoạn 12: "lâu quá không gặp"
- 2 ngày trở lên không nói chuyện, mở web là Bơ tự chào kiểu bạn thân lâu không gặp (tốn 1 câu API). Đổi số ngày bằng `GREET_MISS_DAYS` trong .env, 0 = tắt.
- Sửa lỗi nhỏ do lượt trước gây ra: nếu Tân không trả lời lời chào, mở lại web Bơ có thể chào lặp lại. Giờ lời chào cũng tính là "vừa nói chuyện"; chỉ lời nhắc tự động là không tính.
- 82 test qua hết.

## 2026-10-10 – Rà soát lần 2 và sửa
- **iPhone/iPad đời cũ** (Safari < 16.4) không chạy được web vì một biểu thức tách câu mới → đã viết lại cách tách cho máy cũ hiểu.
- Lời nhắc / lời chào / câu trả lời giờ xếp hàng, không chen vào giữa các bong bóng của nhau.
- Xóa một điều Bơ nhớ đúng lúc Bơ đang gộp trí nhớ → trước đây điều đó có thể quay lại; giờ không.
- Việc nền (tóm tắt, gộp) không còn bắt tin nhắn mới phải chờ.
- 84 test qua hết.

## 2026-10-10 – run.bat tự cập nhật thư viện
- Mỗi lần chạy, `run.bat` kiểm tra và cài thư viện còn thiếu (nhanh nếu đã đủ). Sau `git pull` không cần xóa `.venv` nữa.
- `run.bat` được lưu với kiểu xuống dòng của Windows (file `.gitattributes`).
- Chưa thử trên Windows thật (máy của Claude chạy Linux) → **Tân cần thử:** `git pull` rồi nhấp đúp `run.bat`.

## 2026-10-10 – Giai đoạn 12 xong (báo cáo)
- Chạm vào mặt Bơ lúc đang đọc to → Bơ im ngay (rảnh tay thì nghe tiếp).
- Cả giai đoạn: bong bóng + ba chấm đang gõ, chào khi lâu không gặp, chạm để im.
- 84 test qua hết, test trên GitHub đều xanh.

**Tiếp theo (lần chạy sau):** các việc phần mềm lớn đã xong. Lần sau ưu tiên góp ý trong FEEDBACK.md; nếu chưa có góp ý thì tiếp tục rà soát/đánh bóng nhỏ, không thêm tính năng tốn tiền.

## 2026-10-10 – Giai đoạn 13: tìm trong chuyện cũ
- Nút **"Tìm"** dưới khuôn mặt: gõ vài chữ, hiện các tin nhắn có chữ đó (mới nhất trước, tối đa 30), chỗ khớp tô vàng.
- Gõ không dấu vẫn ra: "da bong" tìm được "Đá bóng". Không tốn câu API nào.
- 85 test qua hết.

**Tân cần thử:** bấm "Tìm", gõ một chữ đã từng nhắn với Bơ.


## 2026-10-10 – Giai đoạn 13: ngày đặc biệt
- Kể "sinh nhật mình 5/3" hay "kỷ niệm ngày cưới 1/12" → Bơ ghi lại (mục nội bộ `ngay_dac_biet`, giao diện không thấy). Lặp lại mỗi năm; 29/02 thì năm không nhuận chúc vào 28/02.
- Đúng ngày: mở web là Bơ chủ động chúc (dù vừa nói chuyện), hoặc chúc ngay trong câu trả lời đầu tiên của ngày. Mỗi năm chúc một lần.
- Xem/xóa trong "Bơ nhớ gì về mình?" → mục "Ngày đặc biệt". Có trong file sao lưu.
- 92 test qua hết.

**Tân cần thử:** nhắn "sinh nhật mình là ngày <ngày mai>", bấm "Bơ nhớ gì về mình?" xem đã có chưa; mai mở web xem Bơ có chúc không.

## 2026-10-10 – Giai đoạn 13 xong (báo cáo): xem lại chuyện cũ
- **Tìm:** nút "Tìm" dưới khuôn mặt, gõ không dấu vẫn ra, chỗ khớp tô vàng.
- **Ngày đặc biệt:** kể sinh nhật/kỷ niệm → đúng ngày Bơ chúc (mỗi năm một lần). Xem/xóa trong "Bơ nhớ gì về mình?".
- **Tải trò chuyện (.txt):** trong "Bơ nhớ gì về mình?" → "Tải trò chuyện (.txt)", chia theo ngày, mở bằng Notepad đọc được tiếng Việt.
- Cả ba không tốn thêm câu API nào. 94 test qua hết.

**Tân cần thử:** bấm "Tìm"; kể "sinh nhật mình <ngày mai>" rồi mai mở web; tải file .txt mở bằng Notepad.

## 2026-10-10 – Giai đoạn 14: lời nhắc lặp lại
- Nhắn "7h sáng mỗi ngày nhắc mình uống nước" hay "tối thứ Hai hằng tuần 8h nhắc mình họp nhóm" → Bơ nhắc đều đặn (mục `lap` trong lời nhắc: `ngay` / `tuan`).
- Nói lúc 9h mà giờ nhắc là 7h → lần đầu là 7h sáng mai. Tắt máy mấy ngày → mở lại chỉ nhắc 1 lần (không dồn), rồi hẹn lần kế tiếp.
- Trong "Bơ nhớ gì về mình?" lời nhắc lặp có ghi "(mỗi ngày)"/"(mỗi tuần)"; bấm "Xóa" là thôi nhắc. File `.db` cũ tự thêm cột mới, không mất gì.
- 97 test qua hết.

**Tân cần thử:** nhắn "mỗi ngày 9h tối nhắc mình đánh răng", mở "Bơ nhớ gì về mình?" xem có dòng "(mỗi ngày)".

## 2026-10-10 – Giai đoạn 14: nhắc lại sau 10 phút
- Dưới mỗi lời nhắc vừa tới giờ có nút **"Nhắc lại sau 10 phút"**. Bấm là Bơ hẹn lại, hiện "Ok, 10 phút nữa Bơ nhắc lại". Không tốn câu API.
- `/api/nhac` (và cổng thiết bị) trả thêm mục `viec` = việc gốc, để nút biết nhắc lại việc gì.
- 98 test qua hết.

**Tân cần thử:** nhắn "1 phút nữa nhắc mình uống nước", chờ lời nhắc, bấm "Nhắc lại sau 10 phút".

## 2026-10-10 – Giai đoạn 14 xong (báo cáo): rà soát lần 3 + sửa lỗi
Một lượt review độc lập phần mới (tìm, ngày đặc biệt, lời nhắc lặp, nhắc lại sau). Không có lỗi nặng; đã sửa 7 lỗi vừa/nhỏ:
- Lời nhắc lặp bị AI ghi 2 lần (khác ngày bắt đầu) → trước đây sẽ nhắc 2 lần mỗi ngày mãi mãi; giờ coi là trùng.
- Trả lời đúng lúc qua nửa đêm có thể đánh dấu "đã chúc" nhầm sinh nhật của ngày mới.
- Lời nhắc tự động không còn bị tính vào giới hạn số câu/ngày.
- Cổng thiết bị `?khong_dau=1` bỏ dấu cả mục `viec`; "nhắc lại sau 10 phút" không còn thành 9 phút; tìm/tải chat không đọc dữ liệu giữa lúc đang nạp sao lưu; tô vàng đúng cả chữ gõ trên máy Mac.
- 102 test qua hết.

**Tân cần thử:** như các mục giai đoạn 14 ở trên.

## 2026-10-10 – Giai đoạn 15: nút "?" – Bơ làm được gì
- Nút **"?"** dưới khuôn mặt: liệt kê ngắn các việc Bơ làm được (nhớ chuyện, hỏi thăm, nhắc việc, ngày đặc biệt, giọng nói, tìm, sao lưu, chi phí). Không tốn API.
- 103 test qua hết.

## 2026-10-10 – Giai đoạn 15: ghim tin nhắn
- Chạm vào một tin nhắn → nút **"Ghim tin này"** (chạm lần nữa để ẩn). Tin đã ghim có viền vàng và chữ "đã ghim".
- Xem lại: bấm "Tìm" khi chưa gõ gì → danh sách tin đã ghim. Có trong file sao lưu.
- `/api/chat` trả thêm `id` (để web ghim được tin vừa nói); cổng thiết bị vẫn chỉ trả `{noi, cam_xuc, hanh_dong}`.
- 104 test qua hết.

**Tân cần thử:** chạm vào một câu hay của Bơ → "Ghim tin này" → bấm "Tìm".

## 2026-10-10 – Giai đoạn 15 xong (báo cáo): bạn đồng hành
- **Nút "?"**: liệt kê những việc Bơ làm được.
- **Ghim tin nhắn**: chạm vào tin → "Ghim tin này"; xem lại ở nút "Tìm".
- **Tổng kết tuần**: tối Chủ nhật (từ 17h) mở web, nếu tuần đó có nói chuyện (≥5 tin), Bơ chủ động điểm lại 2–3 chuyện đáng nhớ và hỏi dự định tuần tới. Mỗi tuần một lần, tốn 1 câu API. Tắt bằng `WEEKLY_RECAP=0` trong `.env`.
- 107 test qua hết.

**Tân cần thử:** tối Chủ nhật này mở web xem Bơ điểm lại tuần; chạm vào một tin để ghim.

## 2026-10-10 – Giai đoạn 16: thêm tình huống chấm điểm
- `tinh_huong.json` có 15 tình huống (thêm: kể ngày sinh nhật → phải ghi ngày; đúng ngày sinh nhật → phải chúc; "mỗi ngày 7h nhắc uống nước" → phải ghi nhắc lặp `ngay`).
- Chạy `python -m app.thu_tinh_cach` (tốn ~15 câu API) để xem Bơ thật có làm đúng không.
- 108 test qua hết.

## 2026-10-10 – Giai đoạn 16: Bơ và bạn
- Mở nút **"?"**: dòng đầu cho biết đã quen bao nhiêu ngày (từ ngày nào), trò chuyện bao nhiêu ngày, bao nhiêu tin nhắn, Bơ đang nhớ bao nhiêu điều. Không tốn API.
- 109 test qua hết.

## 2026-10-10 – Giai đoạn 16 xong (báo cáo): rà soát lần 4
- Thêm tình huống chấm điểm (sinh nhật, nhắc mỗi ngày), thống kê "Bơ và bạn" trong nút "?", README cập nhật đủ tính năng mới.
- Rà soát độc lập phần ghim/tổng kết tuần: không có lỗi nặng. Đã sửa: lời nhắc vừa tới giờ ghim được ngay (trước phải tải lại trang); sao lưu/thống kê/tin đã ghim không đọc dữ liệu dở dang khi đang nạp sao lưu; cổng thiết bị (chào, nhắc) vẫn chỉ trả các mục gọn như cũ.
- (Đã sửa ở giai đoạn 17: tổng kết tuần/sinh nhật giờ được kiểm tra cả khi trang đang mở.)
- 110 test qua hết.

## 2026-10-10 – Giai đoạn 17: sửa tính cách trên web
- Nút **"Tính cách"** dưới khuôn mặt: hiện tính cách đang dùng, sửa thẳng rồi "Lưu" → áp dụng từ tin nhắn sau, không cần khởi động lại.
- Bản tự sửa lưu ở `data/persona.md` (không lên GitHub, `git pull` không đè). Bản trước đó giữ ở `data/persona.md.truoc`. "Về mặc định" dùng lại `persona.md` gốc.
- Chặn tính cách quá ngắn (<20 ký tự) hoặc quá dài (>20.000 ký tự, vì gửi kèm mỗi câu sẽ tốn tiền).
- 113 test qua hết.

**Tân cần thử:** bấm "Tính cách", thêm dòng "Gọi mình là đại ca", Lưu, rồi nhắn "hello".

## 2026-10-10 – Giai đoạn 17: dịp đặc biệt khi trang đang mở
- Để trang Bơ mở lâu (qua nửa đêm sinh nhật, qua 17h Chủ nhật): mỗi 10 phút web hỏi máy chủ "có dịp gì không" (`/api/chao?chi_dip=1`). Có thì Bơ tự chúc/điểm lại tuần; không có thì không tốn câu API nào. Hỏi thăm chuyện thường vẫn chỉ khi mở web.
- 114 test qua hết.

## 2026-10-10 – Giai đoạn 17 xong (báo cáo): tự tay chỉnh Bơ
- **Sửa tính cách trên web** (nút "Tính cách"), **dịp đặc biệt khi trang đang mở** (mỗi 10 phút, không tốn API nếu không có dịp).
- **Màn hình điện thoại nhỏ** (chụp tự động ở cỡ iPhone SE 320×568): không bị tràn ngang. Đã sửa: mặt Bơ thu nhỏ trên màn hình thấp để còn chỗ cho tin nhắn; hộp "Tính cách" trước bị che mất nút Lưu, giờ hiện đủ.
- 114 test qua hết.

**Tân cần thử:** mở Bơ trên iPhone, bấm "Tính cách" xem có thấy nút "Lưu" không.

## 2026-10-10 – Giai đoạn 18: Bơ biết thời tiết
- Thêm `THANH_PHO=Da Nang` (hoặc thành phố của Tân) vào `.env` rồi chạy lại `run.bat` → mỗi câu Bơ biết "bây giờ 30°C, mưa nhẹ; hôm nay 24–31°C, khả năng mưa 80%; ngày mai...". Bơ chỉ nhắc khi hợp chuyện (ví dụ Tân nói sắp ra ngoài).
- Dùng Open-Meteo: miễn phí, không cần tài khoản/key. Hỏi tối đa 1 lần/giờ. Mất mạng thì Bơ vẫn nói chuyện bình thường. Để trống `THANH_PHO` = tắt.
- Thêm ~40 chữ vào mỗi câu hỏi gửi AI (chi phí tăng không đáng kể).
- Máy làm việc của Claude không vào được Open-Meteo nên chỉ test bằng dữ liệu giả → Tân thử thật giúp.
- 119 test qua hết.

**Tân cần thử:** thêm `THANH_PHO=...` vào `.env`, chạy lại, nhắn "chiều nay mình đi chơi nè" xem Bơ có nhắc thời tiết không.

## 2026-10-10 – Giai đoạn 18: tình trạng trong nút "?"
- Nút "?" có thêm mục **Tình trạng**: API key, tính cách đang dùng (mặc định hay bản tự sửa), dữ liệu, mật khẩu, ngân sách, thời tiết (lấy được chưa, sai tên thành phố thì báo). Kiểm tra không gọi mạng, không tốn tiền.
- 120 test qua hết.

## 2026-10-10 – Giai đoạn 18 xong (báo cáo): rà soát lần 5
- Thời tiết, nút "?" có Tình trạng, và sửa lỗi sau rà soát độc lập:
  - **Quan trọng:** bản tính cách tự sửa đổi tên thành `data/persona_tu_sua.md` và luôn tính theo thư mục dự án → không bao giờ đè/xóa nhầm `persona.md` gốc (trước đây có thể xảy ra nếu đặt `DB_PATH` lạ).
  - Lưu tính cách "một phát" (không có lúc file trống), giữ 10 bản trước có ngày giờ thay vì 1 bản `.truoc`.
  - Lấy thời tiết ngoài khóa: mạng chậm không làm kẹt lời nhắc hay máy khác.
  - Hỏi dịp đặc biệt 10 phút/lần: bỏ qua khi tab đang ẩn hoặc Bơ đang đọc to (không chúc vào phòng trống, không cắt lời).
  - Dữ liệu thời tiết lạ không làm mất cả bản tin.
- 124 test qua hết.

**Tân cần thử:** nếu đã lỡ sửa tính cách trên web (bản cũ ở `data/persona.md`), mở nút "Tính cách" dán lại rồi Lưu.

## 2026-10-10 – Giai đoạn 19: chọn giọng đọc
- Bật "Giọng nói" mà máy có từ 2 giọng tiếng Việt trở lên (Windows thường có "An" + "HoaiMy" nếu cài thêm gói giọng, Edge có nhiều giọng online) → hiện nút **"Giọng: ..."**. Bấm để đổi sang giọng kế tiếp, Bơ đọc thử, máy nhớ lựa chọn.
- 125 test qua hết.

**Tân cần thử:** mở bằng Edge, bật "Giọng nói", bấm "Giọng: ..." vài lần chọn giọng dễ nghe nhất.

## 2026-10-10 – Giai đoạn 19: màu mặt Bơ
- Nút "?" → mục **Màu mặt Bơ**: vàng (mặc định), xanh bơ, hồng, xanh dương, cam, tím. Mỗi máy nhớ màu riêng.

## 2026-10-10 – Giai đoạn 19 xong (báo cáo): cá nhân hóa giao diện
- Chọn giọng đọc, chọn màu mặt Bơ, phím tắt (Esc: Bơ ngừng đọc; Ctrl+K: tìm). Tất cả lưu trên từng máy, không tốn API.
- 125 test qua hết.

**Tân cần thử:** nút "?" → đổi màu mặt; trên máy tính bấm Ctrl+K.

## 2026-10-10 – Giai đoạn 20: tự thêm / sửa điều Bơ nhớ
- "Bơ nhớ gì về mình?" có ô **Thêm** (gõ điều muốn Bơ nhớ) và nút **Sửa** cạnh mỗi điều (sửa chữ, giữ nguyên vị trí). Trùng điều khác thì báo, không lưu.
- 126 test qua hết.

**Tân cần thử:** thêm "Mình thích ăn phở", rồi hỏi Bơ "mình thích ăn gì?".

## 2026-10-10 – Giai đoạn 20 xong (báo cáo): quản lý trí nhớ + gọn code
- Tự thêm/sửa điều Bơ nhớ (xem mục trên).
- `web/app.js` (600 dòng) tách thành 4 file theo chức năng: `app.js` (khung chat), `giong_noi.js`, `khoi_dong.js`, `hop_thoai.js`. Chạy y như cũ (đã thử tự động trên trình duyệt: gửi tin, ghim, tìm, nhắc lại, các hộp thoại — không lỗi).
- 126 test qua hết.

## 2026-10-10 – Giai đoạn 21: rà soát lần 6
- Rà soát độc lập phần giọng đọc, màu mặt, phím tắt, sửa điều nhớ, tách file JS: không lỗi nặng. Đã sửa:
  - Nút "Gửi" chỉ bật khi đã tải xong mọi file JS (mạng chậm mà gửi sớm thì trước đây mất câu trả lời của Bơ).
  - Ctrl+K không còn chen khi đang gõ dấu tiếng Việt hoặc khi hộp khác đang mở.
  - Nút chọn giọng hiện được trên Safari cũ.
- 126 test qua hết.

## 2026-10-10 – Giai đoạn 21: chi phí chi tiết
- Nút "Chi phí" có thêm: tháng này tốn bao nhiêu cho **trò chuyện / tóm tắt chuyện cũ / gộp trí nhớ**, và số câu gọi API **từng ngày trong 7 ngày gần nhất**.
- 127 test qua hết.

## 2026-10-10 – Giai đoạn 21 xong (báo cáo)
- Rà soát lần 6 + sửa lỗi; chi phí chi tiết; **Hoàn tác**: lỡ xóa một điều Bơ nhớ thì trong 10 giây bấm "Hoàn tác" để Bơ nhớ lại.
- 127 test qua hết.

**Tân cần thử:** mở "Chi phí" xem bảng 7 ngày; xóa thử một điều rồi bấm "Hoàn tác".

## 2026-10-10 – Giai đoạn 22: gợi ý câu mở đầu
- Lần đầu mở (chưa có tin nhắn nào): hiện 4 câu gợi ý ("Chào Bơ! Mình tên là ...", "Kể mình nghe chuyện gì vui đi", "8h tối nay nhắc mình gọi mẹ nha"...). Bấm là gửi (câu giới thiệu tên thì để Tân gõ tiếp). Gửi tin đầu tiên là gợi ý biến mất.
- 127 test qua hết.

## 2026-10-10 – Giai đoạn 22: giờ yên lặng
- Mặc định 23h–6h (`GIO_YEN_LANG=23-6` trong `.env`, để trống = tắt): lời nhắc, lời chào, chúc mừng mà Bơ **tự** nói thì chỉ hiện chữ, không đọc to (không làm giật mình ban đêm). Câu trả lời khi Tân hỏi vẫn đọc bình thường.
- 128 test qua hết.

## 2026-10-10 – Giai đoạn 22 xong (báo cáo): dễ làm quen
- Gợi ý câu mở đầu, giờ yên lặng ban đêm, `SU_CO.md` thêm cách xử lý: tính cách tự sửa bị lạ, thời tiết, giọng đọc, giờ yên lặng, màu mặt.
- 128 test qua hết.

## 2026-10-10 – Giai đoạn 23 xong (báo cáo): không mất chữ
- Đang gõ dở mà lỡ tải lại trang / tắt trình duyệt → mở lại chữ vẫn còn trong ô nhập (lưu trên máy này).
- Gửi tin bị lỗi (mất mạng) → tin được giữ lại; lỡ tải lại trang thì tin nằm sẵn trong ô nhập, bấm Gửi là xong.
- Đã thử tự động trên trình duyệt (giả lập mất mạng). 128 test qua hết.

## 2026-10-10 – Giai đoạn 24: tâm trạng
- Mỗi tin Tân gửi, Bơ đoán tâm trạng (vui / bình thường / buồn / mệt / lo / bực) — mục nội bộ `tam_trang` trong JSON, giao diện không bị ảnh hưởng, không tốn thêm câu API.
- Nút **"?"** có dải **"Tâm trạng của bạn 7 ngày qua"**: mỗi ngày một biểu tượng (😊 🙂 😢 😩 😟 😠), ngày không nói chuyện là dấu chấm.
- Trong 3 ngày gần đây có ít nhất 2 ngày buồn/mệt/lo/bực → Bơ được dặn quan tâm nhẹ nhàng hơn, không gặng hỏi.
- Dữ liệu nằm trong máy (data/), có trong bản sao lưu. 136 test qua hết.

**Tân cần thử:** nhắn "hôm nay mệt quá", rồi bấm "?" xem dải tâm trạng.

## 2026-10-10 – Giai đoạn 24: nhắc trước ngày đặc biệt
- Hôm trước ngày đặc biệt (sinh nhật mẹ, kỷ niệm...), lần đầu Tân mở web từ 8h sáng (hoặc web đang mở sẵn), Bơ chủ động nhắc: "Mai sinh nhật mẹ đó, chuẩn bị quà chưa?". Mỗi năm nhắc 1 lần, tốn 1 câu API.
- Đúng ngày vẫn chúc như cũ. 139 test qua hết.

**Tân cần thử:** kể Bơ một ngày đặc biệt rơi vào ngày kia (ví dụ "sinh nhật mẹ mình 12/10"), ngày mai mở web xem Bơ có nhắc không. (Kể ngày mai luôn thì Bơ không nhắc lại, vì Tân vừa nói xong.)

## 2026-10-10 – Giai đoạn 24 xong (báo cáo): hiểu tâm trạng
- Rà soát lần 7 (độc lập) phần mới, không lỗi nặng. Đã sửa:
  - Tân vừa kể "mai sinh nhật mẹ" thì Bơ không nhắc trước lại vài phút sau nữa.
  - Hôm nay Tân đã vui lại thì Bơ thôi "nhẹ nhàng" kiểu an ủi.
- Cả giai đoạn: Bơ đoán tâm trạng mỗi tin + dải "Tâm trạng 7 ngày" (nút "?"); mấy hôm buồn/mệt thì Bơ quan tâm hơn; nhắc trước ngày đặc biệt 1 ngày.
- 142 test qua hết.

**Tân cần thử:** nhắn vài câu vui/buồn, bấm "?" xem dải tâm trạng; kể một ngày đặc biệt rơi vào ngày kia.

## 2026-10-10 – Giai đoạn 25: việc cần làm (bộ não)
- Nhắn "nhớ giúp mình mua sữa" (không có giờ) → Bơ ghi vào **danh sách việc cần làm** (mục nội bộ `viec_can_lam`). Có giờ cụ thể thì vẫn là lời nhắc như cũ.
- Kể "mua sữa rồi" → Bơ gạch việc đó (`xong_viec`). Hỏi "mình còn việc gì?" → Bơ kể lại đúng danh sách.
- Việc xong quá 3 ngày tự dọn; tối đa 50 việc chưa xong; có trong bản sao lưu (bản sao lưu cũ vẫn nạp được).
- 150 test qua hết.

## 2026-10-10 – Giai đoạn 25: hộp "Việc cần làm"
- Nút **"Việc cần làm"** trên đầu trang: danh sách việc, chạm ô vuông để đánh dấu xong (chữ gạch ngang), "Xóa", và ô tự thêm việc. Thêm trùng thì báo.
- Đã thử tự động trên màn hình điện thoại nhỏ (360px), không vỡ, không lỗi JS. 150 test qua hết.

**Tân cần thử:** nhắn "nhớ giúp mình mua sữa", mở "Việc cần làm" xem; rồi nhắn "mua sữa rồi nha".

## 2026-10-10 – Giai đoạn 25 xong (báo cáo): việc cần làm
- Bơ ghi/gạch việc cần làm qua trò chuyện; hộp "Việc cần làm" trên web.
- Bộ chấm điểm tính cách thêm 5 tình huống (tổng 20): nhờ ghi việc, hỏi còn việc gì, kể đã làm xong, đoán tâm trạng mệt, mấy hôm nay buồn.
- README cập nhật (việc cần làm, tâm trạng, nhắc trước ngày đặc biệt). 151 test qua hết.

**Tân cần thử:** `python -m app.thu_tinh_cach` (khoảng 20 câu API) và gửi tổng điểm vào FEEDBACK.md.

## 2026-10-10 – Giai đoạn 26: nhắc khéo việc để lâu
- Việc cần làm ghi từ 3 ngày trước mà chưa xong → Bơ thấy "(ghi 5 ngày trước)" và thỉnh thoảng nhắc khéo một câu khi hợp lúc (không nhắc dồn, không nhắc khi Tân đang buồn). Không tốn thêm câu API.
- 152 test qua hết.

