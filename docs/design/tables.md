# テーブル定義

> Tạo bảng bằng `flask --app app init-db` cho tới khi có ticket migration (D-035).
> Giá trị mã lưu bằng tiếng Anh, nhãn tiếng Nhật chỉ ở tài liệu/hiển thị (D-036).

## users — 社員
| Cột | Kiểu | Null | Ràng buộc / Ghi chú |
|---|---|---|---|
| id | integer | NO | PK |
| employee_code | varchar(20) | NO | UNIQUE — mã nhân viên |
| name | varchar(100) | NO | |
| manager_id | integer | YES | FK → users.id. Cấp trên trực tiếp; NULL = không có cấp trên |
| created_at | timestamptz | NO | default now() |

Dữ liệu mẫu (`flask --app app seed-users`, chạy nhiều lần không bị trùng):
| employee_code | name | cấp trên |
|---|---|---|
| M001 | Tanaka Taro | — |
| E001 | Sato Hanako | M001 |
| E002 | Suzuki Ichiro | M001 |

## leave_requests — 休暇申請
| Cột | Kiểu | Null | Ràng buộc / Ghi chú |
|---|---|---|---|
| id | integer | NO | PK |
| applicant_id | integer | NO | FK → users.id — người nộp |
| approver_id | integer | NO | FK → users.id — cấp trên lúc nộp |
| leave_type | varchar(20) | NO | CHECK IN (`annual_paid`=年次有給休暇, `special`=特別休暇, `substitute`=振替休日) — 質問票 No.1 |
| period_type | varchar(10) | NO | CHECK IN (`full_day`=終日, `am`=午前, `pm`=午後) — No.4 |
| start_date | date | NO | CHECK start_date <= end_date — No.3 |
| end_date | date | NO | CHECK (period_type = 'full_day' OR start_date = end_date) — No.4 |
| reason | varchar(200) | YES | Không bắt buộc, tối đa 200 — No.2 |
| status | varchar(20) | NO | CHECK IN (`pending`, `approved`, `returned`, `withdrawn`) — xem state-transition.md |
| created_at | timestamptz | NO | default now() |
| updated_at | timestamptz | NO | default now(), cập nhật khi sửa |

Quy tắc **không** đặt ở DB (kiểm tra ở tầng ứng dụng — LEAVE-004):
- Tối đa 30 ngày liên tục (No.3)
- start_date ≥ hôm qua (No.5)
- Không trùng thời gian với đơn `pending`/`approved` khác của cùng người nộp (No.11)

## approval_histories — 承認履歴
| Cột | Kiểu | Null | Ràng buộc / Ghi chú |
|---|---|---|---|
| id | integer | NO | PK |
| leave_request_id | integer | NO | FK → leave_requests.id |
| actor_id | integer | NO | FK → users.id — người thực hiện |
| action | varchar(20) | NO | CHECK IN (`submit`, `approve`, `return`, `resubmit`, `withdraw`) |
| comment | text | YES | Bắt buộc khi `return` (kiểm tra ở ứng dụng) |
| acted_at | timestamptz | NO | default now() |
