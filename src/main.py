from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user

from src.forms.user_forms import RegisterForm, LogInForm
from src.models import Base, SessionLocal, Users, engine
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
    return Users.query.get(int(user_id))


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LogInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Users.query.filter_by(username=username).first()

        if user is None:
            flash("That email does not exist. Please try again.", "danger")
        elif not user.check_password(password, user.password_hash):
            flash("Invalid password. Please try again.", "danger")
        else:
            login_user(user)
            return redirect(url_for("dashboard"))

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
        try:
            # check if user already exists
            if session.query(Users).filter_by(username=username).first() is not None:
                flash(
                    "Username already exists. Please choose a different one.", "danger"
                )
                return redirect(url_for("register"))

            hashed_password = generate_password_hash(password)
            new_user = Users(username=username, password_hash=hashed_password)
            session.add(new_user)
            session.commit()

            flash("Account successfully created. You can now log in.", "success")
            return redirect(url_for("login"))

        finally:
            session.close()

    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
