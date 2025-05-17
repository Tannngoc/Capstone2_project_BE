from flask import Blueprint, jsonify
from app.controllers.user_role_controller import UserRoleController

user_role_bp = Blueprint("user_role", __name__, url_prefix="/api/user-role")

@user_role_bp.route("/add", methods=["POST"])
def add_user_role():
    data, status = UserRoleController.add_role()
    return jsonify(data), status

@user_role_bp.route("/remove", methods=["POST"])
def remove_user_role():
    data, status = UserRoleController.remove_role()
    return jsonify(data), status
