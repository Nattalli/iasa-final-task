from collections import Counter
from datetime import timedelta

from nltk.tokenize import word_tokenize
from textblob import TextBlob

from parsers.constants import STOP_WORDS


def calculate_date(today, choice):
    if choice == '1 день':
        return today - timedelta(days=1)
    elif choice == '1 тиждень':
        return today - timedelta(weeks=1)
    elif choice == '1 місяць':
        return today - timedelta(weeks=4)
    elif choice == '3 місяці':
        return today - timedelta(weeks=13)
    else:
        return None


def analyze_articles(articles):
    keywords = []
    sentiments = []
    patterns = []

    for article in articles:
        title = article.get('title', '')
        description = article.get('description', '')
        content = article.get('content', '')

        if title is None:
            title = ''
        if description is None:
            description = ''
        if content is None:
            content = ''

        text = title + ' ' + description + ' ' + content
        words = [word.lower() for word in word_tokenize(text) if word.isalnum() and word.lower() not in STOP_WORDS]
        word_freq = Counter(words)

        top_keywords = word_freq.most_common(5)
        keywords.append([word[0] for word in top_keywords])

        blob = TextBlob(text)
        sentiments.append(blob.sentiment.polarity)

        patterns.append(article.get('title'))

    return keywords, sentiments, patterns


def translate_sentiment(score):
    if score > 0.5:
        return "Позитивний"
    elif score > 0:
        return "Схвальний"
    elif score == 0:
        return "Нейтральний"
    elif score >= -0.5:
        return "Негативний"
    else:
        return "Дуже поганий"
