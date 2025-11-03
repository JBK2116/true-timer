"""
General Tests for this web application
"""

import uuid

from fastapi import Response
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_connection():
    # Keep it simple
    response: Response = client.get("/test")
    assert response.status_code == 200


def test_uuid():
    # ensure UUID is valid and belongs to a user
    valid_uuid = str(uuid.uuid4())
    first_response = client.get(f"/users/{valid_uuid}")
    # TODO: Also ensure that you check to see if uuid maps to an existing user in database
    assert first_response.status_code == 200
    invalid_uuid = valid_uuid.replace("-", "")[:-2]
    # TODO: Also ensure that you check to see if uuid maps to an existing user in database
    second_response = client.get(f"/users/{invalid_uuid}")
    assert second_response.status_code == 400
