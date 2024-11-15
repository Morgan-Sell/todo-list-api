import pytest

from src.config import TaskStatus
from src.models import Tasks


def test_find_all_tasks(tasks_repository):
    # Action
    tasks = tasks_repository.find_all_tasks()

    # Assert
    assert len(tasks) == 5


def test_find_tasks_by_user(tasks_repository):
    # Act
    tasks_found = tasks_repository.find_tasks_by_user(user_id=2)

    # Assert
    assert len(tasks_found) == 2
    assert tasks_found[0].title == "Do the Carlton Dance"
    assert tasks_found[0].description == "Dance like no one's watching"
    assert tasks_found[1].status == "Not Started"
    assert tasks_found[1].user_id == 2


def test_find_tasks_by_id(tasks_repository):
    # Act
    task_found = tasks_repository.find_task_by_id(task_id=3)

    # Assert
    assert task_found.title == "Catch a cab"
    assert task_found.description == "Take a cab to Bel-Air"
    assert task_found.status == "Completed"
    assert task_found.user_id == 1


def test_add_task(tasks_repository, test_db):
    # Arrange
    title = "Pick apples"
    description = "Ride trailor to the apple orchard with Jen. Remember the baskets."
    user_id = 42
    new_task = Tasks(title=title, description=description, user_id=user_id, status="Not Started")

    # Action
    tasks_repository.add_task(new_task)

    # Assert
    tasks_in_db = test_db.query(Tasks).all()
    assert len(tasks_in_db) == 6
    assert tasks_in_db[5].title == title
    assert tasks_in_db[5].description == description
    assert tasks_in_db[5].status == "Not Started"
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


def test_edit_task_title(tasks_repository, test_db):
    # Arrange
    task = tasks_repository.find_task_by_id(1)
    new_title = "Chillin' Out, Relaxin' All Cool"

    # Action
    tasks_repository.edit_task(task_id=task.id, title=new_title)

    # Assert
    updated_task = tasks_repository.find_task_by_id(task.id)
    assert updated_task.title == "Chillin' Out, Relaxin' All Cool"
    assert updated_task.description == "Relaxing after school"
    assert updated_task.status == "Not Started"


def test_edit_task_description(tasks_repository, test_db):
    # Arrange
    task = tasks_repository.find_task_by_id(2)
    new_description = "Playing basketball with DJ Jazzy Jeff"

    # Action
    tasks_repository.edit_task(task_id=task.id, description=new_description)

    # Assert
    updated_task = tasks_repository.find_task_by_id(task.id)
    assert updated_task.title == "Shoot some b-ball"
    assert updated_task.description == "Playing basketball with DJ Jazzy Jeff"
    assert updated_task.status == "In Progress"


def test_edit_task_status(tasks_repository, test_db):
    # Arrange
    task = tasks_repository.find_task_by_id(3)
    new_status = "Completed"

    # Action
    tasks_repository.edit_task(task_id=task.id, status=new_status)

    # Assert
    updated_task = tasks_repository.find_task_by_id(task.id)
    assert updated_task.title == "Catch a cab"
    assert updated_task.description == "Take a cab to Bel-Air"
    assert updated_task.status == "Completed"