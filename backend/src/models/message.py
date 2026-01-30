from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
import uuid
from sqlalchemy import Column, DateTime

if TYPE_CHECKING:
    from .user import User
    from .conversation import Conversation

class MessageBase(SQLModel):
    role: str = Field(regex="^(user|assistant)$", max_length=20)  # Either 'user' or 'assistant'
    content: str = Field(min_length=1, max_length=5000)


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    conversation_id: int = Field(foreign_key="conversation.id", nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column("created_at", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)))

    # Relationships
    user: "User" = Relationship(back_populates="messages")
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    user_id: uuid.UUID
    conversation_id: int
    created_at: datetime