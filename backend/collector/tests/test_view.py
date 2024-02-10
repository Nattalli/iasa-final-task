from django.test import RequestFactory
from django.urls import reverse
from rest_framework.test import APITestCase

from collector.views import search_articles


class TestSearchArticlesView(APITestCase):
    def test_search_articles_view_correct_params(self):
        url = reverse('search_articles')
        request = RequestFactory().get(url, {'keyword': 'Python', 'date_range': '1 тиждень'})
        response = search_articles(request)

        self.assertEqual(response.status_code, 200)

        self.assertIn('general_articles_analyze', response.data)
        self.assertIn('each_article_analyze', response.data)
