# approval-system

## Tổng quan

Hệ thống xét duyệt đơn nghỉ phép, chi phí của nhân viên lên cấp trên phê duyệt, xử lý.

## Yêu cầu môi trường

Python 3.12+

## Cài đặt

```cmd
git clone https://github.com/HoangQMinh/approval-system.git
cd approval-system
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

## Chạy ứng dụng

**CMD 1 — Khởi động server:**

```cmd
flask --app app run --debug
```

**CMD 2 — Mở một CMD khác để gọi API:**

```cmd
curl -i http://127.0.0.1:5000/health
```

## Chạy test

```cmd
pytest -v
```

## Định dạng lỗi API

Khi API phát sinh lỗi HTTP `404`, `405` hoặc `500`, server trả về response dạng JSON với cấu trúc sau:

```json
{
  "error": "Not Found",
  "message": "The requested URL was not found on the server."
}
```

HTTP status code được trả về trong **HTTP response status line**, không nằm trong JSON body.

### Ví dụ: HTTP 404 Not Found

Ví dụ gọi một URL không tồn tại:

```bash
curl -i http://127.0.0.1:5000/not-found
```

Response:

```http
HTTP/1.1 404 NOT FOUND
Content-Type: application/json

{
  "error": "Not Found",
  "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
}
```

Nội dung `message` thực tế phụ thuộc vào lỗi và cấu hình của Flask.

### Các HTTP status được xử lý

| Status code | Ý nghĩa |
|---|---|
| `404 Not Found` | URL hoặc tài nguyên được yêu cầu không tồn tại. |
| `405 Method Not Allowed` | HTTP method không được hỗ trợ bởi endpoint. |
| `500 Internal Server Error` | Xảy ra lỗi không mong đợi trong server. |

Các lỗi trên được trả về theo cùng cấu trúc JSON:

- `error`: tên lỗi HTTP.
- `message`: mô tả lỗi.

**Lưu ý bảo mật:** Với lỗi `500`, response không cung cấp chi tiết exception nội bộ, thông tin database, đường dẫn file hoặc stack trace. Chi tiết lỗi được ghi log ở phía server để phục vụ debug.
