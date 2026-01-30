import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from src.main import app
from src.db.session import SessionLocal, get_session
from httpx import AsyncClient
from fastapi.testclient import TestClient



@pytest.fixture
def client():
    from sqlmodel import create_engine
    from sqlalchemy.orm import sessionmaker
    from src.db.session import get_session

    # Create in-memory test database engine for complete isolation
    test_engine = create_engine("sqlite:///:memory:", echo=False)

    # Create tables in test database
    SQLModel.metadata.create_all(bind=test_engine)

    # Create sessionmaker for test database
    test_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    # Override the session dependency
    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as tc:
        yield tc

    # Clean up
    app.dependency_overrides.clear()  # Clear overrides after test