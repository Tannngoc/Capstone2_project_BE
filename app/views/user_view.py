from flask import Blueprint, jsonify
from app.controllers.user_controller import UserController

user_bp = Blueprint("user", __name__, url_prefix="/api/user")

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserController.fetch_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    users = UserController.fetch_all_users()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email
    } for u in users])

@user_bp.route('/users/role/<role_name>', methods=['GET'])
def get_users_by_role(role_name):
    users = UserController.fetch_users_by_role(role_name)
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email
    } for u in users])

from flask import request

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    updated_user = UserController.update_user(user_id, data)
    if not updated_user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'id': updated_user.id,
        'username': updated_user.username,
        'email': updated_user.email
    })

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = UserController.delete_user(user_id)
    if not success:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted successfully'})
