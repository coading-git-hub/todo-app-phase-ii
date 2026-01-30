from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
from uuid import UUID
from ..config import settings
from ..models.user import User
from sqlmodel import select
from ..db.session import get_session  # Import sync session
from ..db.database_async import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session  # Import sync session type


security = HTTPBearer()


def verify_token_sync(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """Verify JWT token synchronously and return the authenticated user."""
    try:
        if not credentials or not credentials.credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = credentials.credentials

        # Decode the JWT token
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials - no user ID in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Convert user_id to UUID
        user_uuid = UUID(user_id)

        # Get user from database using sync session
        user = session.exec(select(User).where(User.id == user_uuid)).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValueError as e:
        # Handle invalid UUID format
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token format: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like 401) to ensure they're properly handled
        raise
    except Exception as e:
        # Catch any other unexpected exceptions and return 401 instead of 500
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """Verify JWT token and return the authenticated user."""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        # Decode the JWT token
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials - no user ID in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Convert user_id to UUID
        user_uuid = UUID(user_id)

        # Get user from database
        result = await session.execute(select(User).where(User.id == user_uuid))
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValueError as e:
        # Handle invalid UUID format
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token format: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )