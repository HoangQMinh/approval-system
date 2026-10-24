# approval-system

## Tổng quan

Hệ thống xét duyệt đơn nghỉ phép, chi phí của nhân viên lên cấp trên phê duyệt, xử lý.

## Yêu cầu môi trường

- Python 3.12+
- Docker Desktop

## Cài đặt

```cmd
git clone https://github.com/HoangQMinh/approval-system.git
cd approval-system
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

### Cập nhật dependencies

Sau khi `git pull` hoặc merge code từ branch khác, nếu có thay đổi trong các file `requirements*.txt`, chạy lại lệnh sau để cài đặt hoặc cập nhật dependencies:

```cmd
pip install -r requirements-dev.txt
```

Thực hiện bước này trước khi chạy ứng dụng hoặc các lệnh kiểm tra code.

## Khởi động DB

### 1. Chuẩn bị

- Mở Docker Desktop và đợi Docker khởi động hoàn tất.
- Tại thư mục gốc của project, tạo file `.env` từ `.env.example` (chỉ cần thực hiện lần đầu).

```cmd
copy .env.example .env
```

- `DATABASE_URL` có thêm timeout kết nối 3 giây. Người đã có .env cũ phải tự thêm, sửa xong phải khởi động lại Flask
- `DATABASE_URL` dùng 127.0.0.1 thay vì localhost vì windows có thể localhost thử IPv6 trước nên sẽ chậm hơn

### 2. Khởi động PostgreSQL

```cmd
docker compose up -d
```

### 3. Kiểm tra trạng thái

```cmd
docker compose ps
```

Đợi container `db` có trạng thái `Up` và health check chuyển sang `healthy`.

Có thể kiểm tra kết nối database bằng lệnh:

```cmd
docker compose exec db psql -U approval -d approval -c "SELECT 1"
```

Nếu thành công, kết quả truy vấn sẽ trả về `1`.

### 4. Dừng DB

Khi không cần sử dụng database nữa:

```cmd
docker compose down
```

Lệnh này dừng và xóa container/network do Compose quản lý, nhưng **giữ lại dữ liệu trong named volume**.

**Lưu ý:** Không chạy `docker compose down -v` trừ khi muốn xóa cả volume chứa dữ liệu PostgreSQL. Dữ liệu database sẽ bị mất.

## Chạy ứng dụng

**CMD 1 — Khởi động server:**

```cmd
flask --app app run --debug
```

**CMD 2 — Mở một CMD khác để gọi API và kiểm tra DB:**

```cmd
curl -i http://127.0.0.1:5000/health
```
DB tắt sẽ trả về lỗi 503

## Chạy test

```cmd
pytest -v
```

## Kiểm tra code

Trước khi mở Pull Request (PR), Developer **phải chạy cả 3 lệnh sau** và xử lý các lỗi phát hiện được:

```cmd
ruff check .
ruff format --check .
mypy
```

- `ruff check .`: kiểm tra các quy tắc code.
- `ruff format --check .`: kiểm tra định dạng code, không tự sửa file.
- `mypy`: kiểm tra kiểu dữ liệu.

Nếu có lỗi, sửa code hoặc chạy các lệnh tự động sửa phù hợp, sau đó chạy lại cả 3 lệnh để xác nhận kết quả.

### Sửa lỗi và định dạng code

Nếu Ruff báo lỗi hoặc code chưa đúng định dạng, chạy:

```cmd
ruff check --fix .
ruff format .
```

mypy không có lệnh tự sửa, lỗi mypy phải sửa tay.

Kiểm tra các thay đổi trước khi commit:

```cmd
git diff
pytest -v
```

Sau khi xác nhận các thay đổi hợp lệ, commit code đã được chỉnh sửa.

## Định dạng lỗi API

Khi API phát sinh lỗi HTTP `404`, `405`, `500` hoặc `503` server trả về response dạng JSON với cấu trúc sau:

```json
{
  "error": "Not Found",
  "message": "The requested URL was not found on the server."
}
```

405 có kèm header `Allow` liệt kê method được phép.

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
| `503 Service Unavailable` | Xảy ra lỗi không kết nối được với database. |

Các lỗi trên được trả về theo cùng cấu trúc JSON:

- `error`: tên lỗi HTTP.
- `message`: mô tả lỗi.

**Lưu ý bảo mật:** Với lỗi `500`, response không cung cấp chi tiết exception nội bộ, thông tin database, đường dẫn file hoặc stack trace. Chi tiết lỗi được ghi log ở phía server để phục vụ debug.
