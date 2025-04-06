from flask import render_template
from app.routes import main  # Sử dụng Blueprint đã khai báo trong __init__.py

@main.route('/')
def index():
    return render_template('index.html')
