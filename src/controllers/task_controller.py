from flask import Blueprint, jsonify, request

from src.models import SessionLocal
from src.repository.tasks_repository import TasksRespository

task_blueprint = Blueprint("task", __name__)


@task_blueprint.route("/tasks/create", methods=["POST"])
def create_task():
    json = request.json
    title = request.title
    description = request.description
    user_id = request.user_id # TODO: How do I identify the user ID?

    if title is None or description is None:
        return jsonify({"error": "Title and description are required."}), 400

    with SessionLocal() as db:
        task_repo = TasksRespository(db)
        task_repo

