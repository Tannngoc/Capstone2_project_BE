from flask import jsonify, Blueprint, request
from app.controllers.order_controller import OrderController

order = Blueprint('orders', __name__, url_prefix="/api/orders")

@order.route("/place", methods=["POST"])
def place_order():
    """API đặt lệnh mua/bán"""
    data = request.get_json()
    response, status = OrderController.place_order(data)
    return jsonify(response), status

@order.route("/user/<int:user_id>", methods=["GET"])
def get_orders_by_user(user_id):
    """API lấy danh sách lệnh của user"""
    response, status = OrderController.get_orders_by_user(user_id)
    return jsonify(response), status

@order.route("/update/<int:order_id>", methods=["PUT"])
def update_order_status(order_id):
    """API cập nhật trạng thái lệnh"""
    data = request.get_json()
    status = data.get("status")
    response, status = OrderController.update_order_status(order_id, status)
    return jsonify(response), status
