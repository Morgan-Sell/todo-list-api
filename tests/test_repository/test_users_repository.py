import pytest

from src.config import TaskStatus
from src.models import Users
from src.security import check_password_hash


def test_find_all_users(users_repository):
    # Action
    users = users_repository.find_all_users()

    # Assert
    assert len(users) == 2
    assert users[0].username == "Will_Smith"
    assert users[1].username == "Carlton_Banks"


def test_find_user_by_id(users_repository):
    # Action
    user = users_repository.find_user_by_id(user_id=2)

    # Assert
    assert user.username == "Carlton_Banks"


def test_get_user_password(users_repository):
    # Test Case 1: User exists
    password = users_repository.get_user_password(username="Will_Smith")
    assert password == "hashed_fresh_password"

    # Test Case 2: User does not exist
    password = users_repository.get_user_password(username="Uncle_Phil")
    assert password is None


def test_add_user(users_repository, test_db):
    # Arrange
    username = "Geoffrey_Butler"
    password = "whitegloves"

    # Arrange
    users_repository.add_user(username=username, password=password)

    # Assert
    all_users = test_db.query(Users).all()
    assert len(all_users) == 3
    assert all_users[2].username == username
    assert all_users[2].password_hash != password
    assert check_password_hash(all_users[2].password_hash, password)


def test_change_user_password(users_repository, test_db):
    # TODO: create test after creating generate_password_hash()
    pass


def test_delete_user(users_repository, test_db):
    # TODO: create test after creating authentication
    pass