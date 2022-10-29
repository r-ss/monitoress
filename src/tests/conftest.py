import pytest

from config import config

from main import testclient

# from tests.testutils import get


@pytest.fixture
def client():
    config.TESTING_MODE = True
    return testclient
