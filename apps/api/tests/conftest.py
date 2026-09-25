from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from fernweh_api.main import create_app
from fernweh_api.settings import Settings


@pytest.fixture
def settings() -> Settings:
    return Settings(_env_file=None, app_env="test", log_level="DEBUG")


@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    with TestClient(create_app(settings)) as test_client:
        yield test_client
