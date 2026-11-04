# Phân vai trong team (ai làm gì)

> Sinh ra từ retro Sprint 0 (Problem của Minh: "đôi lúc nhầm việc của dev và TL").
> Quy ước: việc của TL mà Minh **thao tác thay** (do TL không có quyền vào GitHub/máy) sẽ được ghi rõ **[Thay TL]** trong tin nhắn và ticket.

| Việc | Dev (Minh — Dev A / Dev B) | TL (AI) | Ghi chú |
|---|---|---|---|
| Hỏi khách / 質問票 | — | ✅ | D-021. Dev hỏi TL, không hỏi khách |
| Viết tài liệu thiết kế (`docs/design/`) | Đọc | ✅ Viết | D-022 |
| Chia ticket, ước lượng, thứ tự merge | — | ✅ | D-015, D-016 |
| Viết / cập nhật file ticket (`docs/tickets/`) | Đọc, hỏi lại | ✅ | D-030 |
| Ghi team-log | — | ✅ (Dev A commit hộ) | D-011 |
| Đọc ticket + link, hỏi chỗ chưa rõ **trước khi code** | ✅ | Trả lời + sửa ticket | Hỏi trong chat với tiền tố ❓ |
| Code, test, chạy 4 công cụ | ✅ | — | |
| Commit, push, mở PR, viết PR body | ✅ | — | |
| Review PR, approve | Review chéo (khi được yêu cầu) | ✅ | |
| Sửa theo review | ✅ | — | |
| Bấm merge (squash) | ✅ (sau khi TL approve) | Quyết định thứ tự | |
| Dọn branch sau merge | ✅ | — | D-027 |
| Thông báo team sau merge có 影響範囲 | — | ✅ 📢 | D-028 |
| Tag + GitHub Release | **[Thay TL]** | ✅ quyết định | D-031 |
| Cấu hình GitHub (ruleset, settings) | **[Thay TL]** | ✅ quyết định | D-013 |
| Test hộp đen, báo bug | — | 🔍 QA (AI) | |
| Phân loại bug, giao người sửa | — | ✅ | D-032 |
| Retro: góp ý KPT | ✅ | ✅ tổng hợp, chốt Try | |
