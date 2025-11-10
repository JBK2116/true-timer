"""
General Tests for this web application
"""
import uuid

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.main import app
from backend.models import User
from backend.schemas import CreateUserOut, GetUserOut

sync_client = TestClient(app)


def test_api_connection():
    """Basic connectivity test."""
    response: Response = sync_client.get("/test")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_user_invalid_timezone(async_client: AsyncClient) -> None:
    """
    Test creating a user with an invalid timezone.
    Expects a 400 response with an error message.
    :param async_client: Async client for testing.
    """
    invalid_timezone = "America/NewYork"
    response: Response = await async_client.post(
        url="/users",
        json={"timezone": invalid_timezone},
    )
    returned_data = response.json()
    assert response.status_code == 400
    assert returned_data["message"] is not None


@pytest.mark.asyncio
async def test_create_user_valid_timezone(
    async_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """
    Test creating a user with a valid timezone and verify database entry.
    :param async_client: Async client for testing.
    :param db_session: Async db connection for testing.
    """
    valid_timezone = "America/New_York"

    response: Response = await async_client.post(
        url="/users", json={"timezone": valid_timezone}
    )

    # Response verification
    returned_data = CreateUserOut.model_validate(response.json())
    assert response.status_code == 200
    assert returned_data.user_id is not None
    assert returned_data.timezone == valid_timezone

    # Database verification
    stmt = select(User).where(User.user_id == returned_data.user_id)
    result = await db_session.execute(stmt)
    created_user = result.scalar_one_or_none()

    assert created_user is not None
    assert created_user.timezone == "America/New_York"

@pytest.mark.asyncio
async def test_get_user_invalid_uuid(async_client: AsyncClient, db_session: AsyncSession) -> None:
    """
    Tests getting a user with an invalid UUID format.
    :param async_client: Async client for testing.
    :param db_session: Async db connection for testing.
    """
    invalid_uuid = "12345-invalid-uuid-67890"
    response: Response = await async_client.get(f"/users/{invalid_uuid}")
    assert response.status_code == 400
    assert response.json()["message"] is not None

@pytest.mark.asyncio
async def test_get_user_valid_uuid_invalid_user(async_client: AsyncClient, db_session: AsyncSession) -> None:
    """
    Tests getting a user with a valid UUID format.
    :param async_client: Async client for testing.
    :param db_session: Async db connection for testing.
    """
    valid_uuid = uuid.uuid4()
    response: Response = await async_client.get(f"/users/{valid_uuid}")
    assert response.status_code == 400
    assert "does not exist" in response.json()["message"]

@pytest.mark.asyncio
async def test_get_user_valid_uuid_valid_user(async_client: AsyncClient, db_session: AsyncSession) -> None:
    """
    Tests getting a user with a valid UUID format and matching existing user.
    :param async_client: Async client for testing.
    :param db_session: Async db connection for testing.
    """

    # Create the user using the POST endpoint
    valid_timezone = "America/New_York"
    response: Response = await async_client.post(f"/users", json={"timezone": valid_timezone})
    created_user = CreateUserOut.model_validate(response.json())

    # Test retrieving the user
    get_user_response = await async_client.get(f"/users/{created_user.user_id}")
    returned_user = GetUserOut.model_validate(get_user_response.json())

    assert get_user_response.status_code == 200
    assert returned_user.user_id == created_user.user_id
    assert returned_user.timezone == valid_timezone

