from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from datetime import timedelta
from ..services.auth import verify_password, create_access_token, hash_password, get_user_by_email, create_user
from ..models.user import UserCreate, UserSignIn, UserRead, User
from ..db.database_async import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from ..utils.sanitization import sanitize_email

import logging


router = APIRouter()


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(user_create: UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        # Sanitize email input
        sanitized_email = sanitize_email(user_create.email)

        # Check if user already exists
        existing_user = await get_user_by_email(session, sanitized_email)
        if existing_user:
          logging.warning("Signup failed: email already exists: %s", sanitized_email)
          raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
          )

        # Create new user
        db_user = await create_user(session, user_create)

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
        logging.info("Signin attempt for email: %s", user_signin.email)
        # Sanitize email input
        sanitized_email = sanitize_email(user_signin.email)
        logging.info("Sanitized email: %s", sanitized_email)

        # Get user from database
        user = await get_user_by_email(session, sanitized_email)
        logging.info("User found in DB: %s", user is not None)

        if not user:
            logging.warning("User not found for email: %s", sanitized_email)
            raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Invalid email or password",
              headers={"WWW-Authenticate": "Bearer"},
            )

        password_valid = verify_password(user_signin.password, user.hashed_password)
        logging.info("Password verification result: %s", password_valid)

        if not password_valid:
          logging.warning("Invalid password for email: %s", sanitized_email)
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