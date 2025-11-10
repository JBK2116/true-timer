"""
General Tests for this web application
"""

from fastapi import Response
from fastapi.testclient import TestClient


def test_api_connection(client: TestClient):
    # Keep it simple
    response: Response = client.get("/test")
    assert response.status_code == 200


def test_create_user_invalid_timezone(client: TestClient):
    """
    Tests creating a user with an invalid timezone.
    :return: Status Code 400
    """
    pass
