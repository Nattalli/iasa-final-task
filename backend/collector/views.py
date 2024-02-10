from collections import Counter, OrderedDict
from datetime import datetime, timedelta

from rest_framework.decorators import api_view
from rest_framework.response import Response

from collector.serializers import GeneralAnalysisSerializer, ArticleSerializer
from parsers.google_news import get_news_articles
from parsers.utils import translate_sentiment, analyze_articles, calculate_date
from statsmodels.tsa.arima.model import ARIMA


@api_view(['GET'])
def search_articles(request):
    search_keyword = request.query_params.get('keyword', '')
    date_range = request.query_params.get('date_range', '')

    search_articles = get_news_articles(search_keyword, date_range)

    keywords, sentiments, patterns = analyze_articles(search_articles)

    all_keywords = [keyword for article_keywords in keywords for keyword in article_keywords]
    top_trends = Counter(all_keywords).most_common(6)
    trends = [keyword[0] for keyword in top_trends if keyword[0] != search_keyword][:5]

    current_count = len(search_articles)

    if current_count <= 5:
        prediction = 'Less then 5'
    else:
        dates = [article.get('publishedAt', '') for article in search_articles]
        daily_counts = Counter([date.split('T')[0] for date in dates])

        if len(daily_counts.values()) <= 5:
            prediction = 'Less than 5'
        else:
            model = ARIMA(list(daily_counts.values()), order=(5, 1, 0))
            model_fit = model.fit()

            prediction = int(model_fit.forecast()[0])

    sentiment_counts = Counter(sentiments)
    total_sentiments = len(sentiments)
    sentiment_percentages = {translate_sentiment(sentiment): count / total_sentiments * 100 for sentiment, count in
                             sentiment_counts.items()}
    total_percentage = sum(sentiment_percentages.values())
    normalized_sentiment_percentages = {key: value / total_percentage * 100 for key, value in
                                        sentiment_percentages.items()}

    today = datetime.now().date()
    last_date = calculate_date(today, date_range)
    date_range = [last_date + timedelta(days=i) for i in range((today - last_date).days + 1)]

    daily_word_usage = OrderedDict()
    for date in date_range:
        articles_on_date = [article for article in search_articles if
                            article.get('publishedAt', '').startswith(str(date))]
        daily_word_usage[date.strftime('%Y-%m-%d')] = len(articles_on_date)

    general_analysis_data = {
        "trends": trends,
        "general_behavior": normalized_sentiment_percentages,
        "count": current_count,
        "prediction": prediction,
        "daily_word_usage": daily_word_usage,
    }
    general_analysis_serializer = GeneralAnalysisSerializer(general_analysis_data)

    serialized_articles = []
    for article, article_keywords, sentiment, pattern in zip(search_articles, keywords, sentiments, patterns):
        article_data = {
            "title": article.get('title', ''),
            "source": article.get('source', '').get('name', ''),
            "date": article.get('publishedAt', ''),
            "description": article.get('description', ''),
            "short_content": article.get('content', ''),
            "author": article.get('author', ''),
            "link": article.get('url', ''),
            "keywords": article_keywords,
            "pattern": pattern,
            "behavior": translate_sentiment(sentiments[search_articles.index(article)] if
                                            search_articles.index(article) < len(sentiments) else 0)
        }
        serialized_article = ArticleSerializer(article_data)
        serialized_articles.append(serialized_article.data)

    return Response({
        "general_articles_analyze": general_analysis_serializer.data,
        "each_article_analyze": serialized_articles
    })
