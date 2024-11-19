from urllib.parse import urlparse

from flask import url_for
from flask_login import login_user


def test_view_tasks_success(client, app, users_repository, tasks_repository):
    with app.app_context():
        user = users_repository.find_user_by_username("Will_Smith")
        assert user is not None, "User should exist in the test database."

        # Simmulate a request context
        with client:
            # Simulate the user has logged in
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)

            # Send GET request to the view_tasks endpoint
            response = client.get(
                url_for("tasks.view_tasks", user_id=user.id), follow_redirects=True
            )

            # Assert: Request was sucessful
            assert response.status_code == 200

            print(response.data.decode())

            # Assert: Tasks to user are displayed
            tasks = tasks_repository.find_tasks_by_user(user.id)
            for task in tasks:
                assert task.title.encode() in response.data
                assert task.description.encode() in response.data


def test_view_tasks_unauthorized_access(app, client):
    with app.app_context():

        # Send GET request without logging in
        response = client.get(url_for("tasks.view_tasks", user_id=1))

        # Assert: Redirect to login page
        assert response.status_code == 302
        assert urlparse(response.location).path == url_for(
            "auth.login", _external=False
        )
