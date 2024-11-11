import pytest

from src.config import TaskStatus
from src.models import Users
from src.security import check_password_hash, generate_password_hash

from unittest.mock import patch
from bcrypt import hashpw, gensalt

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
    original_password = "fresh_password"
    hashed_password = users_repository.get_user_password(username="Will_Smith")
    assert check_password_hash(hashed_password, original_password)

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


def test_add_user_user_already_exists(users_repository):
    # Arrange
    username = "Will_Smith"
    password = "basketball"

    # Arrange
    result = users_repository.add_user(username=username, password=password)

    # Assert
    assert result is False


def test_delete_user(users_repository, test_db):
    # Arrange
    username = "Will_Smith"
    password = "fresh_password"  # The plain text password we intend to "check"

    # Action: mock check_password_hash due to plaintext password in test_db
    with patch("src.security.check_password_hash", return_value=True):
        result = users_repository.delete_user(username=username, password=password)

    # Assert
    assert result is True  # Successful deletion should return True
    assert test_db.query(Users).filter_by(username=username).first() is None


def test_delete_user_wrong_password(users_repository, test_db):
    # Arrange
    username = "Will_Smith"
    password = "wrong_password"

    # Action
    result = users_repository.delete_user(username=username, password=password)

    # Assert
    assert result is False


def test_change_user_password(users_repository, test_db):
    # Arrange
    username = "Will_Smith"
    old_password = "hashed_fresh_password"
    new_password = "letsgobelair"

    # Action
    result = users_repository.change_user_password(username=username, new_password=new_password)

    # Assert
    will_smith = test_db.query(Users).filter_by(username=username).first()
    assert result is True
    assert will_smith.password_hash != old_password


def test_change_user_password_user_does_not_exist(users_repository, test_db):
    # Arrange
    username = "Snoop_Dog"
    old_password = "hashed_fresh_password"
    new_password = "letsgobelair"

    # Action
    result = users_repository.change_user_password(username=username, new_password=new_password)

    # Assert
    assert result is False
