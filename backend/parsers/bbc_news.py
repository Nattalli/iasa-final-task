from datetime import datetime

import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

from parsers.utils import calculate_date


def parse_bbc_news(keyword, date_range):
    today = datetime.now().date()
    last_date = calculate_date(today, date_range)

    url = f"https://www.bbc.co.uk/search?q={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('div', class_='ssrcss-d9gbsd-Promo e1vyq2e80')
        articles = []
        for result in search_results:
            title_element = result.find('p', class_='ssrcss-6arcww-PromoHeadline exn3ah96')
            title = title_element.text.strip() if title_element else None

            link_element = result.find('a', class_='ssrcss-its5xf-PromoLink exn3ah91')
            link = link_element['href'] if link_element else None

            date_published_element = result.find('span', class_='ssrcss-1pvwv4b-MetadataSnippet e4wm5bw3').find('span',
                                                                                                                class_='ssrcss-1if1g9v-MetadataText e4wm5bw1')
            date_published_text = date_published_element.text.strip() if date_published_element else None

            if 'days ago' in date_published_text:
                days_ago = int(date_published_text.split()[0])
                date_published = today - relativedelta(days=days_ago)
            else:
                if len(date_published_text.split()) == 3:
                    date_published_format = '%d %B %Y'
                else:
                    date_published_format = '%d %B'
                date_published = datetime.strptime(date_published_text, date_published_format).date().replace(
                    year=datetime.now().year)

            if today >= date_published >= last_date:
                article = {
                    'source': {'id': None, 'name': 'BBC News'},
                    'author': None,
                    'title': title,
                    'description': None,
                    'url': link,
                    'urlToImage': None,
                    'publishedAt': date_published.strftime('%Y-%m-%d %H:%M:%S'),
                    'content': None,
                }
                articles.append(article)
        return articles
    else:
        return []
