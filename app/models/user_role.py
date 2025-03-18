from app import db

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    
    user = db.relationship('User', back_populates='roles')
    role = db.relationship('Role', backref='user_roles')

    def __init__(self, user_id, role_id):
        """Hàm khởi tạo đối tượng UserRole"""
        self.user_id = user_id
        self.role_id = role_id

    def to_dict(self):
        """Chuyển đổi đối tượng UserRole thành dictionary"""
        return {
            "user_id": self.user_id,
            "role_id": self.role_id
        }