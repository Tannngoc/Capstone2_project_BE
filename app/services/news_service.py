import pandas as pd

class NewsService:
    @staticmethod
    def get_all_news():
        df = pd.read_csv("app/db/news.csv")
        news_list = df.to_dict(orient="records")
        return news_list
    
    @staticmethod
    def get_latest_news_per_company(limit=5):
        df = pd.read_csv("app/db/news.csv")
        df = df.sort_values("published_date", ascending=False)
        latest_news = df.groupby("company").head(1)
        latest_news = latest_news.head(limit)
        return latest_news.to_dict(orient="records")