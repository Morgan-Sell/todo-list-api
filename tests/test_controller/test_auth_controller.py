from unittest.mock import MagicMock, patch
from urllib.parse import urlparse

from flask import url_for
from flask_login import login_user

from src.models import Tasks, Users
from src.repository.users_repository import UsersRepository
from src.security import check_password_hash, generate_password_hash


# -- LOGIN TEST CASES --
def test_login_page_load_success(client, app):
    with app.app_context():
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.is_active = True
        mock_user.username = "Will_Smith"

        # Log in the user
        with patch("flask_login.utils._get_user", return_value=mock_user):
            # perform the request
            response = client.get(url_for("auth.login"))
            assert response.status_code == 200
            assert b"LOGIN" in response.data
            assert b"Peak Performer" in response.data


def test_login_valid_credentails(client, app):
    with app.app_context():
        # simulate user login
        response = client.post(
            url_for("auth.login"),
            data={"username": "Will_Smith", "password": "fresh_password"},
            follow_redirects=False,  # prevents the test client from retriev view_tasks.html content
        )

        # Assert
        assert response.status_code == 302  # Redirect

        # Ensure only paths are compared. Ignore protocl and hostname differences.
        response_path = urlparse(response.location).path
        expected_path = url_for("tasks.view_tasks", user_id=1, _external=False)
        assert response_path == expected_path


def test_login_invalid_username(client, app):
    with app.app_context():
        response = client.post(
            url_for("auth.login"),
            data={"username": "Jazz", "password": "CrushinOnHillary"},
            follow_redirects=True,
        )

        # Assert the login page is returned
        assert response.status_code == 200
        assert b"That username does not exist. Please try again." in response.data
        assert b"LOGIN" in response.data


def test_login_invalid_password(client, app):
    with app.app_context():
        response = client.post(
            url_for("auth.login"),
            data={"username": "Will_Smith", "password": "wrong_password"},
            follow_redirects=True,
        )

        print(response.data.decode())
        # Assert the login page is returned
        assert response.status_code == 200
        assert b"Invalid password. Please try again." in response.data
        assert b"LOGIN" in response.data


def test_login_form_validation(client, app):
    with app.app_context():
        response = client.post(
            url_for("auth.login"),
            data={"username": "", "password": ""},
            follow_redirects=True,
        )

        # Assert that validation errors are displayed
        assert response.status_code == 200
        assert (
            b"Because you're always on top of the mountain (or at least your to-do list)"
            in response.data
        )


# -- LOG OUT TEST CASES --
def test_logout_redirects_to_login_page(client, app):
    with app.app_context():
        # simulate a logged-in user
        with client:
            response = client.get(url_for("auth.logout"), follow_redirects=False)

            # Assert
            assert response.status_code == 302  # Redirect

            # Ensure only paths are compared. Ignore protocl and hostname differences.
            response_path = urlparse(response.location).path
            expected_path = url_for("auth.login", _external=False)
            assert response_path == expected_path


def test_logout_flash_message(client, app, users_repository):
    with app.app_context():
        with client:
            user = users_repository.find_user_by_username("Carlton_Banks")
            # Log in the user via session transaction
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)

            response = client.get(url_for("auth.logout"), follow_redirects=True)

            # Assert
            assert response.status_code == 200
            # Check for flash message
            assert b"You have successfully logged out." in response.data


def test_logout_protected_route_after_logout(client, app, users_repository):
    with app.app_context():
        user = users_repository.find_user_by_username("Carlton_Banks")

        with client:
            # Log in the user via session transaction
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)

            # Assert: successful logout
            response = client.get(url_for("auth.logout"), follow_redirects=True)
            assert response.status_code == 200

            # Assert: Prevent logged out user from accessing protected route
            protect_response = client.get(
                url_for("tasks.view_tasks", user_id=user.id), follow_redirects=True
            )
            assert response.status_code == 200
            assert b"LOGIN" in protect_response.data
