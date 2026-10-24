"""Health check endpoint — để load balancer/monitoring biết app còn sống."""

from flask import Blueprint, Response, abort, current_app, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db import get_engine

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check() -> tuple[Response, int]:
    """Trả về trạng thái sống của ứng dụng và kết nối DB."""
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        current_app.logger.exception("Database health check failed")
        abort(503, description="Database is unavailable.")
    return jsonify({"status": "ok"}), 200
