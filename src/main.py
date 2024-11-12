from flask import Flask, redirect, render_template, url_for, flash

from src.forms.user_forms import LogInForm, CreateUserForm
from flask_login import LoginManager, login_user, login_required
from src.models import Users



app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.config["SECRET_KEY"] = "shhhh_dont_tell_anyone"

login_manager = LoginManager()
login_manager.init_app(app)

# Set the login view to redirect unauthorized users
login_manager.login_view = "login"

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

        if user is not None and user.check_password(password, user.password_hash):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return "Welcome to your dashboard!"


if __name__ == "__main__":
    app.run(debug=True, port=5001)

