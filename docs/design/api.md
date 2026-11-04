# API一覧

## Quy ước chung
- Body request/response: JSON. Lỗi theo D-017: `{"error": "<tên lỗi HTTP>", "message": "..."}`; lỗi 400 có thêm `"details": [{"field": "...", "message": "..."}]` (D-037).
- **Xác thực đơn giản (tạm thời, D-034):** header `X-User-Id: <users.id>`. Chỉ dùng cho môi trường dev; thay bằng đăng nhập thật ở sprint sau.
  - Thiếu header → **401** `X-User-Id header is required.`
  - Không phải số ASCII / không tồn tại → **401** `Invalid X-User-Id.` (không phân biệt 2 trường hợp — tránh dò ID)

| Mã | Khi nào (D-037) |
|---|---|
| 400 | Dữ liệu không hợp lệ (thiếu field, sai định dạng, vi phạm quy tắc) |
| 401 | Thiếu / sai `X-User-Id` |
| 403 | Đã xác thực nhưng không có quyền với tài nguyên |
| 404 | Không tồn tại (hoặc không được phép biết là có tồn tại) |
| 409 | Chuyển trạng thái không hợp lệ, trùng thời gian |

## Sprint 1
| Method | Path | Ai | Mô tả | Thành công | Ticket |
|---|---|---|---|---|---|
| GET | `/health` | — | Kiểm tra sống + DB | 200 | (đã có) |
| GET | `/me` | Mọi user đã xác thực | Thông tin user hiện tại: `id`, `employee_code`, `name`, `manager_id` (D-043) | 200 | LEAVE-002 |
| POST | `/leave-requests` | Người nộp | Tạo và nộp đơn → `pending`, ghi history `submit` | 201 + đơn vừa tạo | LEAVE-003, LEAVE-004 |
| GET | `/leave-requests` | Người nộp | Danh sách đơn **của mình**, mới nhất trước | 200 | LEAVE-005 |
| GET | `/leave-requests/<id>` | Người nộp hoặc approver của đơn | Chi tiết đơn | 200 | LEAVE-005 |

Body `POST /leave-requests`:
```json
{
  "leave_type": "annual_paid",
  "period_type": "full_day",
  "start_date": "2026-11-02",
  "end_date": "2026-11-03",
  "reason": "私用のため"
}
```

## Sprint 2 (dự kiến — chưa chốt chi tiết)
| Method | Path | Ai | Mô tả |
|---|---|---|---|
| POST | `/leave-requests/<id>/approve` | Approver | `pending` → `approved` |
| POST | `/leave-requests/<id>/return` | Approver | `pending` → `returned` (comment bắt buộc) |
| PUT | `/leave-requests/<id>` | Người nộp | Sửa + nộp lại: `returned` → `pending` |
| POST | `/leave-requests/<id>/withdraw` | Người nộp | `pending`/`returned` → `withdrawn` |
| GET | `/approvals` | Cấp trên | Đơn của cấp dưới trực tiếp (lọc theo status) |
| GET | `/leave-requests/<id>/histories` | Người nộp / approver | Lịch sử xử lý |
