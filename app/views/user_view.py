# app/routes/user_routes.py
from flask import Blueprint, jsonify

from app.controllers.user_controller import UserController

user = Blueprint("users", __name__, url_prefix="/api/users")

@user.route("/", methods=["GET"])
def get_all_users():
    response, status = UserController.get_all_users()
    return jsonify(response), status

@user.route("/name/<string:username>", methods=["GET"])
def get_user_by_name(username):
    response, status = UserController.get_user_by_name(username)
    return jsonify(response), status

# @user.route("/role/<string:role>", methods=["GET"])
# def get_users_by_role(role):
#     response, status = UserController.get_users_by_role(role)
#     return jsonify(response), status
