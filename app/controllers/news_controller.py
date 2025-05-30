from flask import jsonify
from app.services.news_service import NewsService

def get_all_news():
    news = NewsService.get_all_news()
    return jsonify(news)

def get_latest_news_per_company():
    news = NewsService.get_latest_news_per_company()
    return jsonify(news)