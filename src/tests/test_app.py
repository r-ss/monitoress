import os
from tests.testutils import get

from config import config


def test_debug_mode(client):
    if config.PRODUCTION:
        assert config.DEBUG is False
    else:
        assert config.DEBUG is True


def test_testing_mode(client):
    assert config.TESTING_MODE is True


def test_root(client):
    status_code, result = get(client, "/")
    assert status_code == 404


def test_info(client):
    status_code, result = get(client, "/api/info")
    assert status_code == 200
    assert result["resource"] == config.APP_NAME
    assert result["testing"] is True
    assert result["python version"].startswith("3.11") is True
