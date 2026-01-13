from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from sqlmodel import SQLModel
import os
import sys

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from backend.src.models.user import User
from backend.src.models.task import Task
from backend.src.config import settings

# this is the Alembic Config object
config = context.config

# Override sqlalchemy.url with the database URL from settings
# Alembic needs a synchronous connection, so convert async URL to sync URL
database_url = settings.database_url
if database_url.startswith("postgresql+asyncpg://"):
    # Convert asyncpg URL to regular postgresql for Alembic (uses psycopg2)
    database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
elif database_url.startswith("sqlite"):
    # Keep SQLite as-is for development
    pass
config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()