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
    # SQLite-specific configuration
    if settings.database_url.startswith("sqlite"):
        # Ensure directory exists for SQLite database file
        db_path = settings.database_url.replace("sqlite+aiosqlite:///", "")
        if db_path and db_path != ":memory:":
            db_dir = os.path.dirname(os.path.abspath(db_path))
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
        
        connect_args = {"check_same_thread": False}
        engine_kwargs = {
            "url": settings.database_url,
            "echo": False,
            "connect_args": connect_args,
            "pool_pre_ping": False,  # SQLite doesn't need connection pooling
        }
    else:
        # PostgreSQL/Neon configuration
        # Remove unsupported parameters for asyncpg
        db_url = settings.database_url
        if "channel_binding" in db_url or "sslmode" in db_url:
            from urllib.parse import urlparse, urlencode, parse_qs
            parsed = urlparse(db_url)
            query_params = parse_qs(parsed.query)
            query_params.pop('channel_binding', None)
            query_params.pop('sslmode', None)
            new_query = urlencode(query_params, doseq=True)
            db_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}" if new_query else f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

        engine_kwargs = {
            "url": db_url,
            "echo": False,
            "pool_size": 5,
            "max_overflow": 10,
            "pool_pre_ping": True,
            "pool_recycle": 300,
            "connect_args": {"ssl": True} if "neon" in db_url.lower() else {},
        }
    
    async_engine = create_async_engine(**engine_kwargs)
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