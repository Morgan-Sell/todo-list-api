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


def test_add_task_success(client, app, tasks_repository, users_repository):
    with app.app_context():
        username = "Carlton_Banks"
        # Use app.session to ensure user is bound to the session
        user = app.session.query(Users).filter_by(username=username).first()

        # Explicity refresh the user to avoid DetachedInstance Error
        # app.session.refresh(user)
        
        # Simulate user login
        with client.session_transaction() as session:
            session["_user_id"] = str(user.id)
        
        task_data = {
            "title": "Organize bowties",
            "description": "Sort bowties by color and season.",
            "status": "In Progress",
        }

        response = client.post(
            url_for("tasks.add_task", user_id=user.id),
            data=task_data,
            follow_redirects=True,
        )

        # Assert: Redirect to the view_tasks page
        assert response.status_code == 200
        assert b"Task successfully created." in response.data

        # Assert: Task exists in the database
        tasks = tasks_repository.find_tasks_by_user(user.id)
        assert len(tasks) == 3
        assert any(
            task.title == "Organize bowties"
            and task.description == "Sort bowties by color and season."
            for task in tasks
        )