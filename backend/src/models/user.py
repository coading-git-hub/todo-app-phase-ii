from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)


class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


# Pydantic models for API requests/responses
class UserCreate(BaseModel):
    email: str
    password: str


class UserSignIn(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: uuid.UUID
    email: str
    created_at: datetime

    class Config:
        from_attributes = True