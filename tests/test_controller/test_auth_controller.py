from unittest.mock import patch
from urllib.parse import urlparse

from src.models import Users, Tasks
from src.repository.users_repository import UsersRepository
from flask import url_for
from flask_login import login_user

from unittest.mock import patch, MagicMock

from src.security import check_password_hash, generate_password_hash


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
            assert b'LOGIN' in response.data
            assert b'Peak Performer' in response.data


def test_login_valid_credentails(client, app):
    with app.app_context():
        # simulate user login
        response = client.post(
            url_for("auth.login"),
            data={"username": "Will_Smith", "password": "fresh_password"},
            follow_redirects=False, # prevents the test client from retriev view_tasks.html content
        )

        # Assert
        assert response.status_code == 302 # Redirect
      
        # Ensure only paths are compared. Ignore protocl and hostname differences.
        response_path = urlparse(response.location).path
        expected_path = url_for("tasks.view_tasks", user_id=1, _external=False)
        assert response_path == expected_path