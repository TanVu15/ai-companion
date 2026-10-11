# Nhật ký tiến độ

## Cách dừng / góp ý (dành cho Tân)
- **Dừng tự chạy:** tạo file tên `STOP` ở thư mục gốc repo (trên github.com: Add file → Create new file → gõ `STOP` → Commit). Xóa file đó để chạy lại. Hoặc nhắn Claude "dừng".
- **Góp ý:** ghi vào file `FEEDBACK.md`, phiên sau Claude sẽ xử lý trước.
- **Lấy bản mới về máy:** `git pull` trong thư mục dự án rồi chạy lại `run.bat`.

## 2026-10-11 – Giai đoạn 69 xong: Bơ đồng cảm
- **Ngáp lây**: gửi tin có "buồn ngủ", "ngáp", "đi ngủ", "ngủ ngon" hoặc 😴 → Bơ ngáp theo ngay (trước khi Bơ trả lời, không tốn API). "ngủ trưa dậy rồi" thì không. Máy bật giảm chuyển động thì thôi.
- **Rình & vồ lông vũ**: bật cần câu lông vũ, thả lông xuống sát đất ngay trước mặt Bơ (dưới hai chân trước) → Bơ hạ người, cúi đầu, mắt mở to dán vào lông, mông với đuôi ngoáy ngoáy "Rình... rình..."; khoảng 1,4 giây sau Bơ nhảy vồ "Phập! Bắt được rồi!" (điện thoại Android rung nhẹ). Rút lông đi trước lúc đó thì Bơ thôi rình. Nghỉ 3 giây giữa hai lần vồ. Ảnh `docs/anh/meo-rinh-long-vu.png` (trái: rình, phải: vồ).
- Rà soát, sửa: nhắn "không buồn ngủ", "chưa buồn ngủ", "hết buồn ngủ" thì Bơ không ngáp nữa. Đang rình thì mắt Bơ mở to cả lúc khuya (trước đây lim dim). Rình/vồ với 4 kiểu lông, nền sáng và tối: rõ, không vỡ hình (ảnh `docs/anh/rinh-kieu-long.png`). `scripts/thu_cham.py` thử thêm rình & vồ — đạt hết. 424 test qua hết.
**Tân cần thử:** bật nút lông vũ, kéo lông xuống ngay dưới chân Bơ rồi giữ yên một giây.

## 2026-10-11 – Giai đoạn 68 xong: bế Bơ ấm hơn
- **Bế yên**: bế Bơ lên rồi giữ yên khoảng 2,5 giây → Bơ thả lỏng trên tay, nhắm mắt lim dim, má hồng, rừ rừ "Rừ rừ... cứ bế Bơ vầy hoài nha". Lắc lên xuống thì Bơ mở mắt lại. Ảnh `docs/anh/meo-be-em.png`.
- Bật "Giọng nói": lần bế đầu tiên trong ngày Bơ đọc to "Ơ ơ, bế Bơ đi đâu đó?", các lần sau chỉ kêu "mrr?"; câu bế yên cũng được đọc to.
- Rà soát, sửa: đang bế mà chuyển tab / có cuộc gọi đến / trình duyệt mất cú chạm thì trước đây Bơ có thể kẹt lơ lửng → giờ tự thả Bơ xuống. Đang dỗi, đang ngủ, đang chơi đồ chơi thì không bế được. 420 test qua hết, `scripts/thu_cham.py` đạt hết.
**Tân cần thử:** bế Bơ lên rồi giữ yên vài giây.
- Bộ ảnh `docs/anh/meo-tat-ca.png` chụp lại, có thêm hắt xì, boop, nựng má, bế, râu sữa.

## 2026-10-11 – Giai đoạn 67 xong: boop mũi & nựng má
- **Boop mũi**: chạm nhanh đúng chóp mũi hồng → Bơ nhắm tịt mắt, mũi chun lại, ria vểnh, chữ "Boop!" bật ra, "Hí, nhột mũi!".
- **Nựng má**: chạm vào má → Bơ nghiêng đầu dụi về bên đó, má hồng đậm, mắt cười, rừ rừ một chút. Chạm trán/đỉnh đầu vẫn là xoa đầu như cũ. Ảnh `docs/anh/meo-boop-nung-ma.png`.
- Rà soát: bàn phím thêm **N** = boop mũi; chữ "Boop!" có viền cho dễ đọc trên lông cam. Chụp boop · nựng má · bế · râu sữa với mèo đen, tam thể, mướp vằn ở nền tối: đều rõ, không vỡ hình (ảnh `docs/anh/tu-the-66-67-kieu-long-toi.png`). `scripts/thu_cham.py` thử thêm boop, nựng má, phím N, phím B — đạt hết. 420 test qua hết.
**Tân cần thử:** chạm nhẹ chóp mũi Bơ, rồi chạm má.

## 2026-10-11 – Giai đoạn 66 xong: tiếng ăn & bế Bơ
- **Tiếng ăn**: đang bật "Giọng nói" thì lúc Bơ ăn có tiếng: cá nhai **rộp rộp**, pate **chép chép** (trầm, mềm), sữa liếm **lép lép** nhanh. Tạo ngay trong trình duyệt, không file, không mạng; độ to đã đo bằng máy, cỡ tiếng meo. Giờ yên lặng, lúc Bơ đang đọc hay bật rảnh tay thì im.
- **Bế Bơ**: nhấn giữ đầu Bơ nửa giây rồi kéo lên → Bơ bị nhấc lên, người dài ra, hai chân sau lủng lẳng, đuôi thõng, mắt tròn xoe "Ơ ơ, bế Bơ đi đâu đó?". Thả tay → Bơ rơi "bịch", bẹp xuống một chút "Hú hồn, đất đây rồi!". Vuốt đầu bình thường (không giữ trước) vẫn là vuốt. Bàn phím: giữ phím **B**. Ảnh `docs/anh/meo-be-len.png`.
- Rà soát, sửa: trên điện thoại màn hình thấp (cao dưới 640px) menu chọn món bị đẩy lên khỏi màn hình → giờ xếp ngang ba món (mũi tên trái/phải cũng đi được). `scripts/thu_cham.py` thử thêm bế Bơ — đạt hết. 419 test qua hết.
**Tân cần thử:** bật "Giọng nói" (có loa), cho Bơ ăn từng món nghe tiếng nhai; nhấn giữ đầu Bơ rồi kéo lên.

## 2026-10-11 – Giai đoạn 65 xong: lông vũ & bữa ăn
- **Chọn món**: nhấn giữ nút con cá nửa giây → hiện menu **Cá / Sữa / Pate** (máy tính: chuột phải; bàn phím: mũi tên lên). Bấm thường thì cho món vừa chọn (nhớ trên máy này). Sữa: Bơ dính râu sữa trắng "Râu Bơ dính sữa rồi nè". Pate: tim bay, "Pate! Bơ mê pate nhất trần đời~". Vẫn không có thanh đói. Ảnh `docs/anh/meo-chon-mon.png`.
- **Hắt xì**: đưa cần câu lông vũ quét ngang mũi Bơ → Bơ nhắm tịt mắt, há miệng "Hắt xì!" (tối đa 6 giây một lần). Ảnh `docs/anh/meo-hat-xi-long-vu.png`.
- Rà soát: menu chọn món dùng được bằng bàn phím (mũi tên lên mở, mũi tên đi, Enter chọn, Esc đóng), đẹp ở nền tối và mèo đen (ảnh `docs/anh/meo-chon-mon-toi.png`); bấm ra ngoài là đóng. Gợi ý trò chưa thử có thêm "nhấn giữ nút cá". `scripts/thu_cham.py` thử thêm chọn món — đạt hết. 417 test qua hết.
**Tân cần thử:** nhấn giữ nút con cá, chọn Sữa xem râu Bơ dính sữa; chọn Pate xem tim bay.

## 2026-10-11 – Giai đoạn 64 xong: Bơ để ý tin nhắn
- Gửi tin có **"cá"** hoặc 🐟 → Bơ liếm mép ngay; có **"thương"/"yêu"**/❤ → tim bay quanh Bơ, Bơ nhắm mắt sướng (trước cả khi Bơ trả lời, không tốn API). "các", "cám ơn", "yêu cầu" không bị nhận nhầm.
- Rà soát chạm & chơi, sửa: đang chơi đồ chơi thì Bơ không tự ngáp/ngó quanh (trước đây mắt bị kéo khỏi đồ chơi); việc vặt gọi chồng nhau không còn tắt sớm.
- Thêm `scripts/thu_cham.py`: bấm thử 15 trò chạm & chơi trên trình duyệt thật (điện thoại + máy tính), in ĐẠT/LỖI — hiện đạt hết.
- Rà soát: "cá nhân", "cá tính", "cá cược" không làm Bơ liếm mép nữa. 415 test qua hết.
**Tân cần thử:** nhắn "tối nay ăn cá" và "thương Bơ ghê" xem Bơ phản ứng.

## 2026-10-11 – Giai đoạn 63 xong: dễ khám phá
- Hộp "Bơ làm được gì?" ghi đủ các trò chạm & đồ chơi mới, phím tắt. Ảnh `docs/anh/hop-choi-voi-bo.png`.
- **Bơ gợi ý trò chưa thử**: mở web khoảng 40 giây mà Bơ đang rảnh (không gõ, không chơi, không mở hộp nào) → Bơ nghiêng đầu, bong bóng gợi ý một trò Tân chưa từng thử ("Psst... chạm nhanh hai lần vào chân Bơ thử xem~"). Tối đa 1 lần/ngày, chỉ hiện chữ; thử hết các trò rồi thì Bơ thôi gợi ý. Ảnh `docs/anh/bo-goi-y.png`.
- Rà soát: đang gõ, đang chơi, đang mở hộp thoại thì Bơ chờ lát nữa mới gợi ý. 414 test qua hết.

## 2026-10-11 – Giai đoạn 62 xong: giọng nói chơi đùa
- Đang bật "Giọng nói": câu **chóng mặt**, **ngửi tay** và **lần đập tay đầu tiên trong ngày** được đọc to (các lần đập tay sau chỉ kêu "meo~"). Giờ yên lặng thì vẫn chỉ hiện chữ.
- Sửa: Bơ đang đọc to mà Tân **vuốt** Bơ thì trước đây Bơ im bặt (vì nhả tay ra bị tính là một cú chạm). Giờ chỉ **chạm nhanh** mới bảo Bơ im; vuốt hay nhấn giữ thì Bơ vẫn đọc tiếp, mắt lim dim sướng.

## 2026-10-11 – Giai đoạn 61 xong: lắc điện thoại
- **Lắc điện thoại** mạnh vài cái → Bơ chóng mặt: mắt xoáy @_@, người lắc lư, "Ối ối, chóng mặt quá~". Đi bộ hay đặt máy xuống không tính (phải 4 cú giật mạnh trong 1 giây). Ảnh `docs/anh/meo-chong-mat.png`.
- Trong "Bơ làm được gì? · Cài đặt" (chỉ hiện trên điện thoại) có ô **"Lắc điện thoại để trêu Bơ"** (ảnh `docs/anh/cai-dat-lac.png`). Android: bật sẵn. iPhone: phải tick ô này, máy hỏi cho phép thì bấm "Cho phép".
- Rà soát: iPhone tải lại trang có thể quên quyền → lần chạm Bơ đầu tiên tự xin lại (đã cho phép thì không hiện hộp hỏi). README thêm ngửi tay, chạm đuôi, lắc. 412 test qua hết.
**Tân cần thử:** trên điện thoại, lắc mạnh 3–4 cái.

## 2026-10-11 – Giai đoạn 60 xong: đẹp đều mọi bộ lông, rừ rừ ấm hơn
- Chụp 6 tư thế mới (ngược lông · đập tay · rửa mặt · ngửi · cọ má · chạm đuôi) với 4 kiểu lông (thường, tam thể, mèo đen, mướp vằn), cả nền sáng và tối: đều rõ, không vỡ hình. Ảnh `docs/anh/tu-the-moi-kieu-long.png`, `docs/anh/tu-the-moi-kieu-long-toi.png`.
- **Rừ rừ ấm hơn**: mới vuốt thì rừ rừ nhỏ, vuốt liền vài giây thì to dần (tối đa vừa phải). Điện thoại Android có rung thì rung rất nhẹ ba nhịp lúc Bơ bắt đầu rừ rừ (iPhone không hỗ trợ rung từ web; máy bật giảm chuyển động thì không rung).
- Rà soát: các chuyển động mới đều tắt khi máy bật giảm chuyển động. 411 test qua hết.
**Tân cần thử:** vuốt Bơ liền 5–6 giây (bật loa) nghe rừ rừ to dần.

## 2026-10-11 – Giai đoạn 59 xong: ngửi tay & cọ má
- **Ngửi tay**: để yên chuột (hoặc giữ ngón tay) ngay trước mũi Bơ khoảng 1 giây → Bơ rướn đầu, nhìn xuống tay, mũi phập phồng; rồi nhắm mắt cọ má, rừ rừ "Hít hít... thơm tay bạn ghê~". Mỗi 8 giây tối đa một lần. Ảnh `docs/anh/meo-ngui-tay.png` (ngửi · cọ má).
- Bàn phím: Tab tới Bơ rồi bấm **T** = chạm tai, **D** = đập tay (cùng với Enter xoa đầu, phím cách gãi cằm).
- Rà soát: cọ má xong mà Tân đang vuốt Bơ thì tiếng rừ rừ không bị tắt ngang nữa. 409 test qua hết.
**Tân cần thử:** trên máy tính, để chuột yên ngay mũi Bơ 1 giây; trên điện thoại, đặt ngón tay lên mũi Bơ và giữ yên.

## 2026-10-11 – Giai đoạn 58 xong: đuôi & tiếng meo
- **Chạm đuôi**: đuôi vụt sang một bên, Bơ quay đầu liếc nhìn "Đuôi Bơ mà!". Ảnh `docs/anh/meo-cham-duoi.png`.
- **Tiếng meo**: đang bật "Giọng nói" thì chạm tai/đuôi Bơ kêu "mrr?" ngắn, đập tay thì "meo~" cao dần. Tiếng tạo ngay trong trình duyệt (không file, không mạng). Không kêu trong giờ yên lặng, lúc Bơ đang đọc hay đang bật rảnh tay.
- Rà soát: tiếng meo lúc đầu hơi nhỏ so với giọng đọc (đã đo bằng cách dựng âm thanh thử) → tăng gấp đôi. 407 test qua hết.
**Tân cần thử:** bật "Giọng nói", chạm tai Bơ và chạm nhanh hai lần vào chân trước, nghe tiếng meo có dễ thương không (chưa ưng thì ghi `FEEDBACK.md`: cao/thấp, dài/ngắn).

## 2026-10-11 – Giai đoạn 57 xong: chạm tinh tế hơn
- **Vuốt ngược lông**: chạm/bấm vào hai bên lưng Bơ rồi kéo **lên trên** → lông hai bên dựng đứng, tai cụp ngang, mắt nheo, miệng méo, "Ngược lông rồi á!". Kéo xuống (xuôi) thì vẫn rừ rừ như cũ. Rê chuột không bấm thì không tính. Ảnh `docs/anh/meo-nguoc-long.png`.
- **Đập tay**: chạm nhanh **hai lần** vào chân trước của Bơ → Bơ giơ chân lên cạnh má, mắt cười, chữ "Bốp!" bật ra, "Đập tay nè!". Chạm một lần thì Bơ chỉ rụt chân. Bơ biết hôm nay đập tay mấy lần. Ảnh `docs/anh/meo-dap-tay.png`.
- **Việc vặt lúc rảnh** thêm hai kiểu: **rửa mặt** (lấy chân xoa má, nhắm mắt) và **ngó quanh** (đầu và mắt liếc trái rồi phải), xen với ngáp/liếm chân. Đang nằm bẹp thì không rửa mặt. Máy bật giảm chuyển động thì không có. Ảnh `docs/anh/meo-rua-mat-ngo.png`.
- Bộ ảnh `docs/anh/meo-tat-ca.png` có thêm ngược lông, đập tay, rửa mặt. README cập nhật bảng chạm & chơi. 406 test qua hết.
**Tân cần thử (trên điện thoại):** đặt ngón tay bên hông Bơ rồi kéo lên; chạm nhanh hai lần vào chân trước; để yên vài phút xem Bơ rửa mặt.

## 2026-10-11 – Giai đoạn 56 xong: bàn phím, "Bơ ơi", dọn code
- Đồ chơi dùng được bằng **bàn phím**: bật laser/lông vũ rồi bấm phím mũi tên để di chuyển; cuộn len thì mũi tên để hất (lên = tung cao).
- Rảnh tay: chỉ gọi "Bơ ơi" → Bơ nghiêng đầu, bong bóng "Dạ? Bơ nghe nè!" rồi chờ 8 giây nghe tiếp.
- Dọn code: ba đồ chơi (laser, cuộn len, lông vũ) tách ra file riêng `web/do_choi.js`; `choi.js` còn phần vuốt/chạm/cho ăn. Hành vi giữ nguyên (đã bấm thử từng đồ chơi bằng Playwright, không lỗi). 401 test qua hết.
- Rà soát, sửa: gọi "Bơ ơi" xong mà không nói gì thì dòng chữ "Bơ nghe nè..." bị kẹt mãi → giờ sau 8 giây quay về "Gọi Bơ ơi để nói chuyện". Ảnh `docs/anh/bo-oi.png`.
- Sửa: cuộn len lăn tới nằm đè lên nút cá/cuộn len (máy tính) → che nút, bấm không trúng. Giờ len nằm đè nút thì tự lăn nhẹ vào giữa (Bơ lại vồ tiếp).
**Tân cần thử:** bật "Rảnh tay", gọi "Bơ ơi" xem Bơ nghiêng đầu dạ; bật laser rồi bấm phím mũi tên; ném cuộn len xem nó còn che nút cá không.

## 2026-10-11 – Giai đoạn 55 xong: thêm chút sống động
- Ngủ say: Bơ thỉnh thoảng giật tai trong mơ hoặc trở mình. Đang đọc to: đuôi vẫy nhanh hơn, tai động nhẹ.
- **Cần câu lông vũ** (nút xanh, trên nút laser): lông vũ treo dây, lắc lư theo ngón tay/chuột; đưa lên trên đầu Bơ là Bơ giơ hai chân trước vồ. Ảnh `docs/anh/long-vu.png`. Mỗi lúc chỉ một đồ chơi (bật cái này thì cất cái kia).
- Sửa: mỗi câu giọng AI trước đây để lại một "nút âm thanh" trong trình duyệt → nói chuyện bằng giọng rất lâu sẽ nặng dần; giờ ngắt sau mỗi câu.
- Rà soát: đang chơi lông vũ mà nhấn giữ lên Bơ thì không bị nhầm thành "lăn nũng"/chọc bụng. README cập nhật bảng chạm & chơi, ảnh kiểu lông. 400 test qua hết.
**Tân cần thử (giai đoạn 51–55, đều miễn phí):** nhấn giữ bụng Bơ 1 giây; bấm nút cuộn len rồi kéo ném; bấm nút lông vũ rồi rê lên trên đầu Bơ;
chọn kiểu lông "Tam thể" trong Cài đặt; bật "Giọng nói" rồi cho Bơ ăn cá; thử 3 giọng mẫu. Thấy chỗ nào xấu/khó dùng thì ghi `FEEDBACK.md`.

## 2026-10-11 – Giai đoạn 54: tư thế & bộ lông
Ảnh: `docs/anh/kieu-long.png` (thường · mướp vằn · tam thể · mèo đen), `docs/anh/meo-o-banh-mi.png`, `docs/anh/meo-den-toi.png`.
- **Ổ bánh mì**: 1 phút không ai đụng → Bơ nằm bẹp, giấu chân, đuôi quấn quanh người, mắt lim dim; 3 phút mới ngủ gật. Chạm/gõ là ngồi dậy.
- **Kiểu lông** (trong "Bơ làm được gì? · Cài đặt", dưới bảng màu lông): Thường, **Mướp vằn** (thêm vằn, dùng màu đã chọn), **Tam thể** (trắng, đốm cam-đen, tai hai màu), **Mèo đen** (mắt vàng, con ngươi dọc). Lưu trên máy này.
- Đổi màu/kiểu lông rồi đóng hộp → Bơ nhảy lên khoe "Thấy Bơ xinh lên hông?" (ảnh `docs/anh/meo-tam-the.png`).
- `docs/anh/meo-tat-ca.png` chụp lại, có thêm các tư thế mới.
- Rà soát: đang chơi laser/cuộn len bằng chuột thì Bơ không nằm bẹp hay ngủ gật giữa chừng nữa. 399 test qua hết.
**Tân cần thử:** chọn "Tam thể" hoặc "Mèo đen" xem có thích không; để yên 1 phút xem Bơ nằm bẹp.

## 2026-10-11 – Giai đoạn 53: Bơ hóng chuyện, giọng mẫu
Ảnh: `docs/anh/bo-hong-chuyen.png`, `docs/anh/cai-dat-giong.png`.
- **Hóng chuyện**: đang gõ tin thì Bơ nhìn xuống khung chat, tai vểnh, đầu hơi nghiêng; ngừng gõ 2 giây thì thôi.
- **Khuya** (22h–5h) vuốt Bơ, thỉnh thoảng Bơ nói "Khuya rồi nè, bạn ngủ sớm nha~" (nhẹ nhàng, không ép).
- Cài đặt → **Giọng mẫu**: "Mặc định", "Mèo con" (cao, nhanh nhẹ), "Mèo béo lười" (trầm, chậm). Bấm là lưu và nghe thử luôn.
**Tân cần thử:** Cài đặt → bấm lần lượt 3 giọng mẫu, chọn cái nghe thích nhất.

## 2026-10-11 – Giai đoạn 52: giọng có cảm xúc, cuộn len
Ảnh: `docs/anh/cuon-len.png`.
- **Giọng theo cảm xúc**: câu vui/hào hứng Bơ đọc nhanh và cao hơn chút, câu buồn chậm và trầm hơn (giọng AI lẫn giọng trình duyệt).
- Đang bật "Giọng nói": câu chơi **mừng rỡ, ăn cá, no, dỗi, làm lành, bị đánh thức** được đọc to (câu ngắn có sẵn, lưu đệm). Câu vuốt/chọc chỉ hiện chữ cho đỡ ồn. Giờ yên lặng thì không đọc.
- **Cuộn len** (nút mới màu hồng, trên nút cá): cuộn len rơi xuống, lăn, nảy. **Kéo rồi ném** nó; len chạm người Bơ là Bơ vồ, đập văng ra. Bật laser thì len cất đi; 20 giây không đụng thì tự cất (Esc cũng cất).
- Bơ biết "hôm nay bạn chơi cuộn len với Bơ N lần". 398 test qua hết.
- Rà soát: bong bóng câu nói trên điện thoại nhỏ bị bó thành 3–4 dòng hẹp → giờ rộng hơn, không đè tai Bơ (ảnh `docs/anh/man-nho-toi.png`, màn 375×600 chế độ tối).
**Tân cần thử:** bật "Giọng nói", cho Bơ ăn cá → nghe Bơ nói "Măm măm"; bấm nút cuộn len, kéo ném vào Bơ.

## 2026-10-11 – Giai đoạn 51: Bơ sống động hơn (không tốn API)
Ảnh: `docs/anh/meo-mung.png` (mừng rỡ), `docs/anh/meo-lan.png` (lăn nũng), `docs/anh/meo-nhin-theo.png`, `docs/anh/meo-lim-dim.png`.
- **Mắt nhìn theo**: rê chuột (máy tính) hoặc kéo ngón tay trên Bơ (điện thoại) → con ngươi liếc theo; đứng yên 3 giây thì nhìn thẳng lại.
- **Bạn về rồi!**: mở web sau từ 1 ngày → Bơ nhảy cẫng, mắt cười, đuôi ngoe nguẩy, bong bóng "Bạn về rồi! Bơ nhớ bạn ghê~". Không trách, không gọi API.
  Sáng sớm (5–10h) lần đầu mở sau ít nhất 4 tiếng → Bơ vươn vai "chào buổi sáng".
- **Nhấn giữ lưng/bụng ~1 giây** → Bơ lăn qua lăn lại nũng nịu, co hai chân trước lên ngực ("Gãi bụng Bơ đi mà~").
- **Khuya (22h–5h)**: mắt Bơ lim dim, hay ngáp hơn.
- Rà soát: đang lăn mà bị chọc 5 lần thì Bơ dỗi quay lưng đúng (trước bị kẹt tư thế lăn); giữ lâu trên iPhone không hiện menu "Sao chép".
- 394 test qua hết.
**Tân cần thử:** trên điện thoại, đặt ngón tay lên bụng Bơ và giữ yên 1 giây.

## 2026-10-11 – Giai đoạn 50 xong: gọn & chắc
Ảnh: `docs/anh/tinh-trang-giong.png`, `docs/anh/meo-ban-phim.png`, `docs/anh/menu-them.png`.
- Rà soát mèo / chạm / giọng AI / giữ để nói, sửa:
  - Giọng AI đọc đoạn dài hơn 20 giây (máy chưa biết độ dài file) bị cắt ngang và đọc chồng đoạn sau → giờ chỉ coi là "xong" khi âm thanh thật sự dừng.
  - Dùng được bằng **bàn phím**: Tab tới nút "Giữ để nói" rồi giữ phím cách = giữ để nói; Tab tới Bơ, Enter = xoa đầu, phím cách = gãi cằm (đang đọc to thì phím bảo Bơ im).
  - Rê chuột vuốt Bơ lâu không làm Bơ ngủ gật giữa chừng nữa.
  - `.env` ghi `TOC_DO_GIONG=+10%` hay `CAO_DO_GIONG=8Hz` (gõ nhầm kiểu edge-tts) trước đây làm máy chủ **không chạy được** → giờ hiểu được, sai hẳn thì dùng mặc định.
- 392 test qua hết.
**Tân cần thử (giai đoạn 50):** mở "Bơ làm được gì? · Cài đặt" → Tình trạng, xem dòng "Giọng AI" sau khi bật Giọng nói và nhắn một câu.

## 2026-10-11 18:00 UTC – Giai đoạn 50: Tình trạng báo giọng AI
- "Bơ làm được gì? · Cài đặt" → **Tình trạng** có dòng **Giọng AI**: chưa thử / "Dùng được — đọc thành công lần gần nhất lúc 18:02" /
  "Lỗi lúc 18:05: không gọi được máy chủ giọng — kiểm tra mạng" / "Chưa cài edge-tts — chạy lại run.bat". Ảnh: `docs/anh/tinh-trang-giong.png`.
- Thông báo nhỏ "Giọng AI chưa dùng được" giờ chỉ luôn chỗ xem lý do. SU_CO.md thêm dòng cho lỗi này. 391 test qua hết.

## 2026-10-11 17:45 UTC – Giai đoạn 50 (đang làm): đầu trang gọn
- Các nút chữ (Bơ nhớ gì, Việc cần làm, Nhật ký, Thói quen, Tìm, Chi phí, Tính cách, "?") gom vào nút **"☰ Thêm"**;
  đầu trang chỉ còn mèo, nút "Giữ để nói", Giọng nói, Rảnh tay → khung chat trên điện thoại rộng gần gấp đôi.
  Ảnh: `docs/anh/trang-dien-thoai.png`, `docs/anh/menu-them.png`.

## 2026-10-11 17:40 UTC – Giai đoạn 49 xong: Trò chuyện bằng giọng mượt
Ảnh: `docs/anh/giu-de-noi.png`.
- Nút to **"Giữ để nói"** ngay dưới mèo (kiểu bộ đàm): giữ là Bơ nghe, thả tay là gửi. Bấm nhanh quá thì Bơ nhắc "giữ trong lúc nói".
- Khi micro đang nghe, mèo **dựng tai, nghiêng đầu lắng nghe**.
- Tin nói bằng micro (nút giữ, nút micro nhỏ, hay "Bơ ơi" rảnh tay) → Bơ được dặn trả lời **1–2 câu, không ký hiệu**, và **đọc to** câu trả lời kể cả khi đang tắt "Giọng nói".
- Nút chỉ hiện khi trình duyệt nghe được giọng (Chrome/Edge trên máy tính; trên điện thoại cần https – xem `DUA_LEN_MANG.md`).
**Tân cần thử:** trên máy tính mở Chrome ở http://localhost:8000, giữ nút, nói "Bơ ơi hôm nay vui không", thả tay.

## 2026-10-11 17:35 UTC – Giai đoạn 48 xong: Bơ nói bằng giọng AI miễn phí (edge-tts)
- Bật "Giọng nói" → Bơ đọc bằng **giọng AI của Microsoft Edge** (Hoài My, giọng nữ, cao độ +8 cho dễ thương). Không cần tài khoản, không tốn tiền.
- Máy chủ tạo mp3 (`/api/giong`), lưu đệm trong `data/am_thanh/` (giữ 200 file) nên câu lặp lại phát ngay không cần mạng.
- Câu dài: đọc câu đầu ngay, tải sẵn câu sau trong lúc đọc. **Miệng mèo mở theo âm lượng thật** của giọng.
- Nút "?" → Cài đặt: chọn giọng (Hoài My / Nam Minh), thanh trượt tốc độ và cao độ, nút "Lưu rồi nghe thử giọng". Ảnh: `docs/anh/cai-dat-giong.png`.
- Không có mạng / Microsoft lỗi → tự dùng giọng của trình duyệt, báo nhỏ một lần, 5 phút sau thử lại giọng AI.
- **Tân cần thử (quan trọng):** máy làm việc của Claude KHÔNG gọi được máy chủ Microsoft nên chưa nghe thử giọng thật.
  `git pull`, chạy `run.bat` (nó tự cài `edge-tts`), bật "Giọng nói", nhắn một câu. Nếu thấy dòng
  "Giọng AI chưa dùng được" thì gửi mấy dòng cuối `data/loi.log` vào `FEEDBACK.md`. Nghe xong thấy giọng cao/thấp/nhanh quá thì chỉnh ở Cài đặt.

## 2026-10-11 17:25 UTC – Giai đoạn 47 xong: Chạm & chơi với Bơ, không tốn API
Ảnh: `docs/anh/choi-voi-bo.png` (vuốt đầu · gãi cằm · dỗi quay lưng · ăn cá). 379 test qua hết.
- **Vuốt** đầu/lưng (kéo ngón tay, hoặc rê chuột trên máy tính): Bơ nhắm mắt, tim bay, kêu **rừ rừ** (tạo bằng Web Audio, không cần file).
- **Gãi cằm**: ngửa cổ sướng. **Chạm tai**: tai giật. **Chọc bụng**: giật mình; chọc 5 lần trong 4 giây → **dỗi quay lưng** 4 giây rồi làm lành.
- **Nút con cá**: cá rơi xuống, Bơ cúi xuống nhai rồi liếm mép. Không có thanh "đói"; cho quá 5 lần/ngày Bơ chỉ bảo "no rồi".
- **Nút chấm đỏ (laser)**: rê/kéo ngón tay quanh Bơ, mắt Bơ nhìn theo, chấm chạy vào người là Bơ vồ. 15 giây không đụng thì tự tắt (Esc cũng tắt).
- Câu nói nhỏ hiện bong bóng cạnh Bơ, không lưu vào lịch sử chat. Chạm Bơ không làm cuộn trang trên điện thoại.
- **Bơ nhớ nhẹ:** web đếm số lần vuốt/gãi cằm/cho ăn hôm nay, gửi kèm tin nhắn thành một dòng ngắn → Bơ thỉnh thoảng nói "hôm nay bạn gãi cằm Bơ 5 lần đó nha". Tốn thêm khoảng 30 token mỗi câu (gần như 0 đồng).
**Tân cần thử:** trên điện thoại, vuốt đầu Bơ và nghe tiếng rừ rừ (bật tiếng máy). Thấy tiếng to/nhỏ/khó nghe thì ghi `FEEDBACK.md`.

## 2026-10-11 17:00 UTC – Giai đoạn 46 xong: Mèo Bơ ra đời 🐱
Khuôn mặt tròn đã thành **mèo béo màu cam** (vẽ bằng SVG, không dùng ảnh ngoài). 374 test qua hết.
- **Xem ngay trên GitHub (không cần chạy):** `docs/anh/meo-tat-ca.png` (mọi cảm xúc), `docs/anh/trang-dien-thoai.png`,
  `docs/anh/trang-may-tinh.png`, `docs/anh/trang-toi-vay-tay.png` (chế độ tối, mèo vẫy chân).
- 7 cảm xúc: vui (mắt ^^, đuôi dựng), hào hứng (há miệng, nhún nhảy), suy nghĩ (nghiêng đầu, tai xoay, nhìn lên),
  ngạc nhiên (mắt to, tai dựng, đuôi xù), buồn (tai cụp, đuôi quấn, miệng mếu), thương (má hồng, lim dim), bình thường.
- 6 hành động: gật/lắc/nghiêng đầu, nhảy, vẫy chân trước.
- "Sống": bụng phập phồng thở, đuôi đung đưa, chớp mắt ngẫu nhiên, 25–55 giây ngáp hoặc liếm chân một lần.
- Ngủ gật (3 phút): mèo cuộn đuôi, mắt nhắm, "zzz" bay; chạm là tỉnh và **vươn vai**.
- Lúc chờ trả lời: ngoe nguẩy đuôi nhìn lên. Lúc đọc to: miệng mấp máy.
- Nút "?" → **Màu lông Bơ**: cam (mặc định), vàng, xám, trắng kem, nâu, xanh bơ, hồng, xanh dương, tím.
- Máy bật "giảm chuyển động" thì mèo vẫn đổi tư thế nhưng không lắc lư.
- Công cụ mới: `python scripts/chup_meo.py` tự chụp mọi tư thế vào `docs/anh/`.
**Tân cần thử:** `git pull`, chạy `run.bat`, mở trên điện thoại; nhắn vài câu xem mèo đổi tư thế; để yên 3 phút xem mèo ngủ.
Thấy chỗ nào chưa dễ thương (mặt, màu, cỡ) thì ghi vào `FEEDBACK.md`.

## Tóm tắt nhanh lần chạy 2026-10-10 23:31 → 2026-10-11 00:10 UTC
Xong giai đoạn 31 → 38 (244 test qua hết, 8 lượt rà soát độc lập đã sửa lỗi). Đáng thử nhất:
1. **Nhật ký:** kể chuyện trong ngày → nút "Nhật ký"; hỏi "hôm qua mình làm gì nhỉ?". Tự ghi/sửa/tải .txt được.
2. **Thói quen:** "theo dõi giúp mình thói quen đọc sách" → kể "đọc sách rồi" → nút "Thói quen" xem chuỗi ngày. Tối 20:30 chưa làm thì Bơ nhắc nhẹ (miễn phí).
3. **Nhắc linh hoạt:** "ngày đi làm 7h nhắc mình...", "ngày 5 hằng tháng nhắc đóng tiền nhà".
4. **Đếm ngược:** "còn mấy ngày nữa Tết?"; danh sách ngày đặc biệt ghi "(còn X ngày)"; dòng lịch báo ngày sắp tới.
5. **Lịch điện thoại:** "Bơ nhớ gì về mình?" → "Tải lịch cho điện thoại (.ics)" → thêm vào app Lịch iPhone.
6. **Tự sao lưu** mỗi ngày vào `data/sao_luu/` (giữ 7 bản). Nút "?" có "Chuỗi N ngày liền trò chuyện"; tròn 100 ngày / 1 năm quen nhau Bơ tự nhắc.

## Tóm tắt nhanh lần chạy 2026-10-10 (22:31–23:10 UTC)
Xong giai đoạn 24 → 30 (189 test qua hết, 4 lượt rà soát độc lập đã sửa lỗi). Đáng thử nhất:
1. **Tâm trạng:** nút "?" có dải tâm trạng 7 ngày; mấy hôm buồn/mệt Bơ nhẹ nhàng hơn.
2. **Việc cần làm:** "nhớ giúp mình mua sữa" → nút "Việc cần làm"; "mua sữa rồi" → Bơ gạch.
3. **Âm lịch:** dòng lịch dưới tên Bơ; Bơ biết và chủ động chúc ngày lễ (20/10 sắp tới!); kể "giỗ ông 15/7 âm lịch" → hôm trước Bơ nhắc.
4. **Cài đặt trên web:** "?" → Cài đặt (thành phố, giờ yên lặng, tổng kết tuần) — không cần sửa `.env`.
5. **Sửa lời nhắc** ngay trong "Bơ nhớ gì về mình?".
6. `python -m app.thu_tinh_cach` (22 tình huống) → gửi điểm vào `FEEDBACK.md`.

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

## 2026-10-11 tối – SỬA LỖI: Bơ chỉ trả lời "..."
- Tân chạy với API thật: mọi câu trả lời đều là "...".
- Nguyên nhân: Haiku 5.5 có chế độ "suy nghĩ" (adaptive thinking), ăn hết giới hạn 500 token → không còn chữ nào.
- Sửa: tắt suy nghĩ (`thinking: disabled`, model không cho tắt thì tự bỏ tham số), tăng `MAX_TOKENS` lên 4000,
  câu trả lời rỗng thì báo lỗi rõ (kèm stop_reason) thay vì hiện "..." và không lưu "..." vào trí nhớ.
- Bài học cho các phiên tự chạy: test bằng bộ não giả KHÔNG bắt được lỗi kiểu này. Khi đổi cách gọi API,
  luôn giả lập phản hồi giống API thật (có khối thinking, stop_reason) như tests/test_tra_loi_rong.py.

## 2026-10-11 đêm – Giai đoạn 43: chạy thử với API thật trên máy Tân, sửa 4 lỗi thật
Chạy `python -m app.thu_tinh_cach` (29 tình huống) và một cuộc trò chuyện 14 lượt bằng API thật (trí nhớ tạm, không đụng `data/`).
Điểm bộ chấm: 95% → 98% (bộ chấm cũng đã chặt hơn). Tổng tiền thử: khoảng 0,1 đô. 351 test qua hết.
- **Bơ thỉnh thoảng trả lời chữ thường thay vì JSON** (bắt chước lịch sử chat chỉ có chữ) → mất cảm xúc, không ghi nhớ,
  không đặt lời nhắc. Sửa: gửi kèm khuôn JSON bắt buộc (`output_config`, "structured outputs"); model nào không nhận thì tự bỏ.
- **Chi phí hiện cao gấp 10 lần thật:** giá Haiku 5.5 là 0,10 / 0,50 đô cho 1 triệu token, `.env` đang ghi 1 / 5 (giá Haiku 4.5)
  → ngân sách 5 đô/tháng sẽ dừng Bơ khi mới tiêu thật 0,5 đô. Sửa: để trống `PRICE_*` thì Bơ tự lấy giá theo model;
  đã xóa hai số đó trong `.env` trên máy Tân; nút "?" → Tình trạng có dòng "Giá tính chi phí" báo khi lệch.
  Mỗi câu trả lời tốn khoảng 0,0008 đô (≈ 20 đồng). **Tân nên so với số tiền thật trên console.anthropic.com.**
- **Bơ hỏi lại mãi một chuyện:** model chép "Chiều nay đi tập chân (kể hôm qua)" vào `da_hoi` nên không khớp, chuyện
  không bao giờ được gạch. Sửa: bỏ ghi chú "(kể ...)" trước khi so. Chuyện hỏi thăm mới giờ ghi ngày cụ thể ("Chiều 11/10...").
- **Bơ bịa số đường dây nóng** khi Tân nói chán sống, và hứa "mai mình đi tập cùng". Sửa: thêm phần "Giới hạn" cố định
  (không nằm trong tính cách tự sửa được): không bịa số điện thoại, nguy hiểm thì chỉ bảo gọi 115, không hứa đi cùng.
- Lời dặn chắc hơn: đúng ngày đặc biệt thì bắt buộc chúc (trước đây 1/4 lần Bơ quên mà vẫn bị tính là đã chúc);
  việc nhờ nhắc / việc cần làm không bị chép thêm vào "điều Bơ nhớ" nữa (trí nhớ đỡ phình).
- **Rẻ hơn nữa nhờ "prompt caching"** (API tính 1/10 tiền cho đoạn lời dặn giống hệt lần gọi trước, trong 5 phút):
  lời dặn giờ xếp phần cố định (tính cách + cách trả lời, ~5.800 token) lên trước, phần thay đổi (giờ, trí nhớ...) ra sau.
  Đo thật: câu đầu ~7.500 token quy đổi, các câu sau ~1.000 (trước đây câu nào cũng ~6.000). Chấm 29 tình huống
  giờ tốn 0,006 đô thay vì 0,021; điểm 99%. Số token trong "Chi phí" là số đã quy đổi về giá thường.
  Lưu ý khi sửa `build_system_prompt`: đừng đưa thứ gì thay đổi (giờ, tên, trí nhớ) lên trước dòng "## Tình hình lúc này".
- **Rà soát lần 23** (xong giai đoạn 43, 355 test qua hết): "cứ 2 tiếng nhắc mình..." model hay ghi lần đầu = ngay bây giờ
  nên vừa nhờ xong đã bị nhắc → giờ lần đầu luôn là N tiếng nữa (rơi vào giờ yên lặng thì dời tới sáng); kiểu lặp của
  lời nhắc nằm trong khuôn JSON nên model không ghi sai kiểu được; model không nhận một tham số thì ghi vào `loi.log`;
  SU_CO.md thêm 3 dòng (chi phí hiện cao, "Bơ không trả lời được", "Bơ bị khựng").
- Việc tiếp theo đã ghi trong TASKS.md (giai đoạn 44).
- Bài học cho phiên tự chạy: máy của Tân gọi được API thật. Khi sửa lời dặn (prompt), chạy `python -m app.thu_tinh_cach`
  để xem model thật phản ứng ra sao; test giả chỉ kiểm tra được phần code.

**Tân cần thử (giai đoạn 43):** tắt cửa sổ `run.bat` đang chạy rồi mở lại (để nạp code mới); nhắn vài câu, bấm "Chi phí" xem
số tiền (giờ nhỏ hơn 10 lần); bấm "?" → Tình trạng xem dòng "Giá tính chi phí".

## 2026-10-11 đêm – Giai đoạn 44: tin cậy khi dùng thật
- **Dòng "✓ Bơ đã ghi: ..."** dưới câu trả lời: nhắc 20:00 12/10: Gọi mẹ · việc cần làm: Mua sữa · nhớ: ... · nhật ký: ...
  (cả bỏ nhắc, xong việc, tích thói quen, quên điều cũ). Lấy từ so sánh trí nhớ trước/sau câu trả lời, không lấy từ lời Bơ
  nói — nên Bơ hứa "để Bơ nhắc" mà không ghi thì không có dòng này. Lưu kèm tin nhắn (mở lại web vẫn thấy, có trong sao lưu).
  Cổng thiết bị không đổi (vẫn chỉ `noi`, `cam_xuc`, `hanh_dong`). Đã thử trên web với API thật. 364 test qua hết.
- **Thử lời Bơ tự mở đầu bằng API thật** (7 kiểu: hỏi thăm, lâu không gặp, tổng kết tuần, chúc 20/10, sinh nhật, mai sinh
  nhật mẹ, tròn 100 ngày quen). Lời chào đều tự nhiên; sửa 3 lỗi lộ ra:
  - Bơ tự mở lời mà model vẫn "ghi" từ chuyện cũ (tạo ngày đặc biệt "Ngày quen nhau", ghi lại điều nhớ, chuyện hỏi thăm)
    → khi Bơ tự mở lời thì chỉ được gạch chuyện đã hỏi thăm, không ghi gì mới.
  - Vừa hỏi thăm xong model lại chép đúng chuyện đó vào danh sách hỏi thăm (lần sau hỏi lại) → bỏ mục trùng.
  - Tin cũ "mai mình đi phỏng vấn" gửi 4 ngày trước bị hiểu là ngày mai tính từ hôm nay (lịch sử gửi cho model không có
    ngày) → tin của hôm trước giờ kèm ghi chú "(tin gửi hôm qua, 10/10)" khi gửi cho model (trí nhớ không đổi).
    Thử lại: Bơ hỏi đúng "hôm qua bạn nói mai đi phỏng vấn, buổi phỏng vấn sao rồi?".
- **Dọn "điều Bơ nhớ"** (tự chạy khi danh sách tới 30 điều): giờ bỏ luôn việc vặt và chuyện đã qua ngày, giữ thông tin
  lâu dài. Thử thật trên 32 điều lẫn lộn → còn 19, không mất điều nào quan trọng. Nếu AI xóa quá tay (còn dưới 1/3) thì
  giữ nguyên bản cũ.
- Bộ 29 tình huống sau các thay đổi: 100%. 368 test qua hết.
- **Rà soát lần 24** (xong giai đoạn 44): gom cách so chuyện hỏi thăm về một chỗ (`Memory.followup_keys`), nên model chép kèm
  gạch đầu dòng hay ghi chú "(kể hôm qua)" đều khớp ở cả hai nơi dùng. Chạy lại 3 câu thật qua máy chủ: dòng "✓ Bơ đã ghi"
  hiện đúng "xong việc", "nhật ký", "bỏ nhắc". Không tìm thấy lỗi khác. Việc tiếp theo: giai đoạn 45 trong TASKS.md.

**Tân cần thử (giai đoạn 44):** tắt rồi mở lại `run.bat`; nhắn "8h tối mai nhắc mình gọi mẹ, với nhớ giúp mình mua sữa" và xem
dòng nhỏ "✓ Bơ đã ghi: ..." dưới câu trả lời; tải lại trang xem dòng đó còn không. Hôm sau mở web xem Bơ hỏi thăm chuyện cũ
có đúng ngày không.

## 2026-10-11 khuya – ĐỔI HƯỚNG: Bơ thành mèo béo
- Tân thấy khuôn mặt tròn chán. Chốt: Bơ là **mèo béo**, chạm vào có phản ứng, nói bằng **giọng AI miễn phí (edge-tts)**.
- Hướng chi tiết ở HUONG_PHAT_TRIEN.md. Việc mới: giai đoạn 46–49 trong TASKS.md.
- Tạm dừng thêm tính năng ngoài hướng này. persona.md đã thêm phần "Bơ là một con mèo béo".
- Lưu ý: nếu Tân đã sửa tính cách trên web (data/persona_tu_sua.md) thì bản đó được ưu tiên → bấm "Về mặc định" để dùng persona mới.

## Cần Tân quyết định
- **Dùng Bơ ngoài nhà bằng cách nào?** Tailscale (riêng tư, cần tạo tài khoản miễn phí, cài app trên iPhone) hay Cloudflare Tunnel (link công khai, không cần cài trên điện thoại). Hướng dẫn cả hai trong `DUA_LEN_MANG.md`. Claude khuyên Tailscale. Cách nào cũng phải đặt `APP_PASSWORD`.
- **Ngân sách tháng:** `.env` trên máy Tân đang đặt `MONTHLY_USD_LIMIT=5` (5 đô/tháng). Với giá Haiku 5.5 thật thì 5 đô là khoảng 6.000 câu trả lời — Tân có thể hạ xuống 1–2 đô nếu muốn chặt hơn.
- **Số đường dây hỗ trợ tâm lý:** hiện Bơ chỉ nhắc 115 khi nguy hiểm. Nếu Tân muốn Bơ đưa thêm một số tư vấn tâm lý cụ thể thì Tân tự kiểm tra số đó còn hoạt động rồi ghi vào `FEEDBACK.md` (Claude không tự thêm vì không xác minh được).
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

## 2026-10-10 – Giai đoạn 26: cổng thiết bị lấy việc cần làm
- `GET /api/thiet-bi/viec` (cần `DEVICE_KEY`): danh sách việc chưa xong cho màn hình nhỏ sau này, có `?khong_dau=1`. Hướng dẫn trong `THIET_BI.md`. 153 test qua hết.

## 2026-10-10 – Giai đoạn 26 xong (báo cáo): nhắc khéo & bảo trì
- Rà soát lần 8 (độc lập) phần việc cần làm. Đã sửa:
  - Bơ chép kèm "(ghi 4 ngày trước)" khi gạch việc thì trước đây không gạch được → giờ được.
  - Danh sách dài hơn 30 việc thì việc mới bị Bơ "không thấy" → giờ Bơ thấy đủ 50.
  - Bỏ đánh dấu một việc đã xong mà đã có việc y hệt đang mở → báo, không tạo việc trùng.
  - Báo lỗi rõ hơn (trùng / danh sách đầy), hộp "Việc cần làm" báo khi mất mạng.
  - Bộ chấm điểm: "Gạch việc đã xong" chỉ đạt khi việc thật sự được gạch.
- `SU_CO.md` thêm 5 dòng (tâm trạng đoán sai, việc cần làm ghi nhầm, nhắc trước ngày đặc biệt...).
- 158 test qua hết.

## 2026-10-10 – Giai đoạn 27: cài đặt trên web
- Nút **"?"** có mục **Cài đặt**: thành phố (thời tiết), giờ yên lặng, bật/tắt tổng kết tuần. Bấm "Lưu cài đặt" là áp dụng ngay, không cần sửa `.env` hay chạy lại.
- Lưu ở `data/cai_dat.json` (ưu tiên hơn `.env`). "Về như file .env" để bỏ. Gõ sai (ví dụ giờ 25-6) thì báo rõ, không lưu.
- API key, mật khẩu vẫn chỉ ở `.env` (không chỉnh trên web, cho an toàn).
- Đã thử tự động trên trình duyệt (màn hình điện thoại). 163 test qua hết.

**Tân cần thử:** bấm "?", gõ thành phố "Da Nang", Lưu; rồi hỏi Bơ "mai trời sao?".

## 2026-10-10 – Giai đoạn 27: sửa lời nhắc trên web
- "Bơ nhớ gì về mình?" → Lời nhắc sắp tới → nút **"Sửa"**: đổi việc, ngày giờ, một lần / mỗi ngày / mỗi tuần. Chọn giờ đã qua thì báo, không lưu. Không tốn câu API.
- Đã thử tự động trên trình duyệt. 165 test qua hết.

**Tân cần thử:** nhắn "8h tối nhắc mình gọi mẹ", rồi vào "Bơ nhớ gì về mình?" → Sửa thành 9h.

## 2026-10-10 – Giai đoạn 27 xong (báo cáo): cài đặt trên web
- Rà soát lần 9 (độc lập). Đã sửa:
  - Lưu cài đặt chỉ giữ mục khác `.env` → sau này Tân sửa `.env` vẫn có tác dụng với mục chưa chỉnh trên web.
  - Sửa lời nhắc thành y hệt một lời nhắc khác (cùng việc, cùng giờ) → báo, không tạo nhắc trùng.
  - Mở hộp "?" chỉ đọc cài đặt, không tự đổi (tránh thời tiết lệch thành phố).
- Cả giai đoạn: mục Cài đặt (thành phố, giờ yên lặng, tổng kết tuần), sửa lời nhắc trên web. 168 test qua hết.

**Tân cần thử:** "?" → Cài đặt; "Bơ nhớ gì về mình?" → Sửa lời nhắc.

## 2026-10-10 – Giai đoạn 28: âm lịch & ngày lễ
- Bơ tự tính **âm lịch** (không cần mạng, không tốn tiền): biết hôm nay "mùng 1 tháng 9 năm Bính Ngọ", đã kiểm tra với ngày Tết 2000–2027, Trung thu, tháng nhuận.
- Bơ biết hôm nay/ngày mai là lễ gì: Tết, Giao thừa, Rằm tháng Giêng, Giỗ Tổ, Trung thu, Vu Lan, ông Táo, 8/3, 30/4, 2/9, **20/10**, 20/11, Noel... và nhắc tự nhiên khi hợp chuyện.
- 181 test qua hết.

**Tân cần thử:** hỏi Bơ "hôm nay âm lịch ngày mấy?"; ngày 19/10 thử chào Bơ xem có nhắc mai 20/10 không.

## 2026-10-10 – Giai đoạn 28: ngày đặc biệt theo âm lịch
- Kể "giỗ ông 15/7 âm lịch" → Bơ ghi là ngày âm; mỗi năm tự tính ra ngày dương tương ứng để nhắc trước 1 ngày và đúng ngày thì nhắc. Giỗ ngày 30 mà tháng đó chỉ có 29 ngày thì tính vào ngày 29.
- "Bơ nhớ gì về mình?" → Ngày đặc biệt hiện "(âm lịch)". 184 test qua hết.

**Tân cần thử:** kể Bơ một ngày giỗ hoặc sinh nhật âm của người nhà, rồi mở "Bơ nhớ gì về mình?" xem.

## 2026-10-10 – Giai đoạn 28 xong (báo cáo): âm lịch & ngày lễ
- Rà soát lần 10 (độc lập): so bộ đổi âm lịch với bản gốc của Hồ Ngọc Đức trên **mọi ngày 1900–2099** → khớp hết. Giỗ/sinh nhật âm được chúc đúng 1 lần mỗi năm âm. Đã sửa 2 điểm nhỏ (2 ngày hiếm năm 2054/2062; Bơ ghi "âm lịch" bằng chữ khác vẫn hiểu).
- Cả giai đoạn: âm lịch offline, ngày lễ Việt Nam, ngày đặc biệt theo âm lịch. 185 test qua hết.

**Tân cần thử:** hỏi "hôm nay âm lịch ngày mấy?"; kể "giỗ ông 15/7 âm lịch".

## 2026-10-10 – Giai đoạn 29: lịch nhỏ
- Dưới tên Bơ có dòng lịch: "Thứ Bảy 10/10 · âm 1/9", ngày lễ thì thêm chữ đậm (ví dụ "· Tết Trung thu"). Tự cập nhật qua nửa đêm.
- Cổng thiết bị `GET /api/thiet-bi/hom-nay` cho màn hình đồng hồ sau này (xem `THIET_BI.md`). 186 test qua hết.

## 2026-10-10 – Giai đoạn 29 xong (báo cáo): lịch nhỏ
- Dòng lịch dương/âm dưới tên Bơ; cổng thiết bị lịch hôm nay; bộ chấm điểm thêm 2 tình huống (tổng 22): hỏi ngày âm, kể ngày giỗ âm lịch.
- 187 test qua hết.

**Tân cần thử:** `git pull`, chạy lại, nhìn dòng lịch dưới tên Bơ; chạy `python -m app.thu_tinh_cach` gửi điểm vào FEEDBACK.md.

## 2026-10-10 – Giai đoạn 30 xong (báo cáo): chúc ngày lễ
- Ngày lễ (Tết, Trung thu, 20/10, Noel...) mở web từ 7h sáng → Bơ chủ động chúc, mỗi ngày lễ 1 lần (1 câu API). Nếu Tân nhắn trước thì Bơ chúc luôn trong câu trả lời, không chúc riêng nữa. Tắt bằng `CHUC_LE=0` trong `.env` hoặc bỏ tick "Chúc ngày lễ" trong "?" → Cài đặt.
- 189 test qua hết (test không bị lệch khi chạy đúng ngày lễ).

**Tân cần thử:** sáng 20/10 mở web xem Bơ chúc gì.

## 2026-10-10 – Giai đoạn 31: đếm ngược ngày đặc biệt
- Danh sách "Ngày đặc biệt" trên web giờ sắp theo ngày gần nhất, ghi "(còn 10 ngày)", "(ngày mai)", "(hôm nay!)". Ngày âm lịch ghi thêm ngày dương năm nay rơi vào.
- Bơ biết các ngày đặc biệt trong 7 ngày tới → hỏi "còn mấy ngày nữa sinh nhật mẹ?" là Bơ trả lời đúng.
- 195 test qua hết.

## 2026-10-10 – Giai đoạn 31: tự sao lưu mỗi ngày
- Mỗi ngày, lần đầu Tân nhắn tin (hoặc mở web), Bơ ghi một bản sao lưu vào `data/sao_luu/bo-NGÀY.json`, giữ 7 bản gần nhất. Không tốn câu API nào.
- Lỡ "Xóa hết" hay file trí nhớ hỏng → "Bơ nhớ gì về mình?" → "Nạp bản sao lưu" → chọn file trong `data/sao_luu/`.
- Nút "?" → tình trạng có dòng "Tự sao lưu" (mấy bản, bản mới nhất). Tắt bằng `TU_SAO_LUU=0`; đổi số bản bằng `SAO_LUU_GIU`.
- 200 test qua hết.

## 2026-10-10 – Giai đoạn 31 xong: rà soát lần 11
- Rà soát độc lập phần đếm ngược + tự sao lưu: số ngày đúng (kể cả 29/2, tháng nhuận âm, qua năm). Sửa 3 lỗi nhỏ: hai tin nhắn cùng lúc có thể ghi chồng bản sao lưu; nút "?" có thể lỗi nếu không đọc được thư mục sao lưu; danh sách ngày đặc biệt đọc trí nhớ không khóa.
- 201 test qua hết.

**Tân cần thử (giai đoạn 31):** mở "Bơ nhớ gì về mình?" xem danh sách ngày đặc biệt có "(còn X ngày)"; nhắn một tin rồi xem thư mục `data/sao_luu/` có file `bo-<ngày>.json`.

## 2026-10-10 – Giai đoạn 32: ngày lễ sắp tới
- Bơ biết các ngày lễ trong 45 ngày tới và Tết còn mấy ngày → hỏi "còn mấy ngày nữa Tết?", "20/10 còn bao lâu?" là Bơ trả lời đúng (tính sẵn, không tốn thêm câu API).
- Dòng lịch dưới tên Bơ: trong 7 ngày tới có lễ / ngày đặc biệt thì ghi "còn 3 ngày nữa là Sinh nhật mẹ"; rê chuột vào dòng lịch xem 3 ngày sắp tới.
- Cổng thiết bị `/api/thiet-bi/hom-nay` có thêm `sap_toi` (xem THIET_BI.md).
- 204 test qua hết.

## 2026-10-10 – Giai đoạn 32: tải lịch cho điện thoại
- "Bơ nhớ gì về mình?" → **"Tải lịch cho điện thoại (.ics)"**: file lịch gồm ngày đặc biệt (lặp mỗi năm; ngày âm lịch ghi sẵn 10 năm tới vì lịch điện thoại không hiểu âm lịch) và lời nhắc sắp tới (cả nhắc mỗi ngày/mỗi tuần). Mỗi ngày đặc biệt báo lúc 20h hôm trước.
- Mở file trên iPhone (Safari/Tệp) hoặc Google Calendar → thêm vào Lịch. Lưu ý: đây là bản chụp lúc tải; thêm ngày mới thì tải lại.
- 209 test qua hết.

## 2026-10-10 – Giai đoạn 32 xong: rà soát lần 12
- Rà soát độc lập: file lịch đúng chuẩn (gập dòng, ký tự đặc biệt, 29/2, giỗ ngày 30 âm), ngày lễ sắp tới không trùng. Sửa 2 lỗi nhỏ: một ký tự thoát viết sai (Python bản mới sẽ báo lỗi); chưa có gì để đưa vào lịch thì web báo rõ thay vì tải về file rỗng (điện thoại sẽ báo "file lỗi").
- 210 test qua hết.

**Tân cần thử (giai đoạn 32):** hỏi Bơ "còn mấy ngày nữa Tết?"; trên iPhone mở web → "Bơ nhớ gì về mình?" → "Tải lịch cho điện thoại" → Thêm vào Lịch.

## 2026-10-10 – Giai đoạn 33: lời nhắc linh hoạt
- Thêm 2 kiểu lặp: **thứ 2–6** ("ngày đi làm 7h nhắc mình uống thuốc bổ") và **mỗi tháng** ("ngày 5 hằng tháng nhắc đóng tiền nhà"; ngày 31 thì tháng thiếu nhắc ngày cuối tháng). Sửa được trong ô sửa lời nhắc trên web; file lịch .ics cũng lặp đúng kiểu.
- Sửa lỗi cũ: Bơ so trùng lời nhắc / ngày đặc biệt bằng chữ thường của SQLite, vốn không hiểu chữ có dấu ("Đi làm" khác "đi làm") → có thể ghi trùng. Giờ so đúng tiếng Việt.
- 214 test qua hết.

## 2026-10-10 – Giai đoạn 33 xong: rà soát lần 13
- Nhắc mỗi tháng ngày 29–31 không bị trôi (31/1 → 28/2 → 31/3), file lịch .ics cũng vậy.
- Rà soát độc lập tìm 2 lỗi, đã sửa: sửa lời nhắc "ngày 31" đúng tháng 2 làm mất ngày gốc; file sao lưu hỏng có thể làm mọi lời nhắc ngừng báo.
- 216 test qua hết.

**Tân cần thử (giai đoạn 33):** "ngày đi làm 7h sáng nhắc mình uống nước" → xem "Lời nhắc sắp tới" ghi "(thứ 2–6)"; "ngày 5 hằng tháng nhắc đóng tiền nhà".

## 2026-10-10 – Giai đoạn 34: nhật ký ngày
- Tân kể việc đã làm trong ngày ("hôm nay đi đá bóng, thắng 3-1") → Bơ tự ghi một dòng nhật ký (tối đa 12 dòng/ngày, không trùng). Chào hỏi, hỏi linh tinh thì không ghi.
- Bơ được xem nhật ký 3 ngày gần nhất → hỏi "hôm qua mình làm gì nhỉ?" là Bơ kể lại đúng. Tốn thêm rất ít chữ mỗi câu.
- Nút **"Nhật ký"** cạnh "Việc cần làm": xem theo ngày (Hôm nay, Hôm qua, Thứ Năm 08/10...), xóa dòng sai, "Xem cũ hơn". Nhật ký nằm trong bản sao lưu.
- Bộ chấm điểm `python -m app.thu_tinh_cach` thêm 3 tình huống (25 tình huống).
- 223 test qua hết.

## 2026-10-10 – Giai đoạn 34 xong: rà soát lần 14
- Sửa lỗi: khi Bơ tự mở lời (tổng kết tuần, lâu không gặp...) có thể ghi chuyện cũ vào nhật ký HÔM NAY. Giờ chỉ ghi khi Tân nhắn.
- Nút "Xóa" trong nhật ký chỉ xóa trên màn hình khi máy chủ xóa được thật.
- 224 test qua hết.

**Tân cần thử (giai đoạn 34):** kể Bơ nghe một chuyện trong ngày, bấm "Nhật ký" xem dòng Bơ ghi; hôm sau hỏi "hôm qua mình làm gì nhỉ?".

## 2026-10-10 – Giai đoạn 35: nhật ký tiện hơn
- **Tổng kết tuần** tối Chủ nhật giờ dựa vào nhật ký (có ngày, có thứ) nếu tuần đó có từ 3 dòng → Bơ điểm lại đúng hơn, gửi ít chữ hơn (rẻ hơn). Ít nhật ký thì dùng tin nhắn như trước.
- Trong "Nhật ký": ô **tự ghi** dòng cho hôm nay, nút **"Sửa"** từng dòng, link **"Tải nhật ký (.txt)"**.
- 226 test qua hết.

## 2026-10-10 – Giai đoạn 35 xong: rà soát lần 15
- Sửa lỗi: sửa một dòng nhật ký thành y hệt dòng khác cùng ngày thì bị trùng → giờ báo "Ngày đó đã có dòng này rồi". Sửa không được thì web báo rõ.
- 227 test qua hết.

**Tân cần thử (giai đoạn 35):** "Nhật ký" → tự ghi một dòng, bấm "Sửa", "Tải nhật ký (.txt)". Tối Chủ nhật xem Bơ tổng kết tuần.

## 2026-10-10 – Giai đoạn 36: kỷ niệm quen nhau
- Nút "?" ghi thêm **"Chuỗi N ngày liền trò chuyện"**.
- Tròn **7, 30, 50, 100, 200, 300, 500, 1000 ngày** hoặc **tròn năm** quen nhau → mở web là Bơ chủ động nhắc dịp này (mỗi mốc một lần, từ 7h sáng, 1 câu API).
- **"Tìm"** giờ tìm cả trong nhật ký (dòng nhật ký hiện đầu, ghi "Nhật ký · Hôm qua, 09/10").
- 231 test qua hết.

## 2026-10-11 – Giai đoạn 36 xong: rà soát lần 16
- Sửa lỗi: kỷ niệm tròn năm bị nhắc sớm 1 ngày (năm nhuận sớm 2 ngày) → giờ đúng ngày tháng quen nhau, Bơ nói "tròn 1 năm".
- Ngày lễ / tối Chủ nhật trùng mốc quen nhau → gộp vào MỘT câu thay vì Bơ tự nhắn 2–3 lần liền (đỡ tốn tiền).
- "Tìm" không trả quá số dòng yêu cầu.
- 233 test qua hết.

**Tân cần thử (giai đoạn 36):** bấm "?" xem "Chuỗi N ngày liền trò chuyện"; "Tìm" gõ một chữ có trong nhật ký.

## 2026-10-11 – Giai đoạn 37: thói quen hằng ngày
- Nhắn "theo dõi giúp mình thói quen đọc sách" → Bơ thêm thói quen (tối đa 10). Mỗi ngày kể "đọc sách xong rồi" → Bơ đánh dấu, khen khi giữ chuỗi dài, tối chưa làm thì nhắc nhẹ.
- Nút **"Thói quen"**: ô vuông đánh dấu hôm nay, "chuỗi 5 ngày · 6/7 ngày", thêm/xóa. Có trong bản sao lưu.
- 236 test qua hết.

## 2026-10-11 – Giai đoạn 37 xong: rà soát lần 17
- Sửa lỗi: thói quen có dấu ngoặc trong tên ("Uống nước (2 lít)") thì Bơ không đánh dấu được. Sao lưu/khôi phục thói quen đã kiểm tra kỹ.
- 237 test qua hết.

**Tân cần thử (giai đoạn 37):** "theo dõi giúp mình thói quen uống 2 lít nước" → "uống đủ nước rồi nè" → bấm "Thói quen" xem đã tích chưa.

## 2026-10-11 – Giai đoạn 38: tài liệu & cổng thiết bị
- Cổng thiết bị `/api/thiet-bi/thoi-quen` (thói quen cho màn hình nhỏ), ghi trong THIET_BI.md.
- Nút "?" → "Bơ làm được gì?" thêm: nhắc thứ 2–6 / hằng tháng, đếm ngược Tết, nhật ký, thói quen, lịch điện thoại, tự sao lưu.
- SU_CO.md thêm 5 sự cố (khôi phục bản tự sao lưu, lịch điện thoại, nhật ký sai, thói quen không tích).
- 238 test qua hết.

## 2026-10-11 – Giai đoạn 38: nhắc thói quen buổi tối
- Từ 20:30, nếu web (hoặc thiết bị) đang mở và còn thói quen chưa làm, Bơ nhắn một câu: "Hôm nay chưa thấy bạn kể đọc sách. Đừng để đứt chuỗi 3 ngày nha!" — mỗi ngày một lần, câu soạn sẵn nên **không tốn tiền API**. Đổi giờ bằng `NHAC_THOI_QUEN` trong `.env` (để trống = tắt).
- 240 test qua hết.

## 2026-10-11 – Giai đoạn 38 xong: rà soát lần 18
- `NHAC_THOI_QUEN` nhận cả "20h30", "20h"; giờ sai (25:00...) thì nút "?" → Tình trạng báo rõ thay vì im lặng tắt.
- Cổng thiết bị `/api/thiet-bi/nhac` có thêm `"loai"` ("nhac" = nên kêu chuông, "thoi_quen" = chỉ nói).
- Tên thói quen viết hoa ("IELTS") giữ nguyên trong câu nhắc.
- 242 test qua hết.
- Bộ chấm điểm `python -m app.thu_tinh_cach` thêm tình huống "nhờ theo dõi thói quen" (26 tình huống). 243 test qua hết.

**Tân cần thử (giai đoạn 38):** chạy `python -m app.thu_tinh_cach` với API key thật, gửi điểm + câu trả lời lạ vào `FEEDBACK.md`.
- Giờ nhắc thói quen chỉnh được trong nút "?" → **Cài đặt** (gõ "21h" hay "21:00" đều được, để trống = tắt). 244 test qua hết.

## 2026-10-11 – Giai đoạn 39: trả lời nhanh không tốn API
- Hỏi ngắn **"mấy giờ rồi?", "hôm nay thứ mấy / ngày mấy âm?", "còn mấy ngày nữa Tết?", "mình còn việc gì cần làm?"** → Bơ trả lời ngay bằng câu soạn sẵn, **không gọi API** (nhanh hơn, không tốn tiền, vẫn trả lời được khi hết ngân sách). Gõ không dấu cũng được.
- Chỉ áp dụng khi CẢ tin nhắn là câu hỏi đó; câu dài hơn ("mấy giờ rồi mà mình chưa ngủ được") vẫn để AI trả lời tự nhiên. Tắt bằng `TRA_LOI_NHANH=0` trong `.env`.
- 271 test qua hết.
- Nút "?" → "Bơ làm được gì?" có mục **Hỏi nhanh, miễn phí**; mục **Tình trạng** báo "tháng này Bơ tự trả lời N câu, không tốn API". SU_CO.md thêm cách tắt. 272 test qua hết.

## 2026-10-11 – Giai đoạn 39 xong: rà soát lần 19
- Sửa lỗi nhận nhầm: "mấy giờ?", "mấy giờ đi?" (hỏi giờ hẹn) giờ để AI trả lời; chỉ "mấy giờ rồi", "bây giờ mấy giờ" mới trả lời nhanh. Câu than "việc gì phải làm thế" không còn bị hiểu thành hỏi danh sách việc.
- "Hôm nay ngày gì?" (thường hỏi dịp lễ) để AI trả lời; hỏi "hôm nay ngày mấy" vào ngày lễ thì Bơ nói luôn lễ gì. Mùng 2–10 Tết hỏi "còn mấy ngày Tết" → "Đang mùng 2 Tết mà!".
- Hiểu thêm "mấy h rồi", "mấy giờ r", "thứ mấy rồi", "còn bao lâu nữa Tết", "có việc gì cần làm không".
- Câu trả lời nhanh không tính vào giới hạn `DAILY_LIMIT` nữa (vì miễn phí).
- 292 test qua hết.

**Tân cần thử (giai đoạn 39):** hỏi Bơ "mấy giờ rồi?", "hôm nay ngày mấy âm?", "còn mấy ngày nữa Tết?" — trả lời ngay lập tức; bấm "?" → Tình trạng xem dòng "Trả lời nhanh".

## 2026-10-11 – Giai đoạn 40: thói quen 30 ngày
- Nút **"Thói quen"**: mỗi thói quen có **30 ô vuông** (30 ngày qua, ô viền vàng là hôm nay, ô xanh là đã làm). Quên tích hôm nào thì **bấm ô ngày đó** để tích bù / bỏ tích. Dưới ô ghi "12/30 ngày · chuỗi dài nhất 9 ngày".
- 293 test qua hết; đã chụp màn hình kiểm tra trên khổ điện thoại.
- Kể **"hôm qua mình có đọc sách mà quên báo"** → Bơ tích bù vào hôm qua (chuỗi ngày không bị đứt). Bơ cũng biết thói quen nào hôm qua chưa làm.
- Bộ chấm điểm `python -m app.thu_tinh_cach`: thêm tình huống "kể bù thói quen hôm qua" (27 tình huống); khi chấm thì tắt trả lời nhanh để chấm đúng câu của AI. 295 test qua hết.
- Hỏi nhanh **"thói quen hôm nay?"** / "mình còn thói quen nào chưa làm?" → Bơ trả lời ngay (miễn phí): đã xong gì, còn gì, chuỗi đang giữ. 301 test qua hết.

## 2026-10-11 – Giai đoạn 40 xong: rà soát lần 20
- Sửa lỗi: bản sao lưu bị sửa tay có ngày sai dạng ("2026-10-1") làm Bơ không trả lời được nữa → giờ bỏ qua dòng hỏng.
- Thói quen mới thêm hôm nay không bị Bơ coi là "hôm qua chưa làm".
- "Thói quen là gì?" để AI trả lời (không bật danh sách thói quen).
- Web mở qua nửa đêm: ô ngày tự cập nhật khi quay lại trang; ô cũ nhất vẫn bấm được. Ô ngày dùng được bằng bàn phím (Tab tới ô hôm nay, mũi tên trái/phải) và trình đọc màn hình.
- 304 test qua hết.

**Tân cần thử (giai đoạn 40):** nút "Thói quen" → bấm một ô ngày hôm qua để tích bù; nhắn "hôm qua mình có đọc sách mà quên báo"; hỏi "thói quen hôm nay?".

## 2026-10-11 – Giai đoạn 41: hỏi nhanh thời tiết, tổng kết thói quen
- Hỏi **"hôm nay trời thế nào?", "mai có mưa không?", "bây giờ bao nhiêu độ?"** → Bơ đọc ngay dự báo đã lấy sẵn, không tốn API. Chưa đặt thành phố thì Bơ chỉ cách đặt trong Cài đặt.
- Tối Chủ nhật Bơ tổng kết tuần giờ khen/động viên thêm về thói quen.
- 313 test qua hết.
- Nút "Thói quen" ghi thêm **"tháng 10: 9 ngày"** cho từng thói quen. 315 test qua hết.

## 2026-10-11 – Giai đoạn 41 xong: rà soát lần 21
- Sửa lỗi: mất mạng qua đêm thì hỏi nhanh thời tiết đọc nhầm số liệu hôm qua → giờ chỉ đọc dự báo lấy trong 2 giờ qua, cùng ngày; cũ hơn thì Bơ nói chưa lấy được.
- Gõ sai tên thành phố → Bơ nói rõ "Không tìm thấy thành phố ..." và chỉ chỗ sửa, thay vì đổ cho mạng.
- "Mai có mua không" (mua đồ) không bị hiểu nhầm thành hỏi mưa; gõ không dấu "mai co mua khong" vẫn hiểu là hỏi mưa.
- Hiểu thêm "thời tiết thế nào", "trời có mưa không", "tối nay có mưa không", "hôm nay trời nóng không".
- 326 test qua hết.

**Tân cần thử (giai đoạn 41):** đặt thành phố trong Cài đặt rồi hỏi "hôm nay trời thế nào?", "mai có mưa không?"; xem nút "Thói quen" có "tháng 10: N ngày".

## 2026-10-11 – Giai đoạn 42: nhắc mỗi vài tiếng
- Nhắn **"cứ 2 tiếng nhắc mình uống nước"** → Bơ nhắc mỗi 2 tiếng (được 1–12 tiếng). Trong giờ yên lặng (mặc định 23h–6h) Bơ nghỉ, sáng ra nhắc tiếp. Máy tắt lâu thì không nhắc dồn.
- Sửa được trên web ("Mỗi 2 tiếng" trong ô Lặp lại). Loại nhắc này không đưa vào file lịch điện thoại (để điện thoại khỏi kêu cả đêm).
- Bộ chấm điểm thêm tình huống "nhắc mỗi 2 tiếng" (28 tình huống). SU_CO.md thêm mục. 327 test qua hết.
- Nói **"thôi khỏi nhắc uống nước nữa"** → Bơ bỏ lời nhắc đó (Bơ giờ biết danh sách lời nhắc đang có, nên cũng trả lời được "mình đang nhờ Bơ nhắc gì?"). Đổi giờ bằng lời cũng được ("đổi nhắc gọi mẹ sang 9h"). Chấm điểm thêm tình huống (29). 329 test qua hết.

## 2026-10-11 – Giai đoạn 42 xong: rà soát lần 22
- Sửa lỗi: có 2 lời nhắc cùng tên ("Uống thuốc" 8h và 20h), nói "thôi nhắc uống thuốc buổi tối" thì Bơ xóa luôn cả hai → giờ Bơ chép cả dòng có giờ "lần tới" nên chỉ bỏ đúng cái tối; nếu không rõ cái nào thì không xóa nhầm.
- Lời nhắc có ngoặc trong tên ("Họp (online)") không làm xóa nhầm lời nhắc "Họp".
- Nhắc mỗi vài tiếng: mở lại trang lúc 2h sáng (giờ yên lặng) thì Bơ không báo nữa mà để tới hết giờ yên lặng.
- Giữ nguyên: nhắn lại "cứ 2 tiếng nhắc uống nước" với giờ khác vẫn coi là trùng (để Bơ khỏi tạo lời nhắc đôi); muốn đổi giờ thì Bơ bỏ cái cũ rồi thêm cái mới.
- 332 test qua hết.

**Tân cần thử (giai đoạn 42):** "cứ 2 tiếng nhắc mình uống nước" → "thôi khỏi nhắc uống nước nữa"; thử 2 lời nhắc cùng tên khác giờ rồi bỏ một cái.

