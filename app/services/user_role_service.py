from app import db
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole

def add_role_to_user(user_id: int, role_name: str):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404
    
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return {"error": "Role not found"}, 404
    
    existing = UserRole.query.filter_by(user_id=user.id, role_id=role.id).first()
    if existing:
        return {"error": "User already has this role"}, 409
    
    user_role = UserRole(user_id=user.id, role_id=role.id)
    db.session.add(user_role)
    db.session.commit()
    db.session.refresh(user)

    return {"message": f"Role '{role_name}' added to user '{user.username}'."}, 200

def remove_role_from_user(user_id: int, role_name: str):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404
    
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return {"error": "Role not found"}, 404
    
    user_role = UserRole.query.filter_by(user_id=user.id, role_id=role.id).first()
    if not user_role:
        return {"error": "User does not have this role"}, 404
    
    db.session.delete(user_role)
    db.session.commit()
    return {"message": f"Role '{role_name}' removed from user '{user.username}'."}, 200
