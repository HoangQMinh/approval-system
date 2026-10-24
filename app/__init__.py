"""Application package - chứa app factory."""

from flask import Flask


def create_app(test_config: dict | None = None) -> Flask:
    """Tạo và cấu hình Flask application.

    Đọc cấu hình mặc định từ biến môi trường, sau đó áp dụng
    test_config nếu được cung cấp.
    Tạo engine từ DATABASE_URL và gắn vào app.

    Args:
        test_config: Cấu hình ghi đè cấu hình đọc từ biến môi trường,
            thường dùng khi chạy test. Nếu là None, sử dụng cấu hình
            đọc từ biến môi trường.

    Returns:
        Flask application đã được cấu hình, đăng ký blueprint và error handler.

    Raises:
        RuntimeError: Nếu DATABASE_URL bị thiếu hoặc rỗng. Hãy thiết lập
            DATABASE_URL trong file .env trước khi khởi động ứng dụng.
    """
    app = Flask(__name__)

    from app.config import load_config_from_env

    app.config.update(load_config_from_env())

    if test_config is not None:
        app.config.update(test_config)

    if not app.config.get("DATABASE_URL"):
        raise RuntimeError(
            "DATABASE_URL is missing. Please set DATABASE_URL in your .env file."
        )

    from app.db import init_db

    init_db(app)

    from app.routes.health import health_bp

    app.register_blueprint(health_bp)

    from app.errors import register_error_handlers

    register_error_handlers(app)

    return app
