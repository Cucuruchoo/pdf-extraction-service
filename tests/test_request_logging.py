
from fastapi.testclient import TestClient

from app.main import app


def test_generates_request_id():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["X-Request-ID"]


def test_preserves_request_id():
    with TestClient(app) as client:
        response = client.get(
            "/health",
            headers={"X-Request-ID": "prueba-123"},
        )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "prueba-123"


def test_replaces_invalid_request_id():
    with TestClient(app) as client:
        response = client.get(
            "/health",
            headers={"X-Request-ID": "id con espacios"},
        )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] != "id con espacios"
