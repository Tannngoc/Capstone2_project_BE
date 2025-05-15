import csv
from typing import List, Dict
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "db" / "news.csv"

def read_news() -> List[Dict[str, str]]:
    news_list = []
    with open(DATA_PATH, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            news_list.append({
                "company": row["company"],
                "title": row["title"],
                "published_date": row["published_date"]
            })
    return news_list

def get_news_by_company(company: str) -> List[Dict[str, str]]:
    all_news = read_news()
    filtered_news = [news for news in all_news if news["company"].lower() == company.lower()]
    return filtered_news

