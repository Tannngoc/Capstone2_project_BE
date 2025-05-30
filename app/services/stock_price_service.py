from app import db
from app.models import StockPrice, Stock
from sqlalchemy import desc

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
    
    @staticmethod
    def get_latest_stock_summary():
        """Lấy dữ liệu stock mới nhất của mỗi doanh nghiệp"""
        results = []
        stocks = Stock.query.all()
        for stock in stocks:
            latest = (
                StockPrice.query
                .filter_by(stock_id=stock.id)
                .order_by(desc(StockPrice.date))
                .first()
            )
            prev = (
                StockPrice.query
                .filter_by(stock_id=stock.id)
                .order_by(desc(StockPrice.date))
                .offset(1)
                .first()
            )
            if latest:
                close = latest.close_price
                prev_close = prev.close_price if prev else None
                change = close - prev_close if prev_close is not None else None
                percent_change = (change / prev_close * 100) if prev_close and prev_close != 0 else None
                results.append({
                    "symbol": stock.symbol,
                    "close": close,
                    "change": change,
                    "percent_change": round(percent_change, 2) if percent_change is not None else None,
                    "volume": latest.volume,
                })
        return results
    
