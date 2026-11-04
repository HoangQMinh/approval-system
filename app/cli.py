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
        Base.metadata.create_all(get_engine())
        click.echo("Tables created.")

    @app.cli.command("seed-users")
    def seed_users_command() -> None:
        """Nạp user mẫu (bỏ qua user đã tồn tại)."""
        with Session(get_engine()) as session:
            for code, name, manager_code in SEED_USERS:
                existing_user = session.scalar(
                    select(User).where(User.employee_code == code)
                )

                if existing_user is not None:
                    continue

                manager_id = None

                if manager_code is not None:
                    manager = session.scalar(
                        select(User).where(User.employee_code == manager_code)
                    )

                    if manager is None:
                        raise ValueError(f"Manager {manager_code} not found")

                    manager_id = manager.id

                user = User(
                    employee_code=code,
                    name=name,
                    manager_id=manager_id,
                )

                session.add(user)

                session.flush()

            session.commit()

        click.echo("Seed users loaded.")
