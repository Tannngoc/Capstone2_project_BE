from app import db

class StockPrice(db.Model):
    __tablename__ = 'stock_prices'
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    date = db.Column(db.DateTime, nullable=False)
    year = db.Column(db.Integer)
    open_price = db.Column(db.Numeric(10, 2), nullable=False)
    high_price = db.Column(db.Numeric(10, 2), nullable=False)
    low_price = db.Column(db.Numeric(10, 2), nullable=False)
    close_price = db.Column(db.Numeric(10, 2), nullable=False)
    volume = db.Column(db.BigInteger, nullable=False)

    def __init__(self, stock_id, date, open_price, high_price, low_price, close_price, volume):
        self.stock_id = stock_id
        self.date = date
        self.year = date.year
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume

    def to_dict(self):
        return {
            "id": self.id,
            "stock_id": self.stock_id,
            "date": self.date.strftime("%Y-%m-%d"),
            "year": self.year,
            "open_price": float(self.open_price),
            "high_price": float(self.high_price),
            "low_price": float(self.low_price),
            "close_price": float(self.close_price),
            "volume": self.volume
        }