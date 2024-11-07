import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.repository.tasks_repository import TasksRespository


@pytest.fixture(scope="function")
def test_db():
    """In-memory SQLite database for testing"""
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)  # create tables

    # Provide the session to the test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Clean up database


@pytest.fixture(scope="function")
def tasks_repository(test_db):
    """Fixture to provide a TasksRepository instance with the test database session."""
    return TasksRespository(test_db)
