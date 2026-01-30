from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
import uuid
from sqlalchemy import Column, DateTime, Integer

if TYPE_CHECKING:
    from .user import User
    from .message import Message

def default_created_at():
    return datetime.now(timezone.utc)

def default_updated_at():
    return datetime.now(timezone.utc)

class ConversationBase(SQLModel):
    pass


class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=default_created_at, sa_column=Column("created_at", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)))
    updated_at: datetime = Field(default_factory=default_updated_at, sa_column=Column("updated_at", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)))

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: int
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime