from fastapi import FastAPI
from fastapi.testclient import TestClient
from structlog.testing import capture_logs

from fernweh_api.main import create_app
from fernweh_api.settings import Settings


def test_response_includes_generated_request_id(client: TestClient) -> None:
    response = client.get("/healthz")

    assert len(response.headers["x-request-id"]) == 32


def test_valid_incoming_request_id_is_echoed(client: TestClient) -> None:
    response = client.get("/healthz", headers={"X-Request-ID": "trace-abc.123"})

    assert response.headers["x-request-id"] == "trace-abc.123"


def test_unsafe_incoming_request_id_is_replaced(client: TestClient) -> None:
    response = client.get("/healthz", headers={"X-Request-ID": "bad id\r\ninjected"})

    assert response.headers["x-request-id"] != "bad id\r\ninjected"
    assert len(response.headers["x-request-id"]) == 32


def test_completed_request_is_logged_with_request_id(client: TestClient) -> None:
    with capture_logs() as logs:
        client.get("/healthz", headers={"X-Request-ID": "req-1"})

    completed = [entry for entry in logs if entry["event"] == "request_completed"]
    assert completed == [
        {
            "event": "request_completed",
            "log_level": "info",
            "method": "GET",
            "path": "/healthz",
            "status_code": 200,
            "duration_ms": completed[0]["duration_ms"],
        }
    ]


def _app_with_failing_route(settings: Settings) -> FastAPI:
    app = create_app(settings)

    @app.get("/boom")
    async def boom() -> None:
        raise RuntimeError("secret internal detail")

    return app


def test_unhandled_error_returns_envelope_without_internal_details(settings: Settings) -> None:
    app = _app_with_failing_route(settings)
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/boom", headers={"X-Request-ID": "req-500"})

    assert response.status_code == 500
    assert response.headers["x-request-id"] == "req-500"
    assert response.json() == {
        "code": "internal",
        "message": "An unexpected error occurred.",
        "retryable": False,
        "request_id": "req-500",
    }
    assert "secret internal detail" not in response.text
