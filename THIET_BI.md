# Nối thiết bị phần cứng với Bơ

Bộ não Bơ chạy trên máy tính. Thiết bị (ví dụ ESP32 có màn hình, loa, servo) chỉ cần:
**gửi chữ → nhận JSON → hiện mặt / cử động / nói.** Thiết bị không cần biết gì về AI.

```
[Thiết bị] --(chữ người nói)--> [Máy tính chạy Bơ] --(JSON)--> [Thiết bị: mặt + servo + loa]
```

## Bật cổng thiết bị

Trong `.env` đặt một khóa riêng (khác mật khẩu web), rồi chạy lại `run.bat`:

```
DEVICE_KEY=esp-bo-7f3a9c
```

Để trống thì cổng thiết bị tắt (trả lỗi 403). Thiết bị không cần `APP_PASSWORD`, chỉ cần khóa này.

## Hai lệnh

Mọi lệnh gửi kèm header `X-Device-Key: <khóa>`. Thêm `?khong_dau=1` nếu màn hình không hiện được chữ có dấu
("Chào Tân" → "Chao Tan", emoji bị bỏ).

### 1. Nói chuyện: `POST /api/thiet-bi/chat`

```
curl -X POST "http://192.168.1.5:8000/api/thiet-bi/chat?khong_dau=1" ^
  -H "X-Device-Key: esp-bo-7f3a9c" -H "Content-Type: application/json" ^
  -d "{\"text\": \"Bo oi hom nay troi dep qua\"}"
```

Trả về:

```json
{ "noi": "Dep that! Di dao mot vong khong?", "cam_xuc": "vui", "hanh_dong": "nhay" }
```

### 2. Chào khi vừa bật / thấy người: `POST /api/thiet-bi/chao`

Nếu có chuyện cần hỏi thăm (ví dụ hôm qua Tân kể đi tập chân) và đã lâu không nói chuyện, Bơ mở lời trước.
Không có thì trả `{"noi": null}` → thiết bị im lặng. Không tốn tiền API khi không có gì để hỏi.

### 3. Lời nhắc tới giờ: `GET /api/thiet-bi/nhac`

Thiết bị hỏi mỗi 30 giây. Có lời nhắc tới giờ (Tân nhờ "8h tối nhắc mình gọi mẹ") thì trả danh sách
`[{"noi": "Tới giờ rồi nè: gọi mẹ!", "cam_xuc": "hao_hung", "hanh_dong": "vay_tay"}]`, không có thì `[]`.
Mỗi lời nhắc chỉ báo **một lần**: nếu web và thiết bị cùng mở, nơi nào hỏi trước thì nơi đó nhận.

### 4. Việc cần làm: `GET /api/thiet-bi/viec`

Danh sách việc Tân nhờ Bơ ghi mà chưa xong (cũ → mới), ví dụ `[{"viec": "Mua sữa"}, {"viec": "Trả sách"}]`.
Màn hình nhỏ có thể hiện khi Tân hỏi "còn việc gì?" hoặc lúc rảnh. Thêm `?khong_dau=1` để bỏ dấu. Không tốn tiền API.

## Lỗi thường gặp

| Mã | Nghĩa | Thiết bị nên làm |
|----|-------|------------------|
| 200 | OK | Hiện mặt, cử động, nói |
| 401 | Sai khóa | Kiểm tra `DEVICE_KEY` |
| 403 | Cổng thiết bị đang tắt | Đặt `DEVICE_KEY` trong `.env` |
| 502 | Bộ não lỗi (mất mạng, hết tiền API…) | Hiện mặt buồn; trường `detail` có câu giải thích |

Thường Bơ trả lời trong vài giây. Khi mạng chập chờn, bộ não tự thử lại nên có thể lâu hơn nhiều. Thiết bị nên chờ 60 giây; quá thì coi như lỗi mạng (hiện mặt buồn, thử lại sau).

## Cảm xúc → khuôn mặt (gợi ý)

| `cam_xuc` | Nghĩa | Màn hình mặt |
|-----------|-------|--------------|
| `vui` | vui | mắt cong, miệng cười |
| `hao_hung` | hào hứng | miệng mở to |
| `binh_thuong` | bình thường | mắt tròn, miệng cười nhẹ |
| `suy_nghi` | đang nghĩ | mắt nhìn lên, miệng thẳng (hiện lúc chờ trả lời) |
| `ngac_nhien` | ngạc nhiên | mắt to, miệng tròn |
| `buon` | buồn | miệng úp xuống |
| `thuong` | thương, đồng cảm | mắt cong, má hồng |
| (`ngu`) | ngủ gật – do thiết bị tự bật khi lâu không ai tương tác, AI không gửi | mắt nhắm thành vạch, "z z" |

## Hành động → servo (gợi ý)

| `hanh_dong` | Cử động |
|-------------|---------|
| `khong` | đứng yên |
| `gat_dau` | servo đầu lên xuống 2 lần |
| `lac_dau` | servo đầu trái phải 2 lần |
| `nghieng_dau` | nghiêng đầu ~15° rồi về |
| `nhay` | cả thân nhún lên xuống |
| `vay_tay` | servo tay vẫy 3 lần |

## Ví dụ ESP32 (Arduino) – CHƯA thử trên máy thật

Cần thư viện **ArduinoJson**. Đây chỉ là khung để bắt đầu; phần nghe giọng nói và đọc to trên thiết bị làm sau.

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* WIFI_TEN = "ten-wifi";
const char* WIFI_MK  = "mat-khau-wifi";
const char* BO_URL   = "http://192.168.1.5:8000/api/thiet-bi/chat?khong_dau=1";
const char* BO_KHOA  = "esp-bo-7f3a9c";

void hoiBo(const String& cau) {
  HTTPClient http;
  http.begin(BO_URL);
  http.setTimeout(60000);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-Device-Key", BO_KHOA);
  JsonDocument gui;
  gui["text"] = cau;
  String body;
  serializeJson(gui, body);
  int ma = http.POST(body);
  if (ma == 200) {
    JsonDocument nhan;
    deserializeJson(nhan, http.getString());
    Serial.printf("Bo noi: %s | cam xuc: %s | hanh dong: %s\n",
                  (const char*)nhan["noi"], (const char*)nhan["cam_xuc"], (const char*)nhan["hanh_dong"]);
    // TODO: vẽ mặt theo cam_xuc, quay servo theo hanh_dong
  } else {
    Serial.printf("Loi %d\n", ma);  // TODO: hiện mặt buồn
  }
  http.end();
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_TEN, WIFI_MK);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  Serial.println("Go mot cau vao Serial Monitor de noi voi Bo");
}

void loop() {
  if (Serial.available()) {
    String cau = Serial.readStringUntil('\n');
    cau.trim();
    if (cau.length()) hoiBo(cau);
  }
}
```

Mở Serial Monitor (115200), gõ "chao Bo" → thấy câu trả lời của Bơ. Thiết bị và máy tính phải chung Wi-Fi.
