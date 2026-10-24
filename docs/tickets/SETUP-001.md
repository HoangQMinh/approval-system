# [SETUP-001] プロジェクト雛形作成

| | |
|---|---|
| 担当 | Minh (trước khi chia Dev A/B) |
| 見積 | 2pt |
| Trạng thái | ✅ Done — PR #1, squash `be464e7` (2026-10-10) |

## Ticket
**背景**: 開発開始に向けて Flask アプリの雛形を作成する。

**受け入れ条件 (AC)**
- [x] app factory `create_app()`、Blueprint `health_bp`
- [x] GET /health → 200 / `{"status": "ok"}`
- [x] 未定義パス（/healthz）→ 404
- [x] pytest 導入・全件パス
- [x] `.gitignore`、README の手順で環境構築できること

## Kết quả
- Cấu trúc: `app/__init__.py` (factory), `app/routes/health.py`, `tests/conftest.py`, `tests/test_health.py`, `pytest.ini`, `requirements*.txt`.
- Quyết định liên quan: D-001 → D-007.

## Bài học chính
- README phải là lệnh copy-paste chạy được; kiểm chứng bằng cách chạy thử trên máy sạch (`C:\temp`).
- Gặp lỗi type hint thì sửa theo dòng `got ...` của mypy, không xóa type hint.
- Commit chưa push thì `--amend`; đã push thì commit mới.
- Squash merge → branch local phải xóa bằng `-D` sau khi xác minh `main` đã có code.
