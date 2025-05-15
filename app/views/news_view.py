from flask import Blueprint, jsonify
from app.services.news_service import read_news, get_news_by_company

news_blueprint = Blueprint('news', __name__)

@news_blueprint.route('/news', methods=['GET'])
def get_all_news():
    news_data = read_news()
    return jsonify({"data": news_data})

@news_blueprint.route('/news/<company>', methods=['GET'])
def get_company_news(company):
    news_data = get_news_by_company(company)
    return jsonify({"data": news_data})
