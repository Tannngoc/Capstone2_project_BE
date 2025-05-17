from flask import request, jsonify
from app.services.user_role_service import add_role_to_user, remove_role_from_user

class UserRoleController:
    @staticmethod
    def add_role():
        data = request.get_json()
        user_id = data.get("user_id")
        role_name = data.get("role_name")
        if not user_id or not role_name:
            return {"error": "Missing user_id or role_name"}, 400
        return add_role_to_user(user_id, role_name)

    @staticmethod
    def remove_role():
        data = request.get_json()
        user_id = data.get("user_id")
        role_name = data.get("role_name")
        if not user_id or not role_name:
            return {"error": "Missing user_id or role_name"}, 400
        return remove_role_from_user(user_id, role_name)
