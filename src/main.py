from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user

from src.forms.task_form import AddTaskForm
from src.forms.user_forms import RegisterForm, LogInForm
from src.models import Base, SessionLocal, Tasks, Users, engine
from src.repository.users_repository import UsersRepository
from src.repository.tasks_repository import TasksRespository
from src.security import generate_password_hash

app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.config["SECRET_KEY"] = "shhhh_dont_tell_anyone"

login_manager = LoginManager()
login_manager.init_app(app)

# Set the login view to redirect unauthorized users
login_manager.login_view = "login"

# Ensure tables are created
Base.metadata.create_all(bind=engine)


@login_manager.user_loader
def load_user(user_id):
    session = SessionLocal()
    user_repo = UsersRepository(session)
    user = user_repo.find_user_by_id(user_id)
    session.close()
    return user


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LogInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        print("Form submitted with:", username, password)
        session = SessionLocal()
        user_repo = UsersRepository(session)
        user = user_repo.find_user_by_username(username)


        if user is None:
            session.close()
            flash("That email does not exist. Please try again.", "danger")
        elif not user_repo.check_password(password, user.password_hash):
            session.close()
            flash("Invalid password. Please try again.", "danger")
        else:
            login_user(user)
            session.close()
            return redirect(url_for("view_tasks", user_id=user.id))

    return render_template("login.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return "Welcome to your dashboard!"


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # create a database session
        session = SessionLocal()
        user_repo = UsersRepository(session)

        if user_repo.find_user_by_username(username) is not None:
            flash(
                "Username already exists. Please choose a different one.", "danger"
            )
            session.close()
            return redirect(url_for("register"))

        user_repo.add_user(username, password)
        session.close()
        flash("Account successfully created. You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/tasks/<int:user_id>")
@login_required
def view_tasks(user_id):
    session = SessionLocal()
    task_repo = TasksRespository(session)
    tasks = task_repo.find_tasks_by_user(user_id)
    session.close()
    return render_template("view_tasks.html", tasks=tasks)


@app.route("/add_task/<int:user_id>", methods=["GET", "POST"])
@login_required
def add_task(user_id):
    
    # Print to confirm function entry
    print("Entered add_task function")

    # Print user_id to confirm the URL parameter is being received correctly
    print(f"Received user_id: {user_id}")
    
    
    form = AddTaskForm()

    if form.validate_on_submit():

        print("Form was submitted and validated successfully")


        title = form.title.data
        description = form.description.data
        status = form.status.data
        print(f"Form Data - Title: {title}, Description: {description}, Status: {status}")


        session = SessionLocal()
        task_repo = TasksRespository(session)

        task = Tasks(title=title, description=description, status=status, user_id=user_id)
        task_repo.add_task(task)
        session.close()

        flash("Task successfully created.", "success")
        return redirect(url_for("view_tasks", user_id=user_id))

    return render_template("add_task.html", form=form, user_id=user_id)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
