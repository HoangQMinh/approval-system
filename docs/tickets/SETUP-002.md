# [SETUP-002] DB環境構築・環境変数による設定読み込み

| | |
|---|---|
| 担当 | Dev A |
| 見積 | 3pt |
| Trạng thái | ✅ Done — PR #4, squash `dc2f8c3` (2026-10-21) |

## Ticket
**受け入れ条件 (AC)**
- [x] docker compose で PostgreSQL 16 が起動し、healthcheck が healthy になること
- [x] 接続情報は環境変数（.env）から読み込むこと。.env はコミットしない、.env.example をコミットする
- [x] DATABASE_URL 未設定時はアプリ起動時に分かりやすいエラーで停止すること
- [x] README に DB 起動手順が記載されていること

## Kết quả
- `docker-compose.yml`: `name: approval` (2 clone dùng chung container), cổng `127.0.0.1:5433:5432` (chỉ máy mình truy cập được), volume `db-data`, healthcheck `pg_isready`.
- `.env.example`, `app/config.py` (`load_config_from_env`), `create_app`: đọc env → `test_config` ghi đè → kiểm tra `DATABASE_URL` (fail fast, `RuntimeError`).
- `tests/conftest.py`: `DATABASE_URL = sqlite+pysqlite:///:memory:` (D-026). `tests/test_config.py` dùng `monkeypatch`.
- Quyết định liên quan: D-023, D-024, D-025, D-026.

## Bài học chính
- Commit ≠ push: branch chưa có `[origin/...]` trong `git branch -vv` là GitHub chưa biết.
- Code trên `main` nhầm → `git switch -c feature/...` (thay đổi chưa commit đi theo).
- Requirements: pin bằng `==`, sửa xong cài lại từ chính file.
- Mô tả PR phải đúng sự thật (PR này KHÔNG kết nối DB — đó là SETUP-005).
- Sau merge, dọn branch bằng D-027 (stash → switch → pull → pop).
