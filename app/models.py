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
        CheckConstraint(_in("period_type", PERIOD_TYPES), name="ck_period_type"),
        CheckConstraint(_in("status", STATUSES), name="ck_status"),
        CheckConstraint("start_date <= end_date", name="ck_date_range"),
        CheckConstraint(
            "period_type = 'full_day' OR start_date = end_date", name="ck_half_day"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    applicant_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    approver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    leave_type: Mapped[str] = mapped_column(String(20))
    period_type: Mapped[str] = mapped_column(String(10))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    reason: Mapped[str | None] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class ApprovalHistory(Base):
    __tablename__ = "approval_histories"
    __table_args__ = CheckConstraint(_in("action", ACTIONS), name="ck_action")

    id: Mapped[int] = mapped_column(primary_key=True)
    leave_request_id: Mapped[int] = mapped_column(ForeignKey("leave_requests.id"))
    actor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(20))
    comment: Mapped[str | None] = mapped_column(Text)
    acted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
