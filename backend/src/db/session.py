from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.orm import sessionmaker
from ..config import settings

# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.debug,  # Log SQL queries in debug mode
    pool_pre_ping=True,  # Verify connections before use
)

# Create session factory using SQLModel's Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create database tables based on SQLModel models."""
    SQLModel.metadata.create_all(bind=engine)