from unittest.mock import MagicMock, patch
from urllib.parse import urlparse

from flask import url_for

from src.security import check_password_hash


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


# -- REGISTER TEST CASES --
def test_register_page_loads(client, app):
    with app.app_context():
        response = client.get(url_for("auth.register"))
        assert response.status_code == 200
        assert b"SIGN UP" in response.data


def test_register_valid_data(client, app, users_repository):
    with app.app_context():
        new_user = "Uncle_Phil"
        new_password = "willlllll"
        response = client.post(
            url_for("auth.register"),
            data={
                "username": new_user,
                "password": new_password,
                "confirm_password": new_password,
            },
            follow_redirects=True,
        )

        # Assert: Registration was successful
        assert response.status_code == 200
        assert b"Account successfully created. You can now log in." in response.data

        # Assert: New user exists in the database
        user = users_repository.find_user_by_username(new_user)
        assert user is not None
        assert check_password_hash(user.password_hash, new_password)


def test_register_existing_username(client, app, users_repository):
    with app.app_context():
        existing_user = "Will_Smith"
        existing_password = "fresh_password"

        response = client.post(
            url_for("auth.register"),
            data={
                "username": existing_user,
                "password": existing_password,
                "confirm_password": existing_password,
            },
            follow_redirects=True,
        )

        # Assert: Registration failed due to existing username
        assert response.status_code == 200
        assert (
            b"Username already exists. Please choose a different one." in response.data
        )

        # Assert: Ensure the database remains unchanged
        user = users_repository.find_user_by_username(existing_user)
        assert user is not None


def test_register_password_mismatch(client, app):
    with app.app_context():
        new_user = "Geoffrey"
        new_password = "best_butler_eva"
        mismatched_password = "slap_will"

        response = client.post(
            url_for("auth.register"),
            data={
                "username": new_user,
                "password": new_password,
                "confirm_password": mismatched_password,
            },
            follow_redirects=True,
        )

        # Assert: Registration failed due to mismatched passwords
        assert response.status_code == 200
        assert b"Passwords must match." in response.data


def test_register_empty_fields(client, app):
    with app.app_context():
        response = client.post(
            url_for("auth.register"),
            data={"username": "", "password": "", "confirm_password": ""},
            follow_redirects=True,
        )

        # Assert: Registration failed due to empty fields
        assert response.status_code == 200
        assert b"This field is required." in response.data


def test_register_redirect_to_login(client, app, users_repository):
    with app.app_context():
        new_user = "Aunt_Viv"
        new_password = "belairqueen"

        response = client.post(
            url_for("auth.register"),
            data={
                "username": new_user,
                "password": new_password,
                "confirm_password": new_password,
            },
            follow_redirects=False,
        )

        # Assert: Redirect to login page
        assert response.status_code == 302
        assert urlparse(response.location).path == url_for(
            "auth.login", _external=False
        )
