import asyncio
import os
from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.db import Base, get_db
from backend.main import app

# Load test environment variables
load_dotenv(".env.test")

# Build the connection string for the test DB
TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Create test engine and async session
test_engine = create_async_engine(TEST_DATABASE_URL, future=True)
TestingSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)


# Override the get_db dependency to use the test DB
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create and drop all tables once per test session."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def prepare():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def cleanup():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    # Create tables before running tests
    loop.run_until_complete(prepare())
    yield
    # Drop tables after tests
    loop.run_until_complete(cleanup())
    loop.close()


@pytest.fixture
def client():
    """Provide a synchronous TestClient that uses the test database."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture(name="db_session")
async def db_session_fixture() -> AsyncGenerator[AsyncSession, Any]:
    """
    Fixture to provide a direct, isolated database session to a test.

    This creates a session, starts a transaction, yields the session
    to the test, and automatically rolls back the transaction
    after the test finishes.
    """
    async with TestingSessionLocal() as session:
        async with session.begin():  # Start a transaction
            yield session
        # The transaction is automatically rolled back here
        # This keeps your tests isolated from each other
