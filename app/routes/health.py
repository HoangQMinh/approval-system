"""Health check endpoint — để load balancer/monitoring biết app còn sống."""
from flask import Blueprint, jsonify, Response

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check() -> tuple[Response, int]:
    """Trả về trạng thái sống của ứng dụng."""
    return jsonify({"status": "ok"}), 200
