"""Error handlers: trả lỗi dạng JSON thống nhất cho toàn bộ API."""

from flask import Flask, Response, jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    """Đăng ký error handler vào app."""

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException) -> tuple[Response, int]:
        status = error.code if error.code is not None else 500
        response = jsonify({"error": error.name, "message": error.description})
        headers = error.get_headers()
        for name, value in headers:
            if name.lower() != "content-type":
                response.headers[name] = value
        return response, status

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> tuple[Response, int]:
        app.logger.exception("Unhandled exception")
        return jsonify(
            {
                "error": "Internal Server Error",
                "message": "An unexpected error occurred",
            }
        ), 500
