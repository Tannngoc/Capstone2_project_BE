from flask import Blueprint, jsonify
from app.controllers.role_controller import RoleController

role_bp = Blueprint("role", __name__, url_prefix="/api/role")

@role_bp.route("/add", methods=["POST"])
def add_role():
    data, status = RoleController.create_role()
    return jsonify(data), status
