import pytest

from src.models import Tasks
from src.config import TaskStatus

def test_find_all_tasks_empty(tasks_repository):
    tasks = tasks_repository.find_all_tasks()
    assert tasks == []


def test_add_task(tasks_repository, test_db):
    # Arrange
    title = "Pick apples"
    description = "Ride trailor to the apple orchard with Jen. Remember the baskets."
    user_id = 42
    new_task = Tasks(title=title, description=description, user_id=user_id)

    # Action
    tasks_repository.add_task(new_task)

    # Assert
    tasks_in_db = test_db.query(Tasks).all()
    assert len(tasks_in_db) == 1
    assert tasks_in_db[0].title == title
    assert tasks_in_db[0].description == description
    assert tasks_in_db[0].status.value == "Not Started"
    assert tasks_in_db[0].user_id == user_id
     


def test_find_tasks_by_user(tasks_repository, test_db):
    # Arrange
    title = "Rake leaves"
    description = "Backyard is covered in leaves. Needs care."
    status = TaskStatus.IN_PROGRESS
    user_id = 36
    new_task = Tasks(title=title, description=description, status=status, user_id=user_id)
    tasks_repository.add_task(new_task)

    # Act
    tasks_found = tasks_repository.find_tasks_by_user(user_id=user_id)


    # Assert
    assert len(tasks_found) == 1
    assert tasks_found[0].title == title
    assert tasks_found[0].description == description
    assert tasks_found[0].status == status 
    assert tasks_found[0].user_id == user_id




