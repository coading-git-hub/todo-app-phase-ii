#!/usr/bin/env python3
"""
Test script to verify that JWT authentication is working properly after our fixes.
"""

import jwt
from datetime import datetime, timedelta
from src.config import settings
from src.middleware.jwt_auth import verify_token_sync
from src.db.session import SessionLocal
from src.models.user import User
from src.services.auth import hash_password


def test_jwt_authentication():
    print("Testing JWT authentication functionality...")

    # Create a test user
    with SessionLocal() as session:
        # Create a test user
        import uuid
        unique_email = f"test_{uuid.uuid4()}@example.com"
        test_user = User(
            email=unique_email,
            hashed_password=hash_password("password123"),
            created_at=datetime.utcnow()
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

        print(f"Created test user with ID: {test_user.id}")

        # Create a JWT token for this user
        token_data = {
            "sub": str(test_user.id),
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow()
        }
        token = jwt.encode(token_data, settings.jwt_secret, algorithm="HS256")

        print(f"Generated token: {token[:20]}...")  # Show first 20 chars

        # Now test the verify_token_sync function
        from fastapi.security import HTTPAuthorizationCredentials
        from unittest.mock import Mock

        # Create a mock credentials object to simulate Authorization header
        mock_credentials = Mock()
        mock_credentials.credentials = token

        # Create a new session for the verification
        with SessionLocal() as verify_session:
            try:
                # Call the verify_token_sync function directly
                authenticated_user = verify_token_sync(
                    credentials=mock_credentials,
                    session=verify_session
                )

                print(f"✅ SUCCESS: JWT authentication passed!")
                print(f"   Authenticated user ID: {authenticated_user.id}")
                print(f"   Authenticated user email: {authenticated_user.email}")

                # Verify it's the same user
                if authenticated_user.id == test_user.id:
                    print("✅ User ID matches the test user")
                else:
                    print("❌ User ID does not match")

            except Exception as e:
                print(f"❌ FAILED: JWT authentication failed with error: {e}")
                import traceback
                traceback.print_exc()

        # Clean up: delete the test user
        session.delete(test_user)
        session.commit()

    print("\nJWT authentication test completed!")


def test_invalid_token():
    print("\nTesting invalid token handling...")

    # Test with an invalid token
    from fastapi.security import HTTPAuthorizationCredentials
    from unittest.mock import Mock

    mock_credentials = Mock()
    mock_credentials.credentials = "invalid.token.here"

    with SessionLocal() as session:
        try:
            verify_token_sync(
                credentials=mock_credentials,
                session=session
            )
            print("❌ FAILED: Invalid token should have raised an exception")
        except Exception as e:
            print(f"✅ SUCCESS: Invalid token properly rejected with: {type(e).__name__}")


if __name__ == "__main__":
    test_jwt_authentication()
    test_invalid_token()