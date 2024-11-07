import pytest

from src.config import TaskStatus
from src.models import Users


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
