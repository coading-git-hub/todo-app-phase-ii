from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
import uuid
from sqlalchemy import Column, DateTime

if TYPE_CHECKING:
    from .user import User

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column("created_at", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column("updated_at", DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)))

    # Relationship
    user: "User" = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None