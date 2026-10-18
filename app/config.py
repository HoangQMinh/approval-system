"""Đọc cấu hình ứng dụng từ biến môi trường."""

import os


def load_config_from_env() -> dict[str, str | None]:
    """Trả về dict cấu hình lấy từ biến môi trường."""
    return {"DATABASE_URL": os.environ.get("DATABASE_URL")}
