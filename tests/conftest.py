import pytest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import TaskStatus
from src.controller.auth_controller import auth_blueprint
from src.models import Base, Tasks, Users
from src.repository.tasks_repository import TasksRespository
from src.repository.users_repository import UsersRepository
from src.security import generate_password_hash

from flask_login import LoginManager, AnonymousUserMixin
from src.controller.tasks_controller import tasks_blueprint
from flask.testing import FlaskClient

@pytest.fixture(scope="function")
def test_db():
    """In-memory SQLite database for testing"""
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)  # create tables

    # Provide the session to the test
    db = TestingSessionLocal()
    try:
        # In West Philadelphia, born and raised...
        will = Users(
            username="Will_Smith",
            password_hash=generate_password_hash("fresh_password"),
        )
        carlton = Users(
            username="Carlton_Banks",
            password_hash=generate_password_hash("carlton_password"),
        )
        db.add_all([will, carlton])
        db.commit()

        # Will's tasks
        task1 = Tasks(
            title="Chill out, maxin'",
            description="Relaxing after school",
            status="Not Started",
            user_id=will.id,
        )
        task2 = Tasks(
            title="Shoot some b-ball",
            description="Basketball with friends",
            status="In Progress",
            user_id=will.id,
        )
        task3 = Tasks(
            title="Catch a cab",
            description="Take a cab to Bel-Air",
            status="Completed",
            user_id=will.id,
        )

        # Carlton's tasks
        task4 = Tasks(
            title="Do the Carlton Dance",
            description="Dance like no one's watching",
            status="Completed",
            user_id=carlton.id,
        )
        task5 = Tasks(
            title="Argue with Will",
            description="Friendly banter with Will",
            status="Not Started",
            user_id=carlton.id,
        )

        db.add_all([task1, task2, task3, task4, task5])
        db.commit()

        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def tasks_repository(test_db):
    """Fixture to provide a TasksRepository instance with the test database session."""
    return TasksRespository(test_db)


@pytest.fixture(scope="function")
def users_repository(test_db):
    """Fixture to provide a UsersRepository instance with the test database session."""
    return UsersRepository(test_db)


@pytest.fixture(scope="function")
def app(test_db):
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.config["TESTING"] = True
    app.config["SERVER_NAME"] = "localhost"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["SECRET_KEY"] = "shhhh_dont_tell_anyone"
    app.config["WTF_CSRF_ENABLED"] = False
    
    # Attach test_db session for testing
    app.session = test_db
    
    # Initialize Flask-login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # Enable the loading of users during the test
    @login_manager.user_loader
    def load_user(user_id):
        session = test_db
        user_repo = UsersRepository(session)
        return user_repo.find_user_by_id(user_id)

    # Register blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(tasks_blueprint)

    return app


@pytest.fixture(scope="function")
def client(app):
    # Enables simulation of client requests in Flask for testing
    app.test_client_class = FlaskClient
    client = app.test_client()

    # Set 'current_user' to anonymous user if no user is logged in
    app.jinja_env.globals["current_user"] = AnonymousUserMixin()
    return client
