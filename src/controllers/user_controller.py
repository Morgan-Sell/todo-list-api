from flask import Blueprint, jsonify, request

from src.models import SessionLocal
from src.repository.users_repository import UsersRepository

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/users/register", methods=["POST"])
def register_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return jsonify({"error": "Username and password are required."}), 400

    with SessionLocal() as db:
        user_repo = UsersRepository(db)
        if user_repo.find_user_by_username(username):
            return jsonify({"error": "Username already exists"}), 409

        user_repo.add_user(username, password)

    return jsonify({"message": "User successfully registered!"}), 201


@user_blueprint.route("/users/password", methods=["POST"])
def change_password():
    data = request.json
    username = data.get("username")
    new_password = data.get("new_password")

    if username is None or new_password is None:
        return jsonify({"error": "Username and new password are required."}), 400

    with SessionLocal() as db:
        user_repo = UsersRepository(db)
        user_repo.change_user_password(username, new_password)

    return jsonify({"message": "Password changed."}), 201
