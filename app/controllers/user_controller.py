from app.services.user_service import UserService

class UserController:
    @staticmethod
    def fetch_user_by_id(user_id):
        return UserService.get_user_by_id(user_id)

    @staticmethod
    def fetch_all_users():
        return UserService.get_all_users()

    @staticmethod
    def fetch_users_by_role(role_name):
        return UserService.get_users_by_role(role_name)
    
    @staticmethod
    def update_user(user_id, data):
        return UserService.update_user(user_id, data)

    @staticmethod
    def delete_user(user_id):
        return UserService.delete_user(user_id)
