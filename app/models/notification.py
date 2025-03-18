from app import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='notifications')

    def __init__(self, user_id, message, is_read=False):
        """Hàm khởi tạo đối tượng Notification"""
        self.user_id = user_id
        self.message = message
        self.is_read = is_read

    def to_dict(self):
        """Chuyển đổi đối tượng Notification thành dict"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }