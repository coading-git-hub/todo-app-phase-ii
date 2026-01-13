from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from datetime import timedelta
from ..services.auth import verify_password, create_access_token, hash_password
from ..models.user import UserCreate, UserSignIn, UserRead, User
from ..db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from ..utils.sanitization import sanitize_email


router = APIRouter()


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(user_create: UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        # Sanitize email input
        sanitized_email = sanitize_email(user_create.email)

        # Check if user already exists
        result = await session.execute(select(User).where(User.email == sanitized_email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )

        # Create new user - need to use async session properly
        hashed_password = hash_password(user_create.password)
        db_user = User(email=sanitized_email, hashed_password=hashed_password)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        # Return user info without password
        return UserRead(
            id=db_user.id,
            email=db_user.email,
            created_at=db_user.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


@router.post("/signin", response_model=dict)
async def signin(user_signin: UserSignIn, session: AsyncSession = Depends(get_async_session)):
    try:
        # Sanitize email input
        sanitized_email = sanitize_email(user_signin.email)

        # Get user from database
        result = await session.execute(select(User).where(User.email == sanitized_email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(user_signin.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(days=7)  # 7 days expiry
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        # Return token and user info
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "created_at": user.created_at
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )