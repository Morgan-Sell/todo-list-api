from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

from src.config import EDIT_TASK_STATUS_LIST, TASK_STATUS_LIST


class AddTaskForm(FlaskForm):

    title = StringField("Title:", validators=[DataRequired()])
    description = StringField("Description:", validators=[DataRequired()])
    status = SelectField(
        "Status:",
        choices=[(status, status) for status in TASK_STATUS_LIST],
        validators=[DataRequired()],
    )
    submit = SubmitField("Create Task")


class EditTaskForm(FlaskForm):

    id = IntegerField("Task ID: ", validators=[DataRequired()])
    title = StringField("Title:")
    description = StringField("Description:")
    status = SelectField(
        "Status:",
        choices=[(status, status) for status in EDIT_TASK_STATUS_LIST],
    )
    submit = SubmitField("Edit Task")
