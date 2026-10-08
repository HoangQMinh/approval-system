"""Application package - chứa app factory."""
from flask import Flask


def create_app(test_config: dict | None = None) -> Flask:
    """Tạo và cấu hình Flask app.

    Args:
        test_config: Config ghi đè khi chạy test. None khi chạy thật.

    Returns:
        Flask app đã đăng ký đủ blueprint.
    """
    app = Flask(__name__)
    if test_config is not None:
        app.config.update(test_config)

    from app.routes.health import health_bp
    app.register_blueprint(health_bp)

    return app
