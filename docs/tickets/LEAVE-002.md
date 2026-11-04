# [LEAVE-002] 簡易認証（X-User-Id ヘッダー）・ログインユーザー取得 API

| | |
|---|---|
| 担当 | Dev B (🔴) |
| Branch | `feature/LEAVE-002` |
| 見積 | 2pt |
| 依存 | LEAVE-001（`User` モデル）— Bước 1 làm ngay được; Bước 2 trở đi sau khi LEAVE-001 merge |
| Trạng thái | 🟡 Assigned (2026-11-01) |

## Ticket
**背景**: 申請・照会 API は「誰が操作しているか」を必要とする。本番の認証方式は未定のため、開発環境用の簡易認証を先に用意する（質問票 No.15, D-034）。

**受け入れ条件 (AC)**
- [ ] リクエストヘッダー `X-User-Id`（users.id）でユーザーを識別すること
- [ ] ヘッダーなし → **401**、message `X-User-Id header is required.`
- [ ] 数字以外（全角数字・負数・空文字・空白を含む）/ 存在しない ID → **401**、message `Invalid X-User-Id.`（存在しないのか形式不正なのかを区別しない）
- [ ] 認証済みユーザーを `g.current_user`（`User`）に格納すること（D-038 — LEAVE-003/005 が利用）
- [ ] `GET /me` でログインユーザー情報（id, employee_code, name, manager_id）を返すこと（200）
- [ ] DB セッションはリクエスト単位で生成し、リクエスト終了時に必ずクローズすること（D-042）
- [ ] テストが追加され、全件パスすること / CI 緑

**参照**: `docs/design/api.md`, D-017, D-034, D-037, D-038, D-042, D-043

---

## 📚 Phần học

| Khái niệm mới | Bên OutSystems |
|---|---|
| Header `X-User-Id` + kiểm tra trước mỗi API | **Exposed REST API → Authentication = Custom → `OnAuthentication`**: đọc header, sai thì raise exception → client nhận 401 |
| Decorator `@login_required` | Giống đặt **OnAuthentication** cho từng method: code chạy **trước** method, không đạt thì method không chạy |
| `g.current_user` | `GetUserId()` — ở bất cứ đâu trong request đều lấy được user hiện tại |
| `g` (flask.g) | **Request-scoped Site Property / biến tạm** — sống trong 1 request, request sau là `g` mới |
| Session theo request (`get_session()` + teardown) | OutSystems tự mở **1 transaction cho mỗi request** và tự đóng/commit khi request kết thúc. High-code phải tự làm việc này |
| `app.teardown_appcontext(func)` | Giống logic chạy **cuối request** (platform tự commit/rollback) — Flask gọi `func` dù request thành công hay lỗi |
| `session.get(User, id)` | **Get<Entity>(Id)** — lấy theo khóa chính, không có thì `None` (OutSystems trả record rỗng) |
| `@pytest.mark.parametrize` | Giống **BDD Framework** chạy 1 scenario với **nhiều dòng dữ liệu** (Examples table) |

### Bước 0 — Bắt đầu (CONTRIBUTING mục 1)
Tạo `feature/LEAVE-002` từ `main` mới nhất (`db6d78e` hoặc mới hơn). **Bước 1 không cần LEAVE-001** → làm ngay.
Khi LEAVE-001 merge: theo CONTRIBUTING **mục 3** (`git fetch` → `git merge origin/main`) để lấy `app/models.py`, rồi làm Bước 2.

📝 README: KHÔNG.

### Bước 1 — Session theo request (`app/db.py`, D-042)
Hiện mỗi chỗ cần DB phải tự `with Session(get_engine())`. Từ ticket này, **code trong request** dùng `get_session()`: 1 request = 1 session, Flask tự đóng khi request kết thúc. (Lệnh CLI của LEAVE-001 vẫn dùng `with Session(...)` — không có request.)

```python
"""Kết nối database bằng SQLAlchemy."""

from flask import Flask, current_app, g
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session


def init_db(app: Flask) -> None:
    """Tạo engine từ DATABASE_URL, gắn vào app và đăng ký đóng session."""
    engine = create_engine(app.config["DATABASE_URL"], pool_pre_ping=True)
    app.extensions["db_engine"] = engine
    # TODO(1): đăng ký close_session chạy khi app context kết thúc


def get_engine() -> Engine:
    """Lấy engine của app hiện tại."""
    return current_app.extensions["db_engine"]


def get_session() -> Session:
    """Lấy Session dùng chung trong request hiện tại (tạo ở lần gọi đầu)."""
    # TODO(2): nếu "db_session" chưa có trong g → tạo Session(get_engine()) gán vào g.db_session
    # TODO(3): trả về g.db_session


def close_session(exception: BaseException | None = None) -> None:
    """Đóng Session của request (nếu có). Flask gọi khi kết thúc app context."""
    # TODO(4): lấy session ra khỏi g (g.pop(..., None)); có thì .close()
```

| Cú pháp | Ghi chú |
|---|---|
| `"tên" in g` | `g` có thuộc tính đó chưa |
| `g.tên = giá trị` / `g.tên` | Gán / đọc |
| `g.pop("tên", None)` | Lấy ra **và xóa**; không có thì trả `None` (giống `dict.pop`) |
| `app.teardown_appcontext(func)` | Đăng ký hàm chạy cuối mỗi app context (cuối request) |

- `exception` trong `close_session`: Flask truyền vào lỗi (nếu có). Không dùng nhưng **phải có tham số** — Flask gọi hàm với 1 đối số.
- Vì sao `g.pop` chứ không `g.db_session`? Request không dùng DB (vd `/health` bị lỗi sớm) thì `g` không có session → `g.db_session` sẽ lỗi.

Kiểm tra: 8 test cũ vẫn xanh (chưa có test mới ở bước này).

📝 README: KHÔNG.

### Bước 2 — Decorator xác thực (`app/auth.py`)

**Decorator là gì** — ví dụ tương tự (KHÔNG phải đáp án), decorator đo thời gian:

```python
import time
from collections.abc import Callable
from functools import wraps


def timed[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)  # giữ tên/docstring của hàm gốc (Flask cần tên để phân biệt route)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()  # ← chạy TRƯỚC hàm gốc
        result = func(*args, **kwargs)  # ← gọi hàm gốc
        print(time.perf_counter() - start)  # ← chạy SAU hàm gốc
        return result

    return wrapped


@timed  # tương đương: slow = timed(slow)
def slow() -> None: ...
```

- `[**P, R]` (cú pháp Python 3.12): nói với mypy "hàm bọc nhận **cùng tham số** (`P`) và trả **cùng kiểu** (`R`) như hàm gốc". Chép nguyên khuôn này cho decorator của mình.
- `login_required` giống hệt khuôn trên, chỉ khác: **trước** khi gọi hàm gốc thì kiểm tra header; không đạt thì `abort(401)` → hàm gốc không bao giờ chạy.

Skeleton:

```python
"""Xác thực tạm thời bằng header X-User-Id (D-034). Chỉ dùng cho môi trường dev."""

from collections.abc import Callable
from functools import wraps

from flask import abort, g, request

from app.db import get_session
from app.models import User

USER_ID_HEADER = "X-User-Id"


def login_required[**P, R](view: Callable[P, R]) -> Callable[P, R]:
    """Decorator: bắt buộc header X-User-Id hợp lệ, gán user vào g.current_user."""

    @wraps(view)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        # TODO(1): đọc header USER_ID_HEADER (không có → None)
        # TODO(2): None → abort 401, description đúng như AC
        # TODO(3): không phải số ASCII → abort 401 "Invalid X-User-Id."
        #          ⚠️ "１".isdigit() là True và int("１") == 1 — QA người Nhật sẽ thử số toàn góc
        # TODO(4): lấy User theo id bằng get_session(); None → abort 401 "Invalid X-User-Id."
        # TODO(5): gán user vào g.current_user
        return view(*args, **kwargs)

    return wrapped
```

| Cú pháp | Ghi chú |
|---|---|
| `request.headers.get("X-User-Id")` | Đọc header; không có → `None`. Tên header không phân biệt hoa thường |
| `abort(401, description="...")` | Dừng request; error handler (SETUP-003) trả JSON `{"error": "Unauthorized", "message": ...}` |
| `s.isascii()` / `s.isdigit()` | Toàn ký tự ASCII? / toàn chữ số? (`""` → cả hai đều... thử xem!) |
| `int(s)` | Chuỗi → số |
| `get_session().get(User, user_id)` | Lấy theo khóa chính, không có → `None` |

- **Vì sao "không tồn tại" và "sai định dạng" cùng 1 message?** Nếu message khác nhau, người ngoài thử lần lượt ID là biết ID nào tồn tại (dò tài khoản). Nguyên tắc: lỗi xác thực không tiết lộ chi tiết.
- mypy: sau `abort(...)` mypy biết hàm không chạy tiếp (kiểu `NoReturn`) → sau dòng kiểm `None`, biến được coi là `str`. Không cần `else`.

📝 README: KHÔNG (README ở Bước 4).

### Bước 3 — `GET /me` (`app/routes/users.py`, D-043)
Endpoint nhỏ để **dùng thử xác thực** (curl, QA) trước khi có API đơn nghỉ.

```python
"""API thông tin người dùng."""

from flask import Blueprint, Response, g, jsonify

from app.auth import login_required

users_bp = Blueprint("users", __name__)


@users_bp.get("/me")
# TODO(1): đặt decorator xác thực — thứ tự: route ở TRÊN, login_required ở DƯỚI
def get_me() -> tuple[Response, int]:
    """Trả về thông tin user đang đăng nhập (theo X-User-Id)."""
    # TODO(2): lấy user từ g, trả JSON 4 field theo AC + 200
    ...
```

`create_app`: đăng ký `users_bp` ngay sau `health_bp` (import trong hàm, D-003).

- **Thứ tự decorator**: decorator gần hàm nhất chạy bọc trước. `@users_bp.get` phải đăng ký hàm **đã được bọc** bởi `login_required`, nên route nằm trên cùng. Đảo ngược → route đăng ký hàm chưa bọc → `/me` **không kiểm tra gì** (lỗi bảo mật — test 401 sẽ bắt).
- PEP 8: dict nhiều field viết mỗi field 1 dòng, có dấu phẩy cuối → `ruff format` giữ nguyên dạng nhiều dòng.

Thử thật (DB Docker + `init-db` + `seed-users` của LEAVE-001):
```cmd
curl -i http://127.0.0.1:5000/me
curl -i -H "X-User-Id: abc" http://127.0.0.1:5000/me
curl -i -H "X-User-Id: 2" http://127.0.0.1:5000/me
```
→ 401 / 401 / 200 (id 2 = E001 nếu seed chạy trên DB trống).

📝 README: KHÔNG (README ở Bước 4).

### Bước 4 — Test + README

**`tests/conftest.py`** — thêm fixture (dùng chung cho LEAVE-003/005, viết sẵn):
```python
@pytest.fixture
def seeded_app(app: Flask) -> Flask:
    runner = app.test_cli_runner()
    runner.invoke(args=["init-db"])
    runner.invoke(args=["seed-users"])
    return app
```
Test nào cần user thì nhận `seeded_app` **và** `client` — cả hai dùng chung 1 `app` nên chung DB.

**`tests/test_auth.py`**:
```python
import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import select

from app.db import get_session
from app.models import User


def user_id_of(app: Flask, employee_code: str) -> int:
    """Lấy id của user theo mã nhân viên (id không cố định — đừng viết cứng 2)."""
    with app.app_context():
        # TODO: get_session().scalar(select(User).where(...)); assert không None; trả id
        ...


def test_me_returns_current_user(seeded_app: Flask, client: FlaskClient):
    # TODO: gọi /me với id của E001 → 200; id, employee_code, manager_id (== id M001) đúng
    ...


def test_me_without_header_returns_401(seeded_app: Flask, client: FlaskClient):
    # TODO: 401; error == "Unauthorized"; message đúng AC
    ...


@pytest.mark.parametrize("value", ["abc", "", "-1", "1.5", "１", "9999"])
def test_me_with_invalid_user_id_returns_401(
    seeded_app: Flask, client: FlaskClient, value: str
):
    # TODO: 401; message == "Invalid X-User-Id."
    ...
```

| Cú pháp | Ghi chú |
|---|---|
| `client.get("/me", headers={"X-User-Id": "1"})` | Gửi request kèm header |
| `@pytest.mark.parametrize("value", [...])` | Test chạy 1 lần cho **mỗi** giá trị; pytest hiện từng case riêng |
| `with app.app_context():` | Cần khi gọi `get_session()` ngoài request |

**Mutation (bắt buộc, ghi vào PR body):**
1. Bỏ `isascii()` → case `"１"` phải đỏ.
2. Đảo thứ tự 2 decorator ở `/me` → các test 401 phải đỏ.
Làm xong hoàn tác (chưa commit thì `git restore <file>`).

**README** — mục API (cạnh "Định dạng lỗi API"): thêm `## Xác thực (tạm thời, chỉ cho dev)`:
- header `X-User-Id: <users.id>`, user lấy từ `seed-users`
- ví dụ curl `/me` (200) + 2 trường hợp 401 và message
- 1 dòng: sẽ thay bằng đăng nhập thật ở sprint sau (D-034)
- bảng HTTP status: thêm dòng **401**

📝 README: CÓ — mục mới "Xác thực (tạm thời, chỉ cho dev)" + dòng 401 trong bảng status.

### Bước 5 — PR
- CONTRIBUTING mục 4: 4 lệnh sạch, PR dùng template (tự điền).
- CI phải ✅ — từ SETUP-007, PR đỏ **không merge được**.
- Không đụng `docs/` (D-011). Merge sau LEAVE-001.

## Definition of Done
- [ ] `get_session()` + đóng session ở teardown; 8 test cũ không đổi vẫn xanh
- [ ] `login_required` đúng 3 nhánh 401 + gán `g.current_user`
- [ ] `GET /me` 200 đúng 4 field; curl thật 3 trường hợp đã thử
- [ ] Test mới xanh (gồm parametrize), 2 mutation đã làm
- [ ] README: mục Xác thực + dòng 401
- [ ] 4 lệnh sạch; CI ✅

## Lịch sử thay đổi
- 2026-11-01: TL giao. Bản tham chiếu của TL (trên LEAVE-001 tham chiếu): ruff/format/mypy sạch, 20 passed.
- 2026-11-01: Sửa khối code ví dụ `timed` theo `ruff format` (ruff 0.17 format cả code Python trong file `.md` — lỗi của TL, Dev A phát hiện).
