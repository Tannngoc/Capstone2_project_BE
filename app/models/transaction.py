from app import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    executed_price = db.Column(db.Numeric(10, 2), nullable=False)
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship('Order', backref='transactions')

    def __init__(self, order_id, executed_price, executed_at=None):
        """Hàm khởi tạo đối tượng Transaction"""
        self.order_id = order_id
        self.executed_price = executed_price
        self.executed_at = executed_at or datetime.utcnow()

    def to_dict(self):
        """Chuyển đổi đối tượng Transaction thành dictionary"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executed_price": float(self.executed_price),
            "executed_at": self.executed_at.strftime('%Y-%m-%d %H:%M:%S')
        }