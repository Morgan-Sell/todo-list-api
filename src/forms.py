from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class UserCreateForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=4, max=25, message="Username must be between 4 and 25 characters.")
            ]
        )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=25, message="Password must be between 8 and 25 characters.")
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match.")
        ]
    )

    submit = SubmitField("Register")


class LogInForm(FlaskForm):

    username =  StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")