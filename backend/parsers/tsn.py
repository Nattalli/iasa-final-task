from datetime import datetime

import requests
from parsers.utils import calculate_date
from bs4 import BeautifulSoup


def parse_tsn_search_results(keyword, date_range):
    today = datetime.now().date()
    last_date = calculate_date(today, date_range)

    url = f"https://tsn.ua/search?query={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('article', class_='c-card')
        articles = []
        for result in search_results:
            title = result.find('h3', class_='c-card__title').text.strip()
            link = result.find('a', class_='c-card__link')['href']
            date_published = result.find('time')['datetime']
            date_published = datetime.strptime(date_published, '%Y-%m-%dT%H:%M:%S%z').date()

            if today >= date_published >= last_date:
                views = result.find('dd', class_='c-bar__label i-before i-before--spacer-r-sm i-views').text.strip()
                article = {
                    'source': {'id': None, 'name': 'https://tsn.ua/'},
                    'author': None,
                    'title': title,
                    'description': None,
                    'url': link,
                    'urlToImage': None,
                    'publishedAt': date_published.strftime('%Y-%m-%d %H:%M:%S'),
                    'content': None,
                    'views': views
                }
                articles.append(article)
        return articles
    else:
        return []
