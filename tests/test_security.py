import pytest

from src.security import check_password_hash, generate_password_hash


def test_generate_password_has():
    # Arrange
    password = "smellYaLater"

    # Act
    hashed_password1 = generate_password_hash(password)
    hashed_password2 = generate_password_hash(password)

    # Assert
    assert hashed_password1 != hashed_password2
    assert isinstance(hashed_password1, str)
    assert isinstance(hashed_password2, str)


def test_check_password_hash_success():
    # Arrange
    password = "carltonDance123"
    hashed_password = generate_password_hash(password)

    # Act & Assert
    assert check_password_hash(
        hashed_password, password
    )  # Should return True for matching passwords


def test_check_password_hash_failure():
    # Arrange
    password = "bornAndRaised"
    wrong_password = "inWestPhilly"
    hashed_password = generate_password_hash(password)

    # Act & Assert
    assert not check_password_hash(
        hashed_password, wrong_password
    )  # Should return False for non-matching passwords
