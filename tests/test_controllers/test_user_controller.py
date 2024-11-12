from unittest.mock import patch

from src.repository.users_repository import UsersRepository


def test_register_user_missing_fields(client):
    response = client.post("/users/register", json={})
    assert response.status_code == 400
    assert response.json == {"error": "Username and password are required."}


def test_register_user_existing_username(client):
    # Mock username already exists
    with patch.object(UsersRepository, "find_user_by_username", return_value=True):
        response = client.post(
            "/ussers/register",
            json={"username": "existing_user", "password": "password123"},
        )
        assert response.status_code == 409
        assert response.json == {"error": "Username already exists"}


def test_register_user_success(client):
    # Mock username does not exist
    with patch.object(UsersRepository, "find_user_by_username", return_value=False):
        # Mock username
        with patch.object(UsersRepository, "add_user", return_value=True):
            response = client.post(
                "/users/register",
                json={"username": "new_user", "password": "password123"},
            )
            assert response.status_code == 201
            assert response.json == {"message": "User registered."}
