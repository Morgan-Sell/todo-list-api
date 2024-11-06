from src.crud import create_task, create_user
from src.models import Tasks, Users


def test_create_user(test_db):
    # Arrange
    username = "Homer Simpson"
    password_hash = "sprinkledonuts"

    # Act
    create_user(test_db, username, password_hash)

    # Assert
    user = test_db.query(Users).filter_by(id=1).first()
    assert user.username == username
    assert user.password_hash == password_hash


def test_create_task_for_user(test_db):
    # Arrange
    title = "Pick apples"
    description = "Ride trailor to the apple orchard with Jen. Remember the baskets."
    user_id = 42

    # Act
    create_task(test_db, title, description, user_id)

    # Assert
    task = test_db.query(Tasks).filter_by(title=title).first()
    assert task.title == title
    assert task.description == description
    assert task.user_id == user_id
