"""Error handlers: trả lỗi dạng JSON thống nhất cho toàn bộ API."""

from flask import Flask, Response, jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    """Đăng ký error handler vào app."""

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException) -> tuple[Response, int]:
        status = error.code if error.code is not None else 500
        return jsonify({"error": error.name, "message": error.description}), status

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> tuple[Response, int]:
        app.logger.exception("Unhandled exception")
        return jsonify(
            {
                "error": "Internal Server Error",
                "message": "An unexpected error occurred",
            }
        ), 500
