import pytest

from src.config import TaskStatus
from src.models import Tasks


def test_find_all_tasks_empty(tasks_repository):
    # Action
    tasks = tasks_repository.find_all_tasks()

    # Assert
    assert len(tasks) == 5


def test_find_tasks_by_user(tasks_repository, test_db):
    # Act
    tasks_found = tasks_repository.find_tasks_by_user(user_id=2)

    # Assert
    assert len(tasks_found) == 2
    assert tasks_found[0].title == "Do the Carlton Dance"
    assert tasks_found[0].description == "Dance like no one's watching"
    assert tasks_found[1].status == TaskStatus.NOT_STARTED
    assert tasks_found[1].user_id == 2


def test_find_tasks_by_id(tasks_repository, test_db):
    # Act
    task_found = tasks_repository.find_task_by_id(task_id=3)

    # Assert
    assert task_found.title == "Catch a cab"
    assert task_found.description == "Take a cab to Bel-Air"
    assert task_found.status == TaskStatus.COMPLETED
    assert task_found.user_id == 1


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
    assert len(tasks_in_db) == 6
    assert tasks_in_db[5].title == title
    assert tasks_in_db[5].description == description
    assert tasks_in_db[5].status.value == "Not Started"
    assert tasks_in_db[5].user_id == user_id


def test_delete_tasks(tasks_repository, test_db):
    # Action
    tasks_repository.delete_task(task_id=3)

    # Assert
    tasks_in_db = test_db.query(Tasks).all()
    assert len(tasks_in_db) == 4
    # Confirm Carlton is now in index 2 b/c Will's last task was deleted
    assert tasks_in_db[2].title == "Do the Carlton Dance"
    assert tasks_in_db[2].user_id == 2
