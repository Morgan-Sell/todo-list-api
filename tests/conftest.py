import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import TaskStatus
from src.models import Base, Tasks, Users
from src.repository.tasks_repository import TasksRespository
from src.repository.users_repository import UsersRepository


@pytest.fixture(scope="function")
def test_db():
    """In-memory SQLite database for testing"""
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)  # create tables

    # Provide the session to the test
    db = TestingSessionLocal()
    try:
        # In West Philadelphia, born and raised...
        will = Users(username="Will_Smith", password_hash="hashed_fresh_password")
        carlton = Users(
            username="Carlton_Banks", password_hash="hashed_carlton_password"
        )
        db.add_all([will, carlton])
        db.commit()

        # Will's tasks
        task1 = Tasks(
            title="Chill out, maxin'",
            description="Relaxing after school",
            status=TaskStatus.NOT_STARTED,
            user_id=will.id,
        )
        task2 = Tasks(
            title="Shoot some b-ball",
            description="Basketball with friends",
            status=TaskStatus.IN_PROGRESS,
            user_id=will.id,
        )
        task3 = Tasks(
            title="Catch a cab",
            description="Take a cab to Bel-Air",
            status=TaskStatus.COMPLETED,
            user_id=will.id,
        )

        # Carlton's tasks
        task4 = Tasks(
            title="Do the Carlton Dance",
            description="Dance like no one's watching",
            status=TaskStatus.COMPLETED,
            user_id=carlton.id,
        )
        task5 = Tasks(
            title="Argue with Will",
            description="Friendly banter with Will",
            status=TaskStatus.NOT_STARTED,
            user_id=carlton.id,
        )

        db.add_all([task1, task2, task3, task4, task5])
        db.commit()

        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def tasks_repository(test_db):
    """Fixture to provide a TasksRepository instance with the test database session."""
    return TasksRespository(test_db)


@pytest.fixture(scope="function")
def users_repository(test_db):
    """Fixture to provide a UsersRepository instance with the test database session."""
    return UsersRepository(test_db)
