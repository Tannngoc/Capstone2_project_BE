from app import db
from app.models import StockPrice, Stock

class StockPriceService:
    @staticmethod
    def get_stock_id(symbol):
        """Lấy stock_id từ bảng stocks dựa trên symbol"""
        stock = Stock.query.filter_by(symbol=symbol).first()
        return stock.id if stock else None

    @staticmethod
    def get_stock_of_month(stock_id, year, month):
        """Lấy dữ liệu giá cổ phiếu theo tháng"""
        return (
            StockPrice.query
            .filter(StockPrice.stock_id == stock_id,
                    db.extract('year', StockPrice.date) == year,
                    db.extract('month', StockPrice.date) == month)
            .order_by(StockPrice.date.asc())
            .all()
        )
    
