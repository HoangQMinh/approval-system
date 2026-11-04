from datetime import date

import pytest
from flask import Flask
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_engine
from app.models import LeaveRequest, User


def _init_and_seed(app: Flask) -> None:
    runner = app.test_cli_runner()

    assert runner.invoke(args=["init-db"]).exit_code == 0
    assert runner.invoke(args=["seed-users"]).exit_code == 0


def test_init_db_creates_tables(app: Flask):
    result = app.test_cli_runner().invoke(args=["init-db"])

    assert result.exit_code == 0

    with app.app_context():
        table_names = inspect(get_engine()).get_table_names()

    assert {"users", "leave_requests", "approval_histories"} <= set(table_names)


def test_seed_users_is_idempotent(app: Flask):
    runner = app.test_cli_runner()

    assert runner.invoke(args=["init-db"]).exit_code == 0
    assert runner.invoke(args=["seed-users"]).exit_code == 0
    assert runner.invoke(args=["seed-users"]).exit_code == 0

    with app.app_context(), Session(get_engine()) as session:
        users = session.scalars(select(User)).all()
        by_code = {u.employee_code: u for u in users}

    assert len(users) == 3
    assert by_code["M001"].manager_id is None
    assert by_code["E001"].manager_id == by_code["M001"].id


def test_half_day_must_be_single_day(app: Flask):
    _init_and_seed(app)

    with app.app_context(), Session(get_engine()) as session:
        applicant = session.scalar(select(User).where(User.employee_code == "E001"))
        approver = session.scalar(select(User).where(User.employee_code == "M001"))

        assert applicant is not None
        assert approver is not None

        session.add(
            LeaveRequest(
                applicant_id=applicant.id,
                approver_id=approver.id,
                leave_type="annual_paid",
                period_type="am",
                start_date=date(2026, 11, 2),
                end_date=date(2026, 11, 3),
                status="pending",
            )
        )

        with pytest.raises(IntegrityError):
            session.commit()
