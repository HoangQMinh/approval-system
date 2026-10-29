<!-- Title: [TICKET-ID] タイトル（チケットと同じ） -->

## 概要
<!-- TODO: PR này làm gì (1–2 câu). KHÔNG copy từ PR khác -->

## 変更内容
<!-- TODO: liệt kê theo thành phần; thay đổi ngoài phạm vi ticket ghi rõ -->

## テスト結果
<!-- TODO: dán output thật -->

## 影響範囲
<!-- requirements / .env / docker-compose thay đổi? Không có → 特になし -->

## レビュー観点
<!-- Điểm muốn reviewer soi kỹ, hoặc 特になし -->

## 対象外（別チケット）
<!-- Mã ticket, hoặc 特になし -->

## 提出前チェック

- [ ] Title có đúng mã ticket của PR này
- [ ] `pytest` / `ruff check` / `ruff format --check` / `mypy` đều đạt
- [ ] Docstring đã cập nhật nếu hàm đổi hành vi
- [ ] README đã cập nhật nếu cách cài / chạy / API thay đổi
- [ ] `.env.example` đã cập nhật nếu thêm/đổi biến môi trường
- [ ] `git stash list` trống, không còn thay đổi chưa commit
- [ ] Mỗi commit có tiền tố `[TICKET-ID]`
