from app.services.order_service import OrderService

class OrderController:
    @staticmethod
    def place_order(data):
        """Xử lý API đặt lệnh"""
        required_fields = ["user_id", "stock_symbol", "order_type", "quantity", "price"]
        if not all(field in data for field in required_fields):
            return {"error": "Thiếu dữ liệu đầu vào"}, 400

        return OrderService.place_order(
            user_id=data["user_id"],
            stock_symbol=data["stock_symbol"],
            order_type=data["order_type"],
            quantity=data["quantity"],
            price=data["price"]
        )

    @staticmethod
    def get_orders_by_user(user_id):
        """Lấy danh sách lệnh của user"""
        return OrderService.get_orders_by_user(user_id), 200

    @staticmethod
    def update_order_status(order_id, status):
        """Cập nhật trạng thái lệnh"""
        if status not in ["PENDING", "COMPLETED", "CANCELLED"]:
            return {"error": "Trạng thái không hợp lệ"}, 400
        return OrderService.update_order_status(order_id, status)
