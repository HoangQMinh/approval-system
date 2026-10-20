import pytest

from app import create_app


def test_database_url_is_read_from_env(monkeypatch):
    database_url = "postgresql+psycopg://u:p@localhost:5433/db"

    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app({"TESTING": True})

    assert app.config["DATABASE_URL"] == database_url


def test_missing_database_url_raises(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        create_app()
