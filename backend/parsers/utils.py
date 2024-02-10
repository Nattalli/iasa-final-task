import calendar
from collections import Counter
from datetime import timedelta

from nltk.tokenize import word_tokenize
from textblob import TextBlob


def load_stop_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        stop_words = set(word.strip() for word in file.readlines())
    return stop_words


stop_words = load_stop_words('parsers/stop_words.txt')


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
        words = [word.lower() for word in word_tokenize(text) if word.isalnum() and word.lower() not in stop_words]
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
