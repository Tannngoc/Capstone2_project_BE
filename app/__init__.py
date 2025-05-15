import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config

# Load biến môi trường từ .env
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))

# ✅ Khởi tạo db và migrate trước nhưng chưa gọi init_app
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_url_path="/static")

    # Cấu hình app
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config.from_object(Config)

    # ✅ Khởi tạo db & migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Import models bên trong app context để tránh lỗi vòng lặp
    with app.app_context():
        from app.models import Stock, StockPrice, User, Role, UserRole, Order, Notification, Prediction, Transaction
        db.create_all()

    # ✅ Import và đăng ký blueprint sau khi db đã init
    from app.views.stock_price_view import stock_price
    from app.views.order_view import order
    from app.views.ai_api import model_bp
    from app.views.news_view import news_blueprint
    app.register_blueprint(news_blueprint)
    app.register_blueprint(model_bp)
    app.register_blueprint(stock_price)
    app.register_blueprint(order)

    return app