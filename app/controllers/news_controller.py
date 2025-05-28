from flask import jsonify
from app.services.news_service import NewsService

def get_all_news():
    news = NewsService.get_all_news()
    return jsonify(news)