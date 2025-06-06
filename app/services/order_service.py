from app import db
from app.models.order import Order
from app.models.stock import Stock
from app.models.user import User
from app.utils.email_helper import send_email
from datetime import datetime

class OrderService:
    @staticmethod
    def place_order(user_id, stock_symbol, order_type, quantity, price):
        stock = Stock.query.filter_by(symbol=stock_symbol).first()
        if not stock:
            return {"error": f"Mã cổ phiếu {stock_symbol} không tồn tại"}, 404

        user = User.query.get(user_id)
        if not user:
            return {"error": "Người dùng không tồn tại"}, 404

        order = Order(
            user_id=user.id,
            stock_id=stock.id,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        db.session.add(order)
        db.session.commit()

        subject = f"Xác nhận lệnh {order_type.upper()} cổ phiếu {stock_symbol} - Starfall Predict Stock"

        body = (
            f"Dear {user.username},\n\n"
            f"We confirm that you have successfully placed a {order_type.upper()} order with the following details:\n"
            f"• Stock symbol: {stock_symbol}\n"
            f"• Quantity: {quantity}\n"
            f"• Order price: {price}\n"
            f"• Order ID: {order.id}\n"
            f"• Status: {order.status}\n"
            f"• Total amount: {quantity * price}\n\n"
            "If you have any questions, please contact our customer support at +84918809264.\n\n"
            "Best regards,\n"
            "Starfall Predict Stock"
        )
        send_email(user.email, subject, body)

        return order.to_dict(), 201

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
