# [LEAVE-001] 休暇申請テーブル作成（モデル定義・初期化コマンド・初期データ）

| | |
|---|---|
| 担当 | Dev A (🔵) |
| Branch | `feature/LEAVE-001` |
| 見積 | 3pt |
| Trạng thái | 🟡 In Review — Draft PR #9 (Bước 1–3 xong, 2026-11-05) |

## Ticket
**背景**: Sprint 1 の申請・照会機能のため、DB テーブルを用意する。

**受け入れ条件 (AC)**
- [ ] `users` / `leave_requests` / `approval_histories` の 3 テーブルを ORM モデルとして定義すること（定義は `docs/design/tables.md` に従う）
- [ ] `flask --app app init-db` でテーブルが作成されること
- [ ] `flask --app app seed-users` で初期ユーザー 3 名（上長関係含む）が登録され、複数回実行しても重複しないこと
- [ ] DB の CHECK 制約で不正値（種別・区分・状態・日付範囲・半休の複数日）が拒否されること
- [ ] テストが追加され、全件パスすること

**参照**: `docs/design/tables.md`, D-023, D-026, D-035, D-036

---

## 📚 Phần học

| Khái niệm mới | Bên OutSystems |
|---|---|
| Model ORM (`class User(Base)`) | **Entity** trong Service Studio |
| `Mapped[int]`, `mapped_column(...)` | **Attribute** của Entity (Data Type, Is Mandatory, Length) |
| `Mapped[int \| None]` | Attribute **không bắt buộc** (Is Mandatory = No) |
| `ForeignKey("users.id")` | Attribute kiểu **User Identifier** (reference tới entity khác) |
| `CheckConstraint(...)` | Không có sẵn trong OutSystems (thường kiểm ở logic). Ở đây **DB tự chặn** dữ liệu sai — lớp bảo vệ cuối |
| `server_default=func.now()` | Attribute có **Default Value** = `CurrDateTime()` nhưng do **DB** điền |
| `Base.metadata.create_all(engine)` | Bấm **Publish** → platform tự tạo/sửa bảng. Ở high-code phải chạy lệnh (sau này: migration) |
| Lệnh CLI `flask --app app init-db` | Giống **Timer chạy tay một lần** / Bootstrap action dựng dữ liệu ban đầu |
| `Session`, `select(...)`, `session.add`, `session.commit()` | **Aggregate** (đọc), **CreateEntity** (thêm) và cơ chế commit transaction cuối request |

### Bước 1 — Model (`app/models.py`)

```python
"""ORM model cho nghiệp vụ nghỉ phép."""

from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

LEAVE_TYPES = ("annual_paid", "special", "substitute")
PERIOD_TYPES = ("full_day", "am", "pm")
STATUSES = ("pending", "approved", "returned", "withdrawn")
ACTIONS = ("submit", "approve", "return", "resubmit", "withdraw")


def _in(column: str, values: tuple[str, ...]) -> str:
    """Tạo biểu thức SQL `column IN ('a', 'b')` cho CheckConstraint."""
    quoted = ", ".join(f"'{v}'" for v in values)
    return f"{column} IN ({quoted})"


class Base(DeclarativeBase):
    """Base class cho mọi model."""


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_code: Mapped[str] = mapped_column(String(20), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    __table_args__ = (
        CheckConstraint(_in("leave_type", LEAVE_TYPES), name="ck_leave_type"),
        # TODO(1): CHECK cho period_type, status (dùng _in)
        # TODO(2): CHECK start_date <= end_date (name="ck_date_range")
        # TODO(3): CHECK nửa ngày chỉ 1 ngày (name="ck_half_day") — xem tables.md
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO(4): các cột còn lại theo tables.md
    #   - applicant_id, approver_id: FK → users.id
    #   - leave_type, period_type, status: String với độ dài theo tables.md
    #   - start_date, end_date: Date
    #   - reason: String(200), cho phép NULL
    #   - created_at: như User
    #   - updated_at: như created_at + onupdate=func.now()


class ApprovalHistory(Base):
    # TODO(5): theo tables.md — nhớ CHECK cho action, comment kiểu Text cho phép NULL
    ...
```

> `User` được viết đầy đủ làm **mẫu**. `LeaveRequest`/`ApprovalHistory` anh tự viết theo `tables.md`.

📝 README: KHÔNG.

### Bước 2 — Lệnh CLI (`app/cli.py`) + đăng ký trong `create_app`

```python
"""Lệnh CLI quản trị DB (chạy bằng flask --app app <lệnh>)."""

import click
from flask import Flask
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_engine
from app.models import Base, User

SEED_USERS = [
    # (employee_code, name, manager_employee_code)
    ("M001", "Tanaka Taro", None),
    ("E001", "Sato Hanako", "M001"),
    ("E002", "Suzuki Ichiro", "M001"),
]


def register_cli(app: Flask) -> None:
    """Đăng ký lệnh CLI vào app."""

    @app.cli.command("init-db")
    def init_db_command() -> None:
        """Tạo bảng (chưa có migration — D-035)."""
        # TODO(1): tạo mọi bảng từ Base.metadata bằng engine
        click.echo("Tables created.")

    @app.cli.command("seed-users")
    def seed_users_command() -> None:
        """Nạp user mẫu (bỏ qua user đã tồn tại)."""
        with Session(get_engine()) as session:
            for code, name, manager_code in SEED_USERS:
                # TODO(2): nếu user có employee_code == code đã tồn tại → bỏ qua (continue)
                #          gợi ý: session.scalar(select(User).where(...))
                # TODO(3): tìm manager_id từ manager_code (None nếu không có cấp trên)
                # TODO(4): session.add(User(...)) rồi session.flush()
                #          (flush để user vừa thêm có id — user sau cần id của cấp trên)
                ...
            # TODO(5): commit
        click.echo("Seed users loaded.")
```

`create_app`: gọi `register_cli(app)` (import trong hàm, D-003), sau `init_db(app)`. Cập nhật docstring.

Thử thật (DB Docker đang chạy):
```cmd
flask --app app init-db
flask --app app seed-users
flask --app app seed-users
docker compose exec db psql -U approval -d approval -c "SELECT id, employee_code, manager_id FROM users"
docker compose exec db psql -U approval -d approval -c "\d leave_requests"
```
Chạy `seed-users` 2 lần vẫn chỉ 3 user. `\d leave_requests` phải liệt kê đủ 5 CHECK constraint.

| Cú pháp | Ghi chú |
|---|---|
| `@app.cli.command("tên")` | Đăng ký lệnh cho `flask --app app tên` |
| `click.echo("...")` | In ra màn hình trong lệnh CLI (thay cho `print`) |
| `with Session(engine) as session:` | Mở phiên làm việc với DB, tự đóng |
| `session.scalar(select(User).where(User.x == y))` | Lấy 1 đối tượng hoặc `None` |
| `session.add(obj)` / `session.flush()` / `session.commit()` | Thêm / gửi xuống DB (có id) / chốt transaction |

📝 README: CÓ — mục **Khởi động DB** thêm bước "Khởi tạo bảng và dữ liệu mẫu" (`init-db`, `seed-users`), ghi chú: chưa có migration, đổi model thì xóa bảng/volume và chạy lại (D-035).

### Bước 3 — Test (`tests/test_models.py`)

Test chạy trên SQLite in-memory của fixture `app` (D-026). Gọi lệnh CLI trong test bằng `app.test_cli_runner()`.

```python
from datetime import date

import pytest
from flask import Flask
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_engine
from app.models import LeaveRequest, User


def test_init_db_creates_tables(app: Flask):
    result = app.test_cli_runner().invoke(args=["init-db"])
    # TODO: exit_code == 0
    # TODO: trong app.app_context(): inspect(get_engine()).get_table_names() chứa đủ 3 bảng


def test_seed_users_is_idempotent(app: Flask):
    # TODO: invoke init-db, rồi seed-users 2 lần
    # TODO: đúng 3 user; E001.manager_id == id của M001
    ...


def test_half_day_must_be_single_day(app: Flask):
    # TODO: init-db + seed-users; thêm LeaveRequest period_type="am" nhưng 2 ngày
    # TODO: with pytest.raises(IntegrityError): session.commit()
    ...
```

- `get_engine()` dùng `current_app` → cần `with app.app_context():` khi gọi ngoài request.
- SQLite **không kiểm FK** mặc định → test FK để sau (khi test trên PostgreSQL). CHECK thì SQLite có kiểm.
- Mutation: bỏ tạm `ck_half_day` → test 3 phải đỏ.

📝 README: KHÔNG thêm.

### Bước 4 — Công cụ, PR (Draft), chờ CI
- 4 công cụ sạch. Commit theo chủ đề (model / CLI / test / README).
- Mở **Draft PR** dùng template mới (sau khi SETUP-006 merge). Khi SETUP-007 merge: `git merge origin/main` → CI chạy trên PR này → xanh → Ready for review.
- Commit cuối: `docs/` (team-log, tickets, design, sprints, roles, qa) — D-011.

## Definition of Done
- [ ] 3 model đúng `tables.md` (cột, null, độ dài, FK, 5 CHECK ở leave_requests + 1 ở approval_histories)
- [ ] `init-db`, `seed-users` chạy thật trên PostgreSQL; seed chạy lại không trùng
- [ ] 3 test mới xanh; mutation `ck_half_day` đã làm
- [ ] 4 công cụ sạch; CI xanh trên PR
- [ ] README có bước khởi tạo bảng

## Lịch sử thay đổi
- 2026-10-26: TL giao.
- 2026-11-05: Bước 1–3 review xong; chờ bằng chứng PostgreSQL + commit `docs/` cuối.
