from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from src.config import TaskStatus


class AddTaskForm(FlaskForm):

    title = StringField("Title:", validators=[DataRequired()])
    description = StringField("Description:", validators=[DataRequired()])
    status = SelectField(
        "Status:",
        choices=[(status.value, status.value) for status in TaskStatus],
        validators=[DataRequired()]
    )
    submit = SubmitField("Create Task")
