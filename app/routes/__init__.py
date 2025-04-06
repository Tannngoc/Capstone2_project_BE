# app/routes/__init__.py

from flask import Blueprint

# Khởi tạo Blueprint cho các routes
main = Blueprint('main', __name__)

# Import các routes từ main.py
from app.routes.main import *

# Có thể import thêm các routes khác nếu cần
# from app.routes.other import *
