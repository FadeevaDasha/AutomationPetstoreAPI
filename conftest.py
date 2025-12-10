from core.clients.api_client import APIClient
import pytest


@pytest.fixture(scope='session')
def api_client():
    client = APIClient()
    client.auth()
    return client