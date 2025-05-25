# app/services/user_service.py
from app.models.user import User
from app.models.user_role import UserRole

class UserService:
    @staticmethod
    def get_all_users():
        users = User.query.all()
        return [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'created_at': u.created_at
        } for u in users]

    @staticmethod
    def get_user_by_name(username):
        users = User.query.filter_by(username=username).all()
        if not users:
            return {"error": "Không tìm thấy người dùng"}, 404
        return [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
        } for u in users], 200

    # @staticmethod
    # def get_users_by_role(role_name):
    #     users = User.query.join(User.roles).filter(UserRole.role == role_name).all()
    #     if not users:
    #         return {"error": "Không tìm thấy người dùng với vai trò này"}, 404
    #     return [{
    #         'id': u.id,
    #         'username': u.username,
    #         'email': u.email,
    #         'roles': [r.role for r in u.roles]
    #     } for u in users], 200
