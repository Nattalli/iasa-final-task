from datetime import datetime

from parsers.utils import calculate_date, analyze_articles
from newsapi import NewsApiClient


newsapi = NewsApiClient(api_key="d0d2b6eb585641d4a15a6bc59b8fa46c")


def get_news_articles(keyword: str, date_range: str) -> list:
    today = datetime.now().date()
    last_date = calculate_date(today, date_range)
    articles = newsapi.get_everything(q=keyword, from_param=last_date.strftime('%Y-%m-%d'),
                                      to=today.strftime('%Y-%m-%d'))

    return articles['articles']


search_keyword = 'COVID'
search_date_range = '1 тиждень'
search_articles = get_news_articles(search_keyword, search_date_range)

keywords, sentiments, patterns = analyze_articles(search_articles)

print("Keywords:")
for i, kw in enumerate(keywords):
    print(f"Article {i + 1}: {kw}")

print("\nSentiments:")
for i, sentiment in enumerate(sentiments):
    print(f"Article {i + 1}: {sentiment}")

print("\nPatterns:")
for i, pattern in enumerate(patterns):
    print(f"Article {i + 1}: {pattern}")