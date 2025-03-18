from app import db

class Stock(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    prices = db.relationship('StockPrice', backref='stock', lazy=True, cascade='all, delete')
    predictions = db.relationship('Prediction', backref='stock', lazy=True, cascade='all, delete')

    def __init__(self, symbol, name):
        self.symbol = symbol.upper()
        self.name = name.strip()

    def to_dict(self):
        return {"id": self.id, "symbol": self.symbol, "name": self.name}