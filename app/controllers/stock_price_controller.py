from app.services.stock_price_service import StockPriceService

class StockPriceController:
    @staticmethod
    def get_stock_of_month(symbol, year, month):
        """API lấy dữ liệu giá cổ phiếu theo tháng"""
        stock_id = StockPriceService.get_stock_id(symbol)
        if not stock_id:
            return {"error": f"Không tìm thấy mã {symbol}"}, 404

        stock_prices = StockPriceService.get_stock_of_month(stock_id, year, month)
        return [sp.to_dict() for sp in stock_prices], 200
