from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from ..config import settings
import logging
import os

logger = logging.getLogger(__name__)

# Create async engine
try:
    async_engine = create_async_engine(
        settings.database_url,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=300,
    )
    db_name = settings.database_url.split("@")[-1] if "@" in settings.database_url else settings.database_url.split("/")[-1]
    logger.info(f"Database engine created: {db_name}")
    logger.info(f"Using database URL: {settings.database_url[:50]}...")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
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