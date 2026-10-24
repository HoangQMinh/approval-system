"""Kết nối database bằng SQLAlchemy."""

from flask import Flask, current_app
from sqlalchemy import Engine, create_engine


def init_db(app: Flask) -> None:
    """Tạo engine từ DATABASE_URL và gắn vào app."""
    engine = create_engine(app.config["DATABASE_URL"], pool_pre_ping=True)
    app.extensions["db_engine"] = engine


def get_engine() -> Engine:
    """Lấy engine của app hiện tại."""
    return current_app.extensions["db_engine"]
