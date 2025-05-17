from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app import db
from flask_jwt_extended import create_access_token

def register_user(username, email, password):
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return None, "Username or email already exists"

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    default_role = Role.query.filter_by(name="admin").first()
    if default_role:
        user_role = UserRole(user_id=user.id, role_id=default_role.id)
        db.session.add(user_role)
        db.session.commit()
    else:
        print("⚠️ Role 'investor' chưa tồn tại, không thể gán role cho user!")

    return user, None


def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = create_access_token(identity=user.id)
        roles = db.session.query(Role.name)\
            .join(UserRole, UserRole.role_id == Role.id)\
            .filter(UserRole.user_id == user.id).all()
        role_names = [r[0] for r in roles]
        return {"access_token": token, "username": user.username, "roles": role_names}
    return None
