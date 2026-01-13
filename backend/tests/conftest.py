import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from backend.src.main import app
from backend.src.db.database import AsyncSessionLocal
from httpx import AsyncClient


# Create test database engine
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.asyncio.fixture
async def async_client():
    # Create tables in test database
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create async session
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    # Clean up
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)