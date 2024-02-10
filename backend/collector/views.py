from collections import Counter

from rest_framework.decorators import api_view
from rest_framework.response import Response

from collector.serializers import GeneralAnalysisSerializer, ArticleSerializer
from parsers.google_news import get_news_articles
from parsers.utils import translate_sentiment, analyze_articles


@api_view(['GET'])
def search_articles(request):
    search_keyword = request.query_params.get('keyword', '')
    date_range = request.query_params.get('date_range', '')

    search_articles = get_news_articles(search_keyword, date_range)

    keywords, sentiments, patterns = analyze_articles(search_articles)

    all_keywords = [keyword for article_keywords in keywords for keyword in article_keywords]
    top_trends = Counter(all_keywords).most_common(5)
    trends = [keyword[0] for keyword in top_trends]

    prediction = trends

    general_analysis_data = {
        "trends": trends,
        "general_behavior": translate_sentiment(sum(sentiments) / len(sentiments) if sentiments else 0),
        "prediction": prediction,
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
