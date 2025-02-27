from typing import AsyncGenerator, Generator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from db.db import Base, get_async_session
from src.api.dependencies import uow
from src.config import settings
from src.main import app

# Create async engine for tests
test_engine = create_async_engine(
    settings.DATABASE_URL_TEST,
    poolclass=NullPool,
    echo=False,
)

# Create async session maker
test_async_session_maker = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
    autoflush=False,
)


# Override dependencies for tests
@pytest.fixture(scope="session")
def override_dependencies() -> Generator[None, None, None]:
    # Override get_async_session dependency
    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async with test_async_session_maker() as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_async_session

    # Override UOW dependencies
    uow.dependency_overrides(test_async_session_maker)

    yield

    # Clean up overrides after tests
    app.dependency_overrides.clear()


# Setup and teardown database
@pytest.fixture(scope="session")
async def setup_database() -> AsyncGenerator[None, None]:
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Drop all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Create FastAPI test application
@pytest.fixture(scope="session")
def test_app(override_dependencies: None) -> FastAPI:
    return app


# Create async client for tests
@pytest.fixture(scope="function")
async def async_client(
    setup_database: None, test_app: FastAPI
) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url="http://test",
    ) as client:
        yield client
