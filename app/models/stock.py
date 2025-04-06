from app import db

class Stock(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    exchange = db.Column(db.String(50), nullable=False)
    
    prices = db.relationship('StockPrice', backref='stock', lazy=True, cascade='all, delete')
    predictions = db.relationship('Prediction', backref='stock', lazy=True, cascade='all, delete')
