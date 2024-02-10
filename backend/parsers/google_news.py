from datetime import datetime

from backend.settings import GOOGLE_NEWS_API
from parsers.utils import calculate_date
from newsapi import NewsApiClient


newsapi = NewsApiClient(api_key=GOOGLE_NEWS_API)


def get_news_articles(keyword: str, date_range: str) -> list:
    today = datetime.now().date()
    last_date = calculate_date(today, date_range)
    articles = newsapi.get_everything(q=keyword, from_param=last_date.strftime('%Y-%m-%d'),
                                      to=today.strftime('%Y-%m-%d'))

    return articles['articles']
