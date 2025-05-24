from flask import request, jsonify
from app import db
from app.services.auth_service import register_user, login_user
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole

def register():
    data = request.get_json()
    user, error = register_user(data["username"], data["email"], data["password"])
    if error:
        return jsonify({"error": error}), 409
    return jsonify({"message": "User registered successfully"}), 201

def login():
    data = request.get_json()
    result = login_user(data["username"], data["password"])
    if not result:
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify(result), 200

@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    roles = db.session.query(Role.name)\
        .join(UserRole, UserRole.role_id == Role.id)\
        .filter(UserRole.user_id == user.id).all()
    role_names = [r[0] for r in roles]

    return jsonify({
        "username": user.username,
        "email": user.email,
        "roles": role_names
    })

@jwt_required(refresh=True)
def refresh_token():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    return jsonify(access_token=new_access_token), 200