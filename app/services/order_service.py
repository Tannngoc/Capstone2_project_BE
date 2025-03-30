from app import db
from app.models.order import Order
from app.models.stock import Stock
from datetime import datetime

class OrderService:
    @staticmethod
    def place_order(user_id, stock_symbol, order_type, quantity, price):
        """Đặt lệnh mua/bán cổ phiếu"""
        stock = Stock.query.filter_by(symbol=stock_symbol).first()
        if not stock:
            return {"error": f"Mã cổ phiếu {stock_symbol} không tồn tại"}, 404

        new_order = Order(user_id=user_id, stock_id=stock.id, order_type=order_type, quantity=quantity, price=price)
        db.session.add(new_order)
        db.session.commit()
        return new_order.to_dict(), 201

    @staticmethod
    def get_orders_by_user(user_id):
        """Lấy danh sách lệnh của người dùng"""
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        return [order.to_dict() for order in orders]

    @staticmethod
    def update_order_status(order_id, status):
        """Cập nhật trạng thái lệnh"""
        order = Order.query.get(order_id)
        if not order:
            return {"error": "Không tìm thấy lệnh"}, 404

        order.status = status
        if status == "COMPLETED":
            order.executed_at = datetime.utcnow()
        
        db.session.commit()
        return order.to_dict(), 200
