from rest_framework.decorators import api_view
from rest_framework.response import Response

from collector.serializers import GeneralAnalysisSerializer, ArticleSerializer
from parsers.google_news import get_news_articles, analyze_articles


@api_view(['GET'])
def search_articles(request):
    search_keyword = request.query_params.get('keyword', '')
    date_range = request.query_params.get('date_range', '')

    search_articles = get_news_articles(search_keyword, date_range)

    keywords, sentiments, patterns = analyze_articles(search_articles)

    general_analysis_data = {
        "trends": keywords,
        "general_behavior": sum(sentiments) / len(sentiments) if sentiments else 0,
        "prediction": "Some prediction here"
    }
    general_analysis_serializer = GeneralAnalysisSerializer(general_analysis_data)

    serialized_articles = []
    for article in search_articles:
        article_data = {
            "title": article.get('title', ''),
            "source": article.get('source', ''),
            "date": article.get('publishedAt', ''),
            "description": article.get('description', ''),
            "short_content": article.get('content', ''),
            "author": article.get('author', ''),
            "link": article.get('url', ''),
            "keywords": [],
            "behavior": sentiments[search_articles.index(article)] if search_articles.index(article) < len(
                sentiments) else 0,
            "pattern": patterns[search_articles.index(article)] if search_articles.index(article) < len(
                patterns) else ""
        }
        serialized_article = ArticleSerializer(article_data)
        serialized_articles.append(serialized_article.data)

    return Response({
        "general_articles_analyze": general_analysis_serializer.data,
        "each_article_analyze": serialized_articles
    })
