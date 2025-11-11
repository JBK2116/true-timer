"""
Testing file for the `standard_timer` package
"""

import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import User


class TestCreateStandardTimer:
    """
    Tests all required possibilities for creating a standard timer.
    """

    @pytest.mark.asyncio
    async def test_create_standard_timer_missing_user_id(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """
        Tests creating a standard timer with missing user id
        :param async_client: Async client for testing
        :param db_session: Async database connection for testing
        """
        response = await async_client.post(
            "/api/standard", json={"minutes": 20, "hours": 1}
        )
        assert response.status_code == 400
        assert response.json()["detail"] is not None

    @pytest.mark.asyncio
    async def test_create_standard_timer_unknown_user(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """
        Tests creating a standard timer with an unknown/missing user in database
        :param async_client: Async client for testing
        :param db_session: Async database session for testing
        """
        response = await async_client.post(
            "/api/standard",
            json={"minutes": 20, "hours": 1},
            headers={"X-User-ID": str(uuid.uuid4())},
        )
        assert response.status_code == 400
        assert response.json()["message"] is not None

    @pytest.mark.asyncio
    async def test_create_standard_timer_invalid_minutes(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """
        Tests ensuring that minutes is [0, 59]
        :param async_client: Async client for testing
        :param db_session: Async database session for testing
        """
        first_response = await async_client.post(
            "/api/standard",
            json={"minutes": -1, "hours": 1},
            headers={"X-User-ID": str(uuid.uuid4())},
        )
        assert first_response.status_code == 422  # caught by pydantic model validation
        second_response = await async_client.post(
            "/api/standard",
            json={"minutes": 60, "hours": 1},
            headers={"X-User-ID": str(uuid.uuid4())},
        )
        assert second_response.status_code == 422  # caught by pydantic model validation

    @pytest.mark.asyncio
    async def test_create_standard_timer_invalid_hours(
        self, async_client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """
        Tests ensuring that hours is [0, 24]
        :param async_client: Async client for testing
        :param db_session: Async database session for testing
        """
        first_response = await async_client.post(
            "/api/standard",
            json={"minutes": 1, "hours": -1},
            headers={"X-User-ID": str(uuid.uuid4())},
        )
        assert first_response.status_code == 422  # caught by pydantic model validation
        second_response = await async_client.post(
            "/api/standard",
            json={"minutes": 1, "hours": 25},
            headers={"X-User-ID": str(uuid.uuid4())},
        )
        assert second_response.status_code == 422  # caught by pydantic model validation

    @pytest.mark.asyncio
    async def test_create_standard_timer_zero_duration(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        create_user_in_db: User,
    ) -> None:
        """
        Tests ensuring that a timer with zero duration is prevented from creation
        :param create_user_in_db: Created User object saved to database
        :param async_client: Async client for testing
        :param db_session: Async database session for testing
        """
        response = await async_client.post(
            "/api/standard",
            json={"minutes": 0, "hours": 0},
            headers={"X-User-ID": str(create_user_in_db.user_id)},
        )
        assert pytest.raises(
            ValueError
        )  # occurs from sqlalchemy database validation constraints
        assert response.status_code == 400
        assert response.json()["message"] is not None

    @pytest.mark.asyncio
    async def test_create_standard_timer_valid(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        create_user_in_db: User,
    ) -> None:
        """
        Tests creating a standard timer with valid information
        :param async_client: Async client for testing
        :param db_session: Async database session for testing
        :param create_user_in_db: Created User object saved to database
        """
        response = await async_client.post(
            "/api/standard",
            json={"minutes": 20, "hours": 1},
            headers={"X-User-ID": str(create_user_in_db.user_id)},
        )
        assert response.status_code == 200
        assert response.json()["timer_id"] is not None
        assert response.json()["minutes"] is not None
        assert response.json()["hours"] is not None
