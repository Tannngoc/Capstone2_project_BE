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
            f"Kính gửi {user.username},\n\n"
            f"Chúng tôi xin xác nhận rằng bạn đã đặt lệnh {order_type.upper()} với các thông tin sau:\n"
            f"• Mã cổ phiếu: {stock_symbol}\n"
            f"• Số lượng: {quantity}\n"
            f"• Giá đặt: {price}\n"
            f"• Mã lệnh: {order.id}\n"
            f"• Trạng thái: {order.status}\n\n"
            "Nếu bạn có bất kỳ thắc mắc nào, vui lòng liên hệ bộ phận hỗ trợ khách hàng: +84918809264.\n\n"
            "Trân trọng,\n"
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
