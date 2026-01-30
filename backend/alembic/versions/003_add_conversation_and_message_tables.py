"""Add conversation and message tables

Revision ID: 003
Revises: 002
Create Date: 2026-01-29 18:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
import uuid
from sqlalchemy import Column


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create conversation table
    op.create_table('conversation',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create message table
    op.create_table('message',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.String(length=5000), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for efficient querying
    op.create_index('ix_conversation_user_id', 'conversation', ['user_id'])
    op.create_index('ix_conversation_created_at', 'conversation', ['created_at'])
    op.create_index('ix_message_user_id', 'message', ['user_id'])
    op.create_index('ix_message_conversation_id', 'message', ['conversation_id'])
    op.create_index('ix_message_role', 'message', ['role'])
    op.create_index('ix_message_created_at', 'message', ['created_at'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_message_created_at', table_name='message')
    op.drop_index('ix_message_role', table_name='message')
    op.drop_index('ix_message_conversation_id', table_name='message')
    op.drop_index('ix_message_user_id', table_name='message')
    op.drop_index('ix_conversation_created_at', table_name='conversation')
    op.drop_index('ix_conversation_user_id', table_name='conversation')

    # Drop tables
    op.drop_table('message')
    op.drop_table('conversation')