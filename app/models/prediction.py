from app import db

class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    predicted_price = db.Column(db.Numeric(10, 2), nullable=False)
    prediction_date = db.Column(db.DateTime, nullable=False)
    model_used = db.Column(db.String(50), nullable=False)
