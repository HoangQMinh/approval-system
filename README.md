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

### Cập nhật dependencies

Sau khi `git pull` hoặc merge code từ branch khác, nếu có thay đổi trong các file `requirements*.txt`, chạy lại lệnh sau để cài đặt hoặc cập nhật dependencies:

```cmd
pip install -r requirements-dev.txt
```

Thực hiện bước này trước khi chạy ứng dụng hoặc các lệnh kiểm tra code.

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

