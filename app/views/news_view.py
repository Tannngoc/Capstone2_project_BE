from app.controllers.news_controller import get_all_news, get_latest_news_per_company
from flask import Blueprint

news_bp = Blueprint("news", __name__, url_prefix="/api/news")

@news_bp.route('/', methods=['GET'])
def fetch_all_news():
    print(get_all_news())
    print("Fetching all news")
    return get_all_news()

@news_bp.route('/latest', methods=['GET'])
def fetch_latest_news_per_company():
    return get_latest_news_per_company()