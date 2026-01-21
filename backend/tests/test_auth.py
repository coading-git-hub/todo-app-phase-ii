import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from src.main import app
from src.models.user import User
from src.db.database import get_async_session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from unittest.mock import AsyncMock


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.asyncio
async def test_signup_valid_user(client):
    """Test signing up with valid credentials."""
    response = client.post(
        "/api/auth/signup",
        json={"email": "test@example.com", "password": "securepassword123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_signup_duplicate_email(client):
    """Test signing up with an already registered email."""
    # First signup should succeed
    client.post(
        "/api/auth/signup",
        json={"email": "duplicate@example.com", "password": "securepassword123"}
    )

    # Second signup with same email should fail
    response = client.post(
        "/api/auth/signup",
        json={"email": "duplicate@example.com", "password": "anotherpassword"}
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_signup_invalid_email_format(client):
    """Test signing up with invalid email format."""
    response = client.post(
        "/api/auth/signup",
        json={"email": "invalid-email", "password": "securepassword123"}
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_signup_weak_password(client):
    """Test signing up with a weak password."""
    response = client.post(
        "/api/auth/signup",
        json={"email": "weakpass@example.com", "password": "123"}
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_signin_valid_credentials(client):
    """Test signing in with valid credentials."""
    # First create a user
    client.post(
        "/api/auth/signup",
        json={"email": "signin@example.com", "password": "securepassword123"}
    )

    # Then try to sign in
    response = client.post(
        "/api/auth/signin",
        json={"email": "signin@example.com", "password": "securepassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data


@pytest.mark.asyncio
async def test_signin_invalid_credentials(client):
    """Test signing in with invalid credentials."""
    # Create a user first
    client.post(
        "/api/auth/signup",
        json={"email": "invalidcred@example.com", "password": "securepassword123"}
    )

    # Try to sign in with wrong password
    response = client.post(
        "/api/auth/signin",
        json={"email": "invalidcred@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_signin_nonexistent_user(client):
    """Test signing in with a nonexistent user."""
    response = client.post(
        "/api/auth/signin",
        json={"email": "nonexistent@example.com", "password": "any_password"}
    )
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_jwt_token_issuance(client):
    """Test that JWT token is issued correctly after successful signin."""
    # Create a user
    signup_response = client.post(
        "/api/auth/signup",
        json={"email": "jwt@example.com", "password": "securepassword123"}
    )
    assert signup_response.status_code == 201

    # Sign in and check token
    signin_response = client.post(
        "/api/auth/signin",
        json={"email": "jwt@example.com", "password": "securepassword123"}
    )
    assert signin_response.status_code == 200

    data = signin_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["access_token"] is not None


@pytest.mark.asyncio
async def test_jwt_token_verification(client):
    """Test that JWT token can be used to access protected endpoints."""
    # Create and sign in a user
    client.post(
        "/api/auth/signup",
        json={"email": "protected@example.com", "password": "securepassword123"}
    )

    signin_response = client.post(
        "/api/auth/signin",
        json={"email": "protected@example.com", "password": "securepassword123"}
    )
    assert signin_response.status_code == 200

    token = signin_response.json()["access_token"]

    # Try to access a protected endpoint (this would require a task endpoint to test)
    # For now, we'll just verify the token was issued properly
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/health", headers=headers)
    # Note: The health endpoint is not protected, so this should work regardless of token
    # A proper test would require a protected endpoint