import requests
from bs4 import BeautifulSoup
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/109.0.0.0 Safari/537.36'}

all_titles = []
all_articles = []
all_prices = []
all_memory_sizes = []
url = 'https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/?filter%2Fastana-is-v_nalichii-or-ojidaem-or-dostavim%2Fapply%2F=&PAGEN_1='

# get pages count
response = requests.get(url, timeout=10, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
pagination_row = soup.find('div', class_='bx-pagination-container row')
pages_count = int(pagination_row.find('ul').find_all('li')[5].text)


for page_num in range(1, pages_count):
    response = requests.get(url + str(page_num), headers=headers, timeout=10)
    print('page: ', page_num, 'http_status_code: ', response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')

    titles = []
    titles_divs = soup.find_all('div', class_='bx_catalog_item_title')
    for titles_div in titles_divs:
        titles.append(titles_div.text)

    titles = [item.replace('Смартфон ', '') for item in titles]
    for i in range(len(titles)):
        titles[i] = titles[i].title().strip()
    all_titles.extend(titles)

    articles = []
    articles_divs = soup.find_all('div', class_='bx_catalog_item_XML_articul')
    for articles_div in articles_divs:
        draft_articles = articles_div.text.strip()
        article = ''
        for item in draft_articles:
            if item.isdigit():
                article += item
        articles.append(article)
    all_articles.extend(articles)

    prices = []
    prices_divs = soup.find_all('div', class_='bx-more-prices')
    for prices_div in prices_divs:
        prices_list = prices_div.find('ul').find_all('li')
        draft_price = prices_list[2].find('span', class_='bx-more-price-text').text
        price = ''
        for item in draft_price:
            if item.isdigit():
                price += item
        prices.append(price)
    all_prices.extend(prices)

    memory_sizes = []
    for title in titles:
        splitted_title = title.split(',')
        memory_sizes.append(splitted_title[-2])
    all_memory_sizes.extend(memory_sizes)

tuples_list = zip(all_titles, all_articles, all_prices, all_memory_sizes)

json_format = [{'name': titles, 'articul': articles, 'price': prices, 'memory_size': memory_sizes} for (titles, articles, prices, memory_sizes) in tuples_list]

with open('smartphones.json', 'w') as file:
    json.dump(json_format, file, indent=2)
