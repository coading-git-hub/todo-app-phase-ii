"""Add timezone to datetime columns

Revision ID: 002
Revises: 001
Create Date: 2026-01-29 17:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Detect the database dialect to handle PostgreSQL vs SQLite differently
    # For PostgreSQL
    conn = op.get_bind()
    dialect_name = conn.dialect.name

    if dialect_name == 'postgresql':
        op.execute("ALTER TABLE task ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at AT TIME ZONE 'UTC';")
        op.execute("ALTER TABLE task ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at AT TIME ZONE 'UTC';")
        op.execute('ALTER TABLE "user" ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at AT TIME ZONE \'UTC\';')

        # If conversation and message tables exist, update them too
        try:
            op.execute("ALTER TABLE conversation ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at AT TIME ZONE 'UTC';")
            op.execute("ALTER TABLE conversation ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at AT TIME ZONE 'UTC';")
            op.execute("ALTER TABLE message ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at AT TIME ZONE 'UTC';")
        except:
            # Tables might not exist yet, that's OK
            pass
    # For SQLite, we skip this migration since we'll rely on the updated model definitions
    # and a fresh database creation will have the correct schema


def downgrade() -> None:
    # For PostgreSQL
    conn = op.get_bind()
    dialect_name = conn.dialect.name

    if dialect_name == 'postgresql':
        op.execute("ALTER TABLE task ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE;")
        op.execute("ALTER TABLE task ALTER COLUMN updated_at TYPE TIMESTAMP WITHOUT TIME ZONE;")
        op.execute("ALTER TABLE user ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE;")

        try:
            op.execute("ALTER TABLE conversation ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE;")
            op.execute("ALTER TABLE conversation ALTER COLUMN updated_at TYPE TIMESTAMP WITHOUT TIME ZONE;")
            op.execute("ALTER TABLE message ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE;")
        except:
            # Tables might not exist, that's OK
            pass
    # For SQLite, nothing to do since we didn't modify the schema