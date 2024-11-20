from urllib.parse import urlparse

from flask import url_for
from flask_login import login_user
from src.models import Users


# -- VIEW_TASKS TEST CASES --
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


# -- ADD_TASK TEST CASES --
def test_add_task_page_loads(client, app):
    with app.app_context():
        user_id = 1
        with client.session_transaction() as session:
            session["_user_id"] = str(user_id) # simulate login session
       
        response = client.get(url_for("tasks.add_task", user_id=user_id))
        assert response.status_code == 200
        assert b"Add Task" in response.data
        assert b"Title" in response.data
        assert b"Description" in response.data
        assert b"Status" in response.data        


# -- GET_TASK_DETAILS TEST CASES --
def test_get_task_details_success(client, app, users_repository, tasks_repository):
    with app.app_context():
        user = users_repository.find_user_by_username("Will_Smith")
        tasks = tasks_repository.find_tasks_by_user(user.id)

        # Simulate login
        with client:
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)
            
            # Get the details for the first task
            task_id = tasks[0].id
            response = client.get(url_for("tasks.get_task_details", task_id=task_id))

            # Assert: Request was successful
            assert response.status_code == 200
            task_data = response.get_json()
            assert task_data["title"] == tasks[0].title
            assert task_data["description"] == tasks[0].description
            assert task_data["status"] == tasks[0].status


def test_get_task_details_not_found(client, app, users_repository):
    with app.app_context():
        user = users_repository.find_user_by_username("Will_Smith")

        # Simulate login
        with client:
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)
            
            # Try to fetch a task doesn't exist
            invalid_task_id = 99999
            response = client.get(url_for("tasks.get_task_details", task_id=invalid_task_id))

            # Assert: Task not found
            assert response.status_code == 404
            error_data = response.get_json()
            assert error_data["error"] == f"Task ID {invalid_task_id} does not exist for this user."


def test_get_task_details_unauthenticated(client, app):
    with app.app_context():
        # Attempt to retrive task details without logging in
        response = client.get(url_for("tasks.get_task_details", task_id=1))

        # Assert: User is redirected to login page
        assert response.status_code == 302
        assert url_for("auth.login", _external=False) in response.headers["Location"]