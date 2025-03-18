from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    roles = db.relationship('UserRole', back_populates='user', cascade='all, delete')

    def __init__(self, username, email, password_hash):
        """Hàm khởi tạo đối tượng User"""
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def to_dict(self):
        """Chuyển đổi đối tượng User thành dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None,
            "roles": [user_role.role_id for user_role in self.roles]  # Lấy danh sách role_id của user
        }
    