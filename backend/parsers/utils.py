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
        current_month = today.month
        current_year = today.year
        _, days_in_current_month = calendar.monthrange(current_year, current_month)
        return today.replace(day=1) - timedelta(days=1)
    elif choice == '3 місяці':
        three_months_ago = today.replace(day=1) - timedelta(days=1)
        for _ in range(2):
            three_months_ago = three_months_ago.replace(day=1) - timedelta(days=1)
        return three_months_ago
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
