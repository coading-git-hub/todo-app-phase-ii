from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from ..config import settings
import logging
import os

logger = logging.getLogger(__name__)

# Create async engine - detect if using PostgreSQL and use appropriate driver
try:
    db_url = settings.DATABASE_URL
    # If using PostgreSQL, ensure we're using async driver
    if "postgresql" in db_url and "asyncpg" not in db_url:
        # Replace psycopg2 with asyncpg for async operations
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

    async_engine = create_async_engine(
        db_url,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=300,
    )
    db_name = db_url.split("@")[-1] if "@" in db_url else db_url.split("/")[-1]
    logger.info(f"Async database engine created: {db_name}")
    logger.info(f"Using database URL: {db_url[:50]}...")
except Exception as e:
    logger.error(f"Failed to create async database engine: {e}")
    raise

# Create async session factory
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency to get async session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session