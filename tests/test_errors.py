from flask import Flask


def test_unknown_route_returns_json_404(client):
    response = client.get("/healthz")

    assert response.status_code == 404
    assert response.is_json
    data = response.json

    assert data is not None
    assert data["error"] == "Not Found"


def test_wrong_method_returns_json_405(client):
    response = client.post("/health")

    assert response.status_code == 405
    assert response.is_json
    allow = response.headers.get("Allow", "")
    methods = [method.strip() for method in allow.split(",")]
    assert allow != ""
    assert "GET" in methods
    data = response.json

    assert data is not None
    assert data["error"] == "Method Not Allowed"


def test_unexpected_error_returns_json_500_without_detail(app: Flask):
    @app.get("/_test/boom")  # route tạm, chỉ tồn tại trong test này
    def boom():
        raise RuntimeError("secret-db-password")

    response = app.test_client().get("/_test/boom")

    assert response.status_code == 500
    assert response.is_json
    data = response.json

    assert data is not None
    assert data["error"] == "Internal Server Error"

    body = response.get_data(as_text=True)
    assert "secret-db-password" not in body
