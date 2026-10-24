# [SETUP-005] DB接続処理の実装・ヘルスチェックへのDB確認追加

| | |
|---|---|
| 担当 | Dev B (clone `approval-system-devb`, cửa sổ 🔴) |
| Branch | `feature/SETUP-005` (tạo từ `main` sau khi #4 merge) |
| 見積 | 3pt |
| Trạng thái | ✅ Done — PR #5, squash `9357e6f` (2026-10-24) |

---

## Ticket

**背景**: SETUP-002 で DB 環境と `DATABASE_URL` の読み込みが整った。アプリから DB に接続し、ヘルスチェックで DB の状態も確認できるようにする。

**受け入れ条件 (AC)**
- [ ] `DATABASE_URL`（D-024）から DB 接続を初期化すること
- [ ] GET /health は DB に接続できる場合 200 / `{"status": "ok"}`
- [ ] DB に接続できない場合 503 / JSON（D-017 形式）、詳細はログのみ
- [ ] DB が応答しない場合も数秒以内に 503 を返すこと（接続タイムアウト：D-029）※2026-10-22 追加
- [ ] テストが追加され、全件パスすること（実DB不要：D-026）

**参照**: D-017（エラー形式）, D-023（SQLAlchemy + psycopg）, D-024（`DATABASE_URL` 契約）, D-026（テストDB）, D-029（`127.0.0.1` + `connect_timeout`）

---

## 📚 Phần học

| Khái niệm mới | Bên OutSystems |
|---|---|
| **Engine** (kèm connection pool) | **Database Connection** trong Service Center |
| `with engine.connect() as connection:` | OutSystems tự mở/đóng kết nối mỗi request; `with` đảm bảo kết nối luôn được trả lại, kể cả khi lỗi |
| `SQLAlchemyError` | Exception Handler loại **Database Exception** |
| `abort(503, ...)` | **Raise Exception** → Global Exception Handler (handler của SETUP-003 tự trả JSON) |
| `current_app` / `app.extensions` | Như đọc Site Property ở bất kỳ action nào mà không cần truyền tham số |
| `connect_timeout` | **Timeout** của Database Connection |
| `logger.exception("...")` | Ghi vào **Service Center → Error Log** kèm stack |

### Bước 1 — Module kết nối DB

1. `requirements.txt` (runtime): `SQLAlchemy==<version>`, `psycopg[binary]==<version>`.
   - `pip show` dùng **tên gói**: `pip show SQLAlchemy psycopg psycopg-binary`.
   - Sửa xong: `pip install -r requirements-dev.txt` phải không lỗi (kiểm thêm `pip check`, venv sạch nếu cần).
2. `app/db.py` (mới):

```python
"""Kết nối database bằng SQLAlchemy."""

# TODO(1): import Flask, current_app từ flask; Engine, create_engine từ sqlalchemy


def init_db(app: Flask) -> None:
    """Tạo engine từ DATABASE_URL và gắn vào app."""
    # TODO(2): tạo engine từ app.config["DATABASE_URL"], thêm pool_pre_ping=True
    # TODO(3): lưu engine vào app.extensions["db_engine"]


def get_engine() -> Engine:
    """Lấy engine của app hiện tại."""
    # TODO(4): lấy engine từ current_app.extensions["db_engine"] và return
    ...
```

3. `app/__init__.py`: gọi `init_db(app)` **sau** bước kiểm tra `DATABASE_URL`, **trước** đăng ký blueprint; import bên trong hàm (D-003). Cập nhật docstring.
4. ~~`tests/conftest.py`: thêm `DATABASE_URL`~~ — **bỏ** (đã có trong `main` từ SETUP-002).

📝 README: KHÔNG.

### Bước 2 — `/health` kiểm tra DB

`app/routes/health.py`:

```python
@health_bp.get("/health")
def health_check() -> tuple[Response, int]:
    """Trả về trạng thái sống của ứng dụng và kết nối DB."""
    # TODO(1): try: with get_engine().connect() as connection:
    #               connection.execute(text("SELECT 1"))
    # TODO(2): except SQLAlchemyError:
    #               current_app.logger.exception("<message cố định>")   ← không f-string, không chèn exception
    #               abort(503, description="Database is unavailable.")
    return jsonify({"status": "ok"}), 200
```

`tests/test_health.py` — test mới **tự tạo app riêng**, không dùng fixture `client`/`app` (đó là app SQLite):

```python
def test_health_returns_503_when_database_is_unreachable():
    # TODO: app = create_app({... "DATABASE_URL": "postgresql+psycopg://u:p@127.0.0.1:1/db?connect_timeout=1"})
    # TODO: response = app.test_client().get("/health")
    # TODO: 503, is_json, body không None, body["error"] == "Service Unavailable"
    ...
```

- Phải có `?connect_timeout=1`: trên Windows, kết nối tới cổng đóng không bị từ chối ngay → không có timeout sẽ chờ mặc định **130s** của psycopg.
- Mutation: bỏ `try/except` → test 503 phải đỏ.

`.env` **và** `.env.example` (D-029):

```
DATABASE_URL=postgresql+psycopg://approval:approval@127.0.0.1:5433/approval?connect_timeout=3
```

Sửa `.env` xong phải **khởi động lại Flask** (`.env` chỉ được đọc lúc khởi động; `--debug` không theo dõi `.env`). Kiểm tra: `flask --app app shell` → `app.config["DATABASE_URL"]`, `get_engine().url`.

📝 README: CÓ
- **Yêu cầu môi trường**: dạng danh sách `- Python 3.12+` / `- Docker Desktop`.
- **Khởi động DB** (sau block `copy .env.example .env`): `DATABASE_URL` dùng `127.0.0.1` (lý do: Windows thử IPv6 trước), có `connect_timeout=3`, sửa `.env` phải khởi động lại Flask.
- **Chạy ứng dụng**: `/health` kiểm tra cả DB; DB tắt → 503.
- **Định dạng lỗi API**: thêm dòng `503 Service Unavailable` vào bảng status.

### Bước 3 — Công cụ, commit, PR

Chạy: `pytest -v`, `ruff check .`, `ruff format --check .`, `mypy`.

Commit gợi ý:
1. `[SETUP-005] Add SQLAlchemy database connection` — `requirements.txt`, `app/db.py`, `app/__init__.py`
2. `[SETUP-005] Check database connection in health endpoint` — `app/routes/health.py`, `tests/test_health.py`
3. `[SETUP-005] Use 127.0.0.1 and connect timeout for DATABASE_URL` — `.env.example`, `README.md`

**Không đụng `docs/team-log.md`** (D-011). PR bình thường (không Draft). Mục 影響範囲:

```markdown
## 影響範囲
- requirements.txt 変更（SQLAlchemy, psycopg）→ `pip install -r requirements-dev.txt` を再実行
- `.env.example` の `DATABASE_URL` を変更（`127.0.0.1` + `connect_timeout=3`）→ 各自 `.env` を修正し Flask を再起動
```

📝 README: KHÔNG thêm.

### Cú pháp

| Cú pháp | Ghi chú |
|---|---|
| `create_engine(url, pool_pre_ping=True)` | Ping kết nối cũ trong pool trước khi dùng |
| `app.extensions["key"] = value` | Chỗ chuẩn của Flask để gắn đối tượng dùng chung vào app |
| `with ... as connection:` | Context manager — tự đóng/trả kết nối |
| `text("SELECT 1")` | SQL thuần qua SQLAlchemy |
| `except SQLAlchemyError:` | Bắt mọi lỗi DB của SQLAlchemy |
| `abort(503, description=...)` | Ném `HTTPException` → handler SETUP-003 trả JSON |
| `current_app.logger.exception("msg")` | Log ERROR kèm traceback; message cố định |

---

## Definition of Done
- [ ] 200 khi DB OK, 503 khi DB chết, đúng JSON D-017
- [ ] DB không phản hồi → 503 trong vài giây (không treo)
- [ ] `pytest` xanh, chạy nhanh (không có test ~130s), mutation đã làm
- [ ] 4 công cụ sạch
- [ ] `.env.example` và README khớp nhau (`127.0.0.1` + `connect_timeout`)
- [ ] README cập nhật đủ 4 chỗ ở Bước 2
- [ ] PR có 影響範囲

## Trạng thái review (cập nhật 2026-10-24, PR #5 @ `7e4bd1d`)
- ✅ Code approve: 3 commit đúng chủ đề, 8 passed, ruff/format/mypy sạch, mergeable clean
- ✅ Đã sửa đủ 4 điểm lần trước: `.env.example` dùng `127.0.0.1`; README có 503 (Chạy ứng dụng + bảng); Yêu cầu môi trường dạng danh sách; log message cố định, bỏ `as e`
- 🔧 Mô tả PR: 概要 đang chép từ SETUP-002 (sai) → viết đúng nội dung SETUP-005
- 🔧 Mô tả PR: 変更内容 ghi thêm README (kể cả dòng Docker Desktop — ngoài phạm vi ticket)
- 🔧 Mô tả PR: テスト結果 thêm curl khi DB chạy (200)
- Nit README (không chặn): "`404`, `405`, `500` hoặc `503`"; `Windows`; backtick cho `127.0.0.1`/`localhost`

## Lịch sử thay đổi
- 2026-10-18: TL giao ticket (làm song song với SETUP-002 theo hợp đồng D-024).
- 2026-10-21: #4 merge trước khi Dev B bắt đầu → bỏ bước tự thêm `DATABASE_URL` vào `conftest.py`.
- 2026-10-22: Thêm AC timeout; thêm bắt buộc log trong `except`.
- 2026-10-24: Test URL phải có `connect_timeout=1` (130s trên Windows); `DATABASE_URL` dùng `127.0.0.1` (D-029).
- 2026-10-24: PR #5 mở; TL review: code approve, mô tả PR cần sửa.
- 2026-10-24: PR #5 squash merge `9357e6f`. Cả 2 clone đã pull, cài lại requirements, sửa `.env`; 8 passed.
