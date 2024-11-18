from flask import Blueprint, flash, redirect, render_template, url_for, current_app
from flask_login import login_required, login_user, logout_user

from src.forms.user_forms import LogInForm, RegisterForm
from src.models import SessionLocal
from src.repository.users_repository import UsersRepository

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/")
@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LogInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Enables connection to different databases, e.g., test & prod
        session = current_app.session
        user_repo = UsersRepository(session)
        user = user_repo.find_user_by_username(username)

        if user is None:
            session.close()
            flash("That username does not exist. Please try again.", "danger")
        elif not user_repo.check_password(password, user.password_hash):
            session.close()
            flash("Invalid password. Please try again.", "danger")
        else:
            login_user(user)
            session.close()
            return redirect(url_for("tasks.view_tasks", user_id=user.id))

    return render_template("login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # create a database session
        session = SessionLocal()
        user_repo = UsersRepository(session)

        if user_repo.find_user_by_username(username) is not None:
            flash("Username already exists. Please choose a different one.", "danger")
            session.close()
            return redirect(url_for("auth.register"))

        user_repo.add_user(username, password)
        session.close()
        flash("Account successfully created. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)
