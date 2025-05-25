
from app.services.user_service import UserService

class UserController:
    @staticmethod
    def get_all_users():
        return UserService.get_all_users(), 200

    @staticmethod
    def get_user_by_name(username):
        return UserService.get_user_by_name(username)

    # @staticmethod
    # def get_users_by_role(role):
    #     return UserService.get_users_by_role(role)
