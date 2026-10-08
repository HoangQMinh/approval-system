from flask import Flask
from flask.testing import FlaskClient
import pytest

from app import create_app


@pytest.fixture
def app() -> Flask:
    return create_app({"TESTING": True})


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
