from app import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    executed_price = db.Column(db.Numeric(10, 2), nullable=False)
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship('Order', backref='transactions')
