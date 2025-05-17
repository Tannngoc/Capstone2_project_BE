import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from config import Config

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, static_url_path="/static")

    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    with app.app_context():
        from app.models import Stock, StockPrice, User, Role, UserRole, Order, Notification, Prediction, Transaction
        db.create_all()

    from app.views.stock_price_view import stock_price
    from app.views.order_view import order
    from app.views.ai_api import model_bp
    from app.views.auth_view import auth_bp
    from app.views.role_view import role_bp
    from app.views.user_role_view import user_role_bp

    app.register_blueprint(role_bp)
    app.register_blueprint(model_bp)
    app.register_blueprint(stock_price)
    app.register_blueprint(order)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_role_bp)

    return app