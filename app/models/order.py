from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    order_type = db.Column(db.Enum('BUY', 'SELL', name='order_type'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('PENDING', 'COMPLETED', 'CANCELLED', name='order_status'), nullable=False, default="PENDING")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    executed_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship('User', backref='orders')
    stock = db.relationship('Stock', backref='orders')

    def __init__(self, user_id, stock_id, order_type, quantity, price, status='PENDING', executed_at=None):
        """Hàm khởi tạo đối tượng Order"""
        self.user_id = user_id
        self.stock_id = stock_id
        self.order_type = order_type
        self.quantity = quantity
        self.price = price
        self.status = status
        self.executed_at = executed_at

    def to_dict(self):
        """Chuyển đổi đối tượng Order thành dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "stock_id": self.stock_id,
            "order_type": self.order_type,
            "quantity": self.quantity,
            "price": float(self.price),
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "executed_at": self.executed_at.isoformat() if self.executed_at else None
        }