from flask import request
from app.services.role_service import add_role

class RoleController:
    @staticmethod
    def create_role():
        data = request.get_json()
        if not data or "name" not in data:
            return {"error": "Missing 'name' field"}, 400
        
        role_name = data["name"].strip()
        if not role_name:
            return {"error": "Role name cannot be empty"}, 400
        
        return add_role(role_name)
