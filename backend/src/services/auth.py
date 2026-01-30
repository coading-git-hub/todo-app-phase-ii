from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt
from jose import JWTError, jwt
from fastapi import HTTPException, status
from ..config import settings
from ..models.user import User, UserCreate


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False


def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt."""
    # Ensure password is a string
    if not isinstance(password, str):
        password = str(password)
    
    # Bcrypt has a 72-byte limit
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token with optional expiration time."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.jwt_expiry_days)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm="HS256")
    return encoded_jwt


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    """Get a user by email."""
    result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    """Create a new user with hashed password."""
    hashed_password = hash_password(user_create.password)
    db_user = User(email=user_create.email, hashed_password=hashed_password)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user