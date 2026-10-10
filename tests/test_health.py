def test_health_returns_200_and_status_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}
    assert response.is_json


def test_unknown_route_healthz_returns_404(client):
    response = client.get("/healthz")

    assert response.status_code == 404
