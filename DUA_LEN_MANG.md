# Dùng Bơ khi ra ngoài (không chung Wi-Fi)

Bơ vẫn chạy trên máy tính ở nhà. Ta chỉ mở một "đường hầm" để điện thoại ở ngoài nói chuyện được với máy đó.
**Máy tính ở nhà phải bật và đang chạy `run.bat`.**

## Bước 0 (bắt buộc): đặt mật khẩu

Mở file `.env`, điền một mật khẩu khó đoán:

```
APP_PASSWORD=bo-cua-tan-2026
```

Chạy lại `run.bat`. Từ giờ mở web sẽ hiện ô đăng nhập: **tên gõ gì cũng được**, mật khẩu là cái vừa đặt.
Không có mật khẩu thì ai biết đường link cũng chat được với Bơ, đọc được trí nhớ và tiêu tiền API của Tân.

## Cách 1 (khuyên dùng): Tailscale – mạng riêng, chỉ máy của Tân vào được

*Tailscale* là ứng dụng nối các thiết bị của mình thành một mạng riêng, như chung Wi-Fi dù ở đâu. Gói cá nhân miễn phí.

1. Tạo tài khoản ở https://tailscale.com (đăng nhập bằng Google cũng được).
2. Cài Tailscale trên **máy tính** và trên **iPhone** (App Store), đăng nhập cùng một tài khoản.
3. Trên máy tính, mở Tailscale xem địa chỉ của máy (dạng `100.x.y.z`).
4. Trên iPhone (bật Tailscale), mở `http://100.x.y.z:8000`.

Ưu: không ai ngoài thiết bị của Tân thấy được Bơ. Nhược: mỗi thiết bị muốn dùng phải cài Tailscale.

## Cách 2: Cloudflare Tunnel – có đường link công khai

*Cloudflare Tunnel* (chương trình `cloudflared`) tạo một đường link `https://...` ai cũng mở được, không cần mở cổng modem.

1. Tải `cloudflared` cho Windows ở trang hướng dẫn của Cloudflare (tìm "cloudflared download").
2. Trong lúc `run.bat` đang chạy, mở một cửa sổ cmd khác và gõ:
   ```
   cloudflared tunnel --url http://localhost:8000
   ```
3. Nó in ra một đường link dạng `https://ten-ngau-nhien.trycloudflare.com` → mở trên điện thoại.

Ưu: không cần cài gì trên điện thoại. Nhược: link đổi mỗi lần chạy (muốn link cố định thì cần tài khoản + tên miền),
và link công khai nên **bắt buộc phải có APP_PASSWORD**.

## Không nên

- Mở cổng (port forwarding) trên modem: dễ cấu hình sai, lộ máy ra internet.
- Gửi đường link cho người khác kèm mật khẩu.

## Gặp lỗi

- Không vào được: kiểm tra máy tính còn bật, `run.bat` còn chạy, Windows Firewall cho phép Python.
- Hỏi mật khẩu mãi: gõ đúng mật khẩu trong `.env` (phân biệt hoa/thường), rồi thử tab ẩn danh.
