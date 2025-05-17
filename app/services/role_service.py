from app import db
from app.models.role import Role

def add_role(role_name: str):
    existing = Role.query.filter_by(name=role_name).first()
    if existing:
        return {"error": "Role already exists"}, 409

    new_role = Role(name=role_name)
    db.session.add(new_role)
    db.session.commit()
    return {"message": f"Role '{role_name}' created successfully."}, 201

def seed_default_roles():
    for name in ["investor", "admin"]:
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name))
    db.session.commit()
