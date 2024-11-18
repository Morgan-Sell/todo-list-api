from flask import Blueprint, flash, jsonify, redirect, render_template, url_for
from flask_login import current_user, login_required

from src.forms.task_form import AddTaskForm, DeleteTaskForm, EditTaskForm
from src.models import SessionLocal, Tasks
from src.repository.tasks_repository import TasksRespository

tasks_blueprint = Blueprint("tasks", __name__)


@tasks_blueprint.route("/<int:user_id>", methods=["GET", "POST"])
@login_required
def view_tasks(user_id):
    session = SessionLocal()
    task_repo = TasksRespository(session)
    tasks = task_repo.find_tasks_by_user(user_id)
    session.close()
    return render_template("view_tasks.html", tasks=tasks)


@tasks_blueprint.route("/add/<int:user_id>", methods=["GET", "POST"])
@login_required
def add_task(user_id):
    form = AddTaskForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        status = form.status.data

        session = SessionLocal()
        task_repo = TasksRespository(session)

        task = Tasks(
            title=title, description=description, status=status, user_id=user_id
        )
        task_repo.add_task(task)
        session.close()

        flash("Task successfully created.", "success")
        return redirect(url_for("tasks.view_tasks", user_id=user_id))

    return render_template("add_task.html", form=form, user_id=user_id)


@tasks_blueprint.route("/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_task(user_id):
    form = EditTaskForm()

    if form.validate_on_submit():
        # gather data from the form
        task_id = form.id.data
        new_title = form.title.data or None  # Convert blank to None
        new_description = form.description.data or None  # Convert blank to None
        new_status = form.status.data or None  # Convert blank to None

        # initiate DB and collect relevant data
        session = SessionLocal()
        task_repo = TasksRespository(session)
        tasks = task_repo.find_tasks_by_user(user_id)
        all_ids = [task.id for task in tasks]

        # Check is username has access to the selected task
        if task_id not in all_ids:
            flash(
                f"Task # {task_id} is not associated with this user. Enter another task ID.",
                "danger",
            )
            session.close()
            return redirect(url_for("tasks.edit_task", user_id=user_id))

        # User is able to edit task
        task_repo.edit_task(
            task_id=task_id,
            title=new_title,
            description=new_description,
            status=new_status,
        )
        flash("Task successfully created.", "success")
        return redirect(url_for("tasks.view_tasks", user_id=user_id))

    return render_template("edit_task.html", form=form, user_id=user_id)


@tasks_blueprint.route("/delete/<int:user_id>", methods=["GET", "POST"])
@login_required
def delete_task(user_id):
    form = DeleteTaskForm()

    if form.validate_on_submit():
        task_id = form.id.data

        # initiate DB and collect relevant data
        session = SessionLocal()
        task_repo = TasksRespository(session)
        tasks = task_repo.find_tasks_by_user(user_id)
        all_ids = [task.id for task in tasks]

        # Check if task belongs to the user
        if task_id not in all_ids:
            flash(
                f"Task # {task_id} is not associated with this user. Enter another task ID.",
                "danger",
            )
            session.close()
            return redirect(url_for("tasks.delete_task", user_id=user_id))

    return render_template("delete_task.html", form=form, user_id=user_id)


@tasks_blueprint.route("/api/<int:task_id>")
@login_required
def get_task_details(task_id):
    session = SessionLocal()
    task_repo = TasksRespository(session)
    task = task_repo.find_task_by_id(task_id)
    session.close()

    if task is not None:
        return jsonify(
            {
                "title": task.title,
                "description": task.description,
                "status": task.status,
            }
        )
    else:
        return (
            jsonify({"error": f"Task ID {task_id} does not exist for this user."}),
            404,
        )
