from urllib.parse import urlparse

from flask import url_for
from flask_login import login_user

from src.models import Tasks, Users


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
            session["_user_id"] = str(user_id)  # simulate login session

        response = client.get(url_for("tasks.add_task", user_id=user_id))
        assert response.status_code == 200
        assert b"Add Task" in response.data
        assert b"Title" in response.data
        assert b"Description" in response.data
        assert b"Status" in response.data


def test_add_task_success(client, app, tasks_repository, users_repository):
    with app.app_context():
        user = users_repository.find_user_by_username("Carlton_Banks")

        # Simulate user login
        with client:
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)


def test_add_task_page_load(client, app, users_repository):
    """
    Test that the add task page loads successfully.
    """
    with app.app_context():
        user = users_repository.find_user_by_username("Carlton_Banks")
        assert (
            user is not None
        ), "User 'Carlton_Banks' should exist in the test database."

        # Simulate user login
        with client:
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)

            # Access the add task page
            response = client.get(url_for("tasks.add_task", user_id=user.id))
            assert response.status_code == 200
            assert b"Add Task" in response.data


def test_add_task_success(client, app, tasks_repository, users_repository):
    """
    Test adding a task successfully.
    """
    with app.app_context():
        user = users_repository.find_user_by_username("Carlton_Banks")
        assert (
            user is not None
        ), "User 'Carlton_Banks' should exist in the test database."

        # Simulate user login
        with client:
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)

            # Task data to be added
            task_data = {
                "title": "Organize bowties",
                "description": "Sort bowties by color and season.",
                "status": "In Progress",
            }

            # Submit the form to add a new task
            response = client.post(
                url_for("tasks.add_task", user_id=user.id),
                data=task_data,
                follow_redirects=True,
            )

            # Assert: Redirect to task views
            assert response.status_code == 200
            assert b"Task successfully created." in response.data

            # Assert: Verify the task exists in the database
            tasks = tasks_repository.find_tasks_by_user(user.id)
            assert len(tasks) == 3  # Carlton initially had 2 tasks
            assert any(
                task.title == "Organize bowties"
                and task.description == "Sort bowties by color and season."
                for task in tasks
            )


def test_add_task_invalid_form(client, app, users_repository):
    with app.app_context():
        user = users_repository.find_user_by_username("Carlton_Banks")

        # Simulate user login
        with client:
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)

            # Invalid task data (missing required fields)
            task_data = {
                "title": "",
                "description": "",
                "status": "In Progress",
            }

            # Submit the form with invalid data
            response = client.post(
                url_for("tasks.add_task", user_id=user.id),
                data=task_data,
                follow_redirects=False,
            )

            # Assert: The form should re-render with validation errors
            assert response.status_code == 200
            assert b"This field is required." in response.data


def test_add_task_unauthorized_access(client, app):
    with app.app_context():
        # Attempt to access the add task without login
        response = client.get(
            url_for("tasks.add_task", user_id=1), follow_redirects=True
        )

        # Assert: Redirect to login page
        assert response.status_code == 200
        assert b"LOGIN" in response.data


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
            response = client.get(
                url_for("tasks.get_task_details", task_id=invalid_task_id)
            )

            # Assert: Task not found
            assert response.status_code == 404
            error_data = response.get_json()
            assert (
                error_data["error"]
                == f"Task ID {invalid_task_id} does not exist for this user."
            )


def test_get_task_details_unauthenticated(client, app):
    with app.app_context():
        # Attempt to retrive task details without logging in
        response = client.get(url_for("tasks.get_task_details", task_id=1))

        # Assert: User is redirected to login page
        assert response.status_code == 302
        assert url_for("auth.login", _external=False) in response.headers["Location"]


# -- DELETE_TASK TEST CASES --
def test_delete_task_success(client, app, tasks_repository, users_repository):
    with app.app_context():
        user = users_repository.find_user_by_username("Carlton_Banks")
        tasks = tasks_repository.find_tasks_by_user(user.id)

        task_to_delete = tasks[0]

        # Simulate user login
        with client:
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)

            # Submit the form to delete a task
            response = client.post(
                url_for("tasks.delete_task", user_id=user.id),
                data={"id": task_to_delete.id},
                follow_redirects=True,
            )

            # Assert: Successful redirect to delete_task page
            assert response.status_code == 200
            assert b"Task successfully deleted." in response.data

            # Assert: Task no longert exists in the database
            remaining_tasks = tasks_repository.find_tasks_by_user(user.id)
            assert task_to_delete.id not in [task.id for task in remaining_tasks]


def test_delete_task_not_found(client, app, tasks_repository, users_repository):
    with app.app_context():
        user = users_repository.find_user_by_username("Carlton_Banks")

        # Use an invalid task ID
        invalid_task_id = 99999

        # Simulate user login
        with client:
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)

            # Submit the form with an invalid task ID
            response = client.post(
                url_for("tasks.delete_task", user_id=user.id),
                data={"id": invalid_task_id},
                follow_redirects=True,
            )

            # Assert: User is informed that the task isn't associated with Carlton_Banks
            assert response.status_code == 200
            assert (
                f"Task # {invalid_task_id} is not associated with this user. Enter another task ID.".encode(),
                response.data,
            )


def test_delete_task_unauthenticated(client, app):
    with app.app_context():
        response = client.post(
            url_for("tasks.delete_task", user_id=1),
            data={"id": 1},
            follow_redirects=False,
        )

        # Assert: User is redirect to the login page
        assert response.status_code == 302
        assert url_for("auth.login", _external=False) in response.headers["Location"]


# -- EDIT_TASK TEST CASES --
def test_edit_task_success(client, app, tasks_repository, users_repository):
    with app.app_context():
        user = users_repository.find_user_by_username("Carlton_Banks")
        task = tasks_repository.find_tasks_by_user(user.id)[0]

        # Simualte user login
        with client:
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)

            edit_data = {
                "id": task.id,
                "title": "Learn a new dance",
                "description": "Let's bring back the macarena.",
                "status": "Completed",
            }

            # Send POST request to edit the task
            response = client.post(
                url_for("tasks.edit_task", user_id=user.id),
                data=edit_data,
                follow_redirects=True,
            )

            # Assert: Successfully redirect to view tasks
            assert response.status_code == 200
            assert b"Task successfully created." in response.data

            # Assert: Verify the task was updated
            updated_task = tasks_repository.find_task_by_id(task.id)
            assert updated_task.title == "Learn a new dance"
            assert updated_task.description == "Let's bring back the macarena."
            assert updated_task.status == "Completed"


def test_edit_task_invalid_task_id(client, app, tasks_repository, users_repository):
    with app.app_context():
        user = users_repository.find_user_by_username("Carlton_Banks")

        # Simulate user login
        with client:
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)

            # Data with an invalid task ID
            invalid_edit_data = {
                "id": 777,  # Non-existent task ID
                "title": "Non-existent task",
                "description": "This task does not exist.",
                "status": "In Progress",
            }

            # send POST request to edit the task
            response = client.post(
                url_for("tasks.edit_task", user_id=user.id),
                data=invalid_edit_data,
                follow_redirects=True,
            )

            # Assert: Redirect to the edit page with an error message
            assert response.status_code == 200
            assert b"Task # 777 is not associated with this user." in response.data


def test_edit_task_invalid_form(client, app, tasks_repository, users_repository):
    with app.app_context():
        user = users_repository.find_user_by_username("Carlton_Banks")

        # Simulate user login
        with client:
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)

            # Data with missing ID field (ID is required)
            invalid_edit_data = {
                "id": "",
                "title": "Get into Princeton",
                "description": "Must do it on my own to please dad!",
                "status": "In Progress",
            }

            # Send POST request to edit the task
            response = client.post(
                url_for("tasks.edit_task", user_id=user.id),
                data=invalid_edit_data,
                follow_redirects=True,
            )

            # Assert: Validation error appes in the response
            assert response.status_code == 200
            assert (
                b"This field is required." in response.data
            )  # Check for field validation error
            assert (
                b"Edit Your Task" in response.data
            )  # Ensure the user is redirected back to the form
