from flask import jsonify, Blueprint, request
from app.controllers.stock_price_controller import StockPriceController

stock_price = Blueprint('stock_price', __name__, url_prefix="/api/stock-price")

@stock_price.route("/<symbol>/<int:year>/<int:month>")
def get_stock_of_month(symbol, year, month):
    data, status = StockPriceController.get_stock_of_month(symbol, year, month)
    return jsonify(data), status

