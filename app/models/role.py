from app import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __init__(self, name):
        """Hàm khởi tạo đối tượng Role"""
        self.name = name

    def to_dict(self):
        """Chuyển đổi đối tượng Role thành dictionary"""
        return {
            "id": self.id,
            "name": self.name
        }
    
    