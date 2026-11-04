# Sprint 1 — 休暇申請（申請・照会）

| | |
|---|---|
| Thời gian | 2026-10-26 → 2026-11-06 (2 tuần) |
| **Mục tiêu sprint** | Nhân viên **tạo được đơn nghỉ (có kiểm tra hợp lệ) và xem được đơn của mình** qua API; CI chạy trên mọi PR |
| Ngoài phạm vi | Duyệt / trả lại / nộp lại / rút đơn, màn hình cấp trên, lịch sử (→ Sprint 2) |
| Tài liệu | `docs/design/`, `docs/qa/sprint1-qa.md` |

## Vì sao không làm hết luồng nghiệp vụ trong Sprint 1
Sprint 0 làm ~13 SP trong ~3 tuần (gồm học). TL nhận ~16 SP cho Sprint 1, ưu tiên **lát cắt dùng được trọn vẹn** (tạo + xem) thay vì làm dở mọi thứ. Trả lời PM: Sprint 1 giao "申請・照会"; 承認・差戻し ở Sprint 2.

## Backlog Sprint 1 (thứ tự ưu tiên)

| Đợt | Ticket | Nội dung | Dev | SP | Phụ thuộc |
|---|---|---|---|---|---|
| 1 | SETUP-006 | PR template có checklist (Try T1, T3) | B | 1 | — |
| 1 | SETUP-007 | CI GitHub Actions (Try T2) | **TL** (đổi 11-01, D-041) | 2 (không tính vào SP của dev) | sau SETUP-006 |
| 1 | LEAVE-001 | Model 3 bảng + `flask init-db` + `seed-users` | A | 3 | — |
| 2 | LEAVE-002 | Xác thực đơn giản `X-User-Id` (401) + `GET /me` + session theo request | B | 2 | LEAVE-001 (Bước 1 làm trước được — giao sớm 11-01 vì SETUP-007 chuyển cho TL) |
| 2 | LEAVE-003 | `POST /leave-requests` — tạo đơn tối thiểu (201, history `submit`) | A | 3 | LEAVE-001, LEAVE-002 (hợp đồng D-038) |
| 3 | LEAVE-004 | Kiểm tra hợp lệ khi tạo đơn (400 + details, 409 trùng ngày) | A | 3 | LEAVE-003 |
| 3 | LEAVE-005 | `GET /leave-requests`, `GET /leave-requests/<id>` (403/404) | B | 2 | LEAVE-002, LEAVE-001 |
| | | | | **16** | |

## Thứ tự merge đợt 1
1. **SETUP-006** (nhỏ, các PR sau dùng template ngay)
2. **SETUP-007** (từ đây mọi PR có CI)
3. **LEAVE-001** — PR đầu tiên được CI kiểm. Dev A mở Draft sớm, merge `main` về sau khi 007 vào.

Ticket đợt 2–3 sẽ được TL tạo file khi giao (D-030).
