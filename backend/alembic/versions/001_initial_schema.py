"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-01-06 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
import uuid


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('user',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create tasks table
    op.create_table('task',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for efficient querying
    op.create_index('ix_task_user_id', 'task', ['user_id'])
    op.create_index('ix_task_created_at', 'task', ['created_at'])
    op.create_index('ix_task_completed', 'task', ['completed'])
    op.create_index('ix_user_email', 'user', ['email'])


def downgrade() -> None:
    # Drop index
    op.drop_index('ix_task_user_id', table_name='task')

    # Drop tables
    op.drop_table('task')
    op.drop_table('user')