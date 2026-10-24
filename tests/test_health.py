from app import create_app


def test_health_returns_200_and_status_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}
    assert response.is_json


def test_unknown_route_healthz_returns_404(client):
    response = client.get("/healthz")

    assert response.status_code == 404


def test_health_returns_503_when_database_is_unreachable():
    app = create_app(
        {
            "TESTING": True,
            "DATABASE_URL": "postgresql+psycopg://u:p@127.0.0.1:1/db?connect_timeout=1",
        }
    )
    response = app.test_client().get("/health")

    assert response.status_code == 503
    assert response.is_json
    data = response.json

    assert data is not None
    assert data["error"] == "Service Unavailable"
