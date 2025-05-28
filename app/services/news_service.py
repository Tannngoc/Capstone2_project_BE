import pandas as pd

class NewsService:
    @staticmethod
    def get_all_news():
        df = pd.read_csv("app/db/news.csv")
        news_list = df.to_dict(orient="records")
        return news_list