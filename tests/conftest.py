import os
import uuid
from typing import AsyncGenerator

import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from backend.db import Base, get_db
from backend.main import app
from backend.models import User

# Load test environment variables
load_dotenv(".env.test")

# Build async test DB URL
TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Use NullPool to avoid connection reuse across concurrent async tests
engine = create_async_engine(
    TEST_DATABASE_URL, future=True, echo=False, poolclass=NullPool
)
AsyncTestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


# 1. Transactional DB session fixture
@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a database session wrapped in a transaction.
    Transaction is rolled back after each test for full isolation.
    """
    async with engine.connect() as connection:
        async with connection.begin() as transaction:
            # Bind a session to this connection
            session = AsyncTestingSessionLocal(bind=connection, expire_on_commit=False)
            yield session
            # Roll back the transaction to clean up
            await transaction.rollback()


# 2. Dependency override fixture
@pytest_asyncio.fixture
def override_get_db(db_session: AsyncSession):
    """Overrides FastAPI get_db to use the transactional test session."""

    async def _override_get_db():
        yield db_session

    return _override_get_db


# 3. Async HTTP client fixture
@pytest_asyncio.fixture
async def async_client(override_get_db) -> AsyncGenerator[AsyncClient, None]:
    """
    Provides an AsyncClient for testing FastAPI endpoints.
    Injects the transactional DB session into the app.
    """
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    # Clean up dependency override after the test
    app.dependency_overrides.pop(get_db)


# 4. Setup and teardown test database (session-scoped)
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    """
    Creates all tables before tests run and drops them after tests finish.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(name="create_user_in_db")
async def create_user_in_db(db_session: AsyncSession) -> User:
    user = User(user_id=uuid.uuid4(), timezone="America/New_York")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user
