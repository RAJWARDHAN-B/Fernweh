from fastapi.testclient import TestClient

from fernweh_api.main import create_app
from fernweh_api.settings import Settings


def test_healthz_reports_ok(client: TestClient) -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz_reports_ready(client: TestClient) -> None:
    response = client.get("/readyz")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_api_docs_are_exposed_outside_production(client: TestClient) -> None:
    assert client.get("/openapi.json").status_code == 200


def test_api_docs_are_hidden_in_production() -> None:
    settings = Settings(_env_file=None, app_env="production")
    with TestClient(create_app(settings)) as client:
        assert client.get("/openapi.json").status_code == 404
        assert client.get("/docs").status_code == 404


def test_cors_allows_configured_origin_only(client: TestClient) -> None:
    allowed = client.get("/healthz", headers={"Origin": "http://localhost:3000"})
    blocked = client.get("/healthz", headers={"Origin": "https://evil.example"})

    assert allowed.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "access-control-allow-origin" not in blocked.headers
