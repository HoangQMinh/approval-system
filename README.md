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
