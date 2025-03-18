from app import db
from datetime import datetime

class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    predicted_price = db.Column(db.Numeric(10, 2), nullable=False)
    prediction_date = db.Column(db.DateTime, nullable=False)
    model_used = db.Column(db.String(50), nullable=False)

    def __init__(self, stock_id, predicted_price, model_used, prediction_date=None):
        """Hàm khởi tạo đối tượng Prediction"""
        self.stock_id = stock_id
        self.predicted_price = predicted_price
        self.model_used = model_used
        self.prediction_date = prediction_date if prediction_date else datetime.utcnow()

    def to_dict(self):
        """Chuyển đổi đối tượng Prediction thành dictionary"""
        return {
            "id": self.id,
            "stock_id": self.stock_id,
            "predicted_price": float(self.predicted_price),
            "prediction_date": self.prediction_date.isoformat() if self.prediction_date else None,
            "model_used": self.model_used
        }
    