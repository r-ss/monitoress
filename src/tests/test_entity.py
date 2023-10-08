from tests.testutils import get

from config import config


def test_entity(client):
    status_code, result = get(client, "/api/all")
    # status_code, result = get(client, "/api/probe/0")
    
    print(result)
    # assert status_code == 200
    # assert result["client"] == config.APP_NAME
    # assert result["entity_name"] == "test_only"
    # assert result["status"] == "ok"