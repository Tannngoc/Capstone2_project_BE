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
