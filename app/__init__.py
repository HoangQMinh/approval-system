"""Application package - chứa app factory."""
from flask import Flask


def create_app(test_config: dict | None = None) -> Flask:
    """Tạo và cấu hình Flask application.

    Args:
        test_config: Cấu hình ghi đè cấu hình mặc định, thường dùng khi chạy test.
            Nếu là None, sử dụng cấu hình mặc định của ứng dụng.

    Returns:
        Flask application đã được cấu hình, đăng ký blueprint và error handler.
    """
    app = Flask(__name__)
    if test_config is not None:
        app.config.update(test_config)

    from app.routes.health import health_bp
    app.register_blueprint(health_bp)

    from app.errors import register_error_handlers
    register_error_handlers(app)

    return app
