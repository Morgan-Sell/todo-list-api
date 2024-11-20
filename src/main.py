from flask import Flask, current_app, redirect, url_for
from flask_login import LoginManager

from src.controller.auth_controller import auth_blueprint
from src.controller.tasks_controller import tasks_blueprint
from src.models import Base, SessionLocal, engine
from src.repository.users_repository import UsersRepository

app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.config["SECRET_KEY"] = "shhhh_dont_tell_anyone"
app.session = SessionLocal()

login_manager = LoginManager()
login_manager.init_app(app)

# Set the login view to redirect unauthorized users
login_manager.login_view = "login"

# Ensure tables are created
Base.metadata.create_all(bind=engine)

# Register blueprints to for tasks and authentication controllers
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(tasks_blueprint, url_prefix="/tasks")


@app.route("/")
def root():
    """
    Redirects the root URL - http://127.0.0.1:5001 - to the login page.
    """
    return redirect(url_for("auth.login"))


@login_manager.user_loader
def load_user(user_id):
    session = current_app.session
    user_repo = UsersRepository(session)
    user = user_repo.find_user_by_id(user_id)
    session.close()
    return user


if __name__ == "__main__":
    app.run(debug=True, port=5001)
