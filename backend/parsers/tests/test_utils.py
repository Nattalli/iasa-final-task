import unittest
from datetime import datetime
from parameterized import parameterized
from parsers.utils import calculate_date, load_stop_words, translate_sentiment, analyze_articles


class TestCalculateDate(unittest.TestCase):
    @parameterized.expand([
        (datetime(2024, 2, 10), '1 день', datetime(2024, 2, 9)),
        (datetime(2024, 2, 10), '1 тиждень', datetime(2024, 2, 3)),
        (datetime(2024, 2, 10), '1 місяць', datetime(2024, 1, 13)),
        (datetime(2024, 2, 10), '3 місяці', datetime(2023, 11, 11)),
    ])
    def test_calculate_date(self, today, choice, expected_date):
        self.assertEqual(calculate_date(today, choice), expected_date)

    @parameterized.expand([
        (datetime(2024, 2, 10), 'invalid_choice'),
    ])
    def test_invalid_choice(self, today, choice):
        self.assertIsNone(calculate_date(today, choice))


class TestLoadStopWords(unittest.TestCase):
    def test_load_stop_words(self):
        file_path = "parsers/stop_words.txt"
        stop_words = load_stop_words(file_path)
        self.assertIsInstance(stop_words, set)
        self.assertTrue(len(stop_words) > 0)

        expected_stop_words = {"вона", "вони", "та", "у", "and", "or"}
        self.assertTrue(all(word in stop_words for word in expected_stop_words))


class TestTranslateSentiment(unittest.TestCase):
    @parameterized.expand([
        (0.6, "Позитивний"),
        (0.3, "Схвальний"),
        (0, "Нейтральний"),
        (-0.3, "Негативний"),
        (-0.6, "Дуже поганий"),
    ])
    def test_translate_sentiment(self, score, expected_sentiment):
        self.assertEqual(translate_sentiment(score), expected_sentiment)


class TestAnalyzeArticlesIntegration(unittest.TestCase):
    def test_analyze_articles_integration(self):
        articles = [
            {
                'title': 'This is a sample title',
                'description': 'This is a sample description',
                'content': 'This is a sample content',
            },
            {
                'title': 'Another sample title',
                'description': 'Another sample description',
                'content': 'Another sample content',
            }
        ]

        keywords, sentiments, patterns = analyze_articles(articles)

        self.assertIsInstance(keywords, list)
        self.assertIsInstance(sentiments, list)
        self.assertIsInstance(patterns, list)

        self.assertEqual(len(keywords), len(articles))
        self.assertEqual(len(sentiments), len(articles))
        self.assertEqual(len(patterns), len(articles))

        self.assertTrue(all(isinstance(keywords_list, list) for keywords_list in keywords))
        self.assertTrue(all(isinstance(sentiment, (int, float)) for sentiment in sentiments))
        self.assertTrue(all(isinstance(pattern, str) for pattern in patterns))


class TestAnalyzeArticles(unittest.TestCase):
    def test_analyze_articles_empty(self):
        articles = []
        keywords, sentiments, patterns = analyze_articles(articles)
        self.assertEqual(keywords, [])
        self.assertEqual(sentiments, [])
        self.assertEqual(patterns, [])

    def test_analyze_articles_single_article(self):
        articles = [
            {
                'title': 'This is a sample title',
                'description': 'This is a sample description',
                'content': 'This is a sample content',
            }
        ]
        keywords, sentiments, patterns = analyze_articles(articles)
        self.assertEqual(len(keywords), 1)
        self.assertEqual(len(sentiments), 1)
        self.assertEqual(len(patterns), 1)

        self.assertTrue(keywords[0])
        self.assertIsInstance(sentiments[0], (int, float))
        self.assertIsInstance(patterns[0], str)

    def test_analyze_articles_multiple_articles(self):
        articles = [
            {
                'title': 'This is a sample title',
                'description': 'This is a sample description',
                'content': 'This is a sample content',
            },
            {
                'title': 'Another sample title',
                'description': 'Another sample description',
                'content': 'Another sample content',
            }
        ]
        keywords, sentiments, patterns = analyze_articles(articles)
        self.assertEqual(len(keywords), 2)
        self.assertEqual(len(sentiments), 2)
        self.assertEqual(len(patterns), 2)

        self.assertTrue(all(keywords_list for keywords_list in keywords))
        self.assertTrue(all(isinstance(sentiment, (int, float)) for sentiment in sentiments))
        self.assertTrue(all(isinstance(pattern, str) for pattern in patterns))
