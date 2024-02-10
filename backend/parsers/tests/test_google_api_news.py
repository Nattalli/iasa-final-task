import unittest

from parameterized import parameterized

from parsers.google_news import get_news_articles


class TestGetNewsArticles(unittest.TestCase):
    @parameterized.expand([
        ("Python", "1 тиждень", 100),
        ("Кіт", "1 тиждень", 0),
        ("Kyiv", "1 місяць", 100),
    ])
    def test_get_news_articles(self, keyword, date_range, counter):
        articles = get_news_articles(keyword, date_range)
        self.assertEqual(len(articles), counter)
