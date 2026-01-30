from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
import uuid
import sqlalchemy

if TYPE_CHECKING:
    from .task import Task
    from .conversation import Conversation
    from .message import Message

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)


from sqlalchemy import Column, DateTime, String
import sqlalchemy

class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(sa_column=Column("hashed_password", String, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column("created_at", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)))
    # Don't define updated_at field since it's causing conflicts
    # We'll use a custom query in the service layer

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(back_populates="user")
    messages: List["Message"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserSignIn(SQLModel):
    email: str
    password: str


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime