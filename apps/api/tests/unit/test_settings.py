import pytest

from fernweh_api.settings import Settings


def test_cors_origins_parse_from_comma_separated_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_CORS_ORIGINS", "http://localhost:3000, https://app.fernweh.dev ,")

    settings = Settings(_env_file=None)

    assert settings.api_cors_origins == ["http://localhost:3000", "https://app.fernweh.dev"]


def test_invalid_app_env_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "prod-ish")

    with pytest.raises(ValueError, match="app_env"):
        Settings(_env_file=None)
