import random
import time

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from main.models import Category, Subcategory, Products

BASE_URL = r'https://www.cifrus.ru'


def get_random_user_agent():
    fake_user_agents = [
        'Opera/8.32 (Windows NT 4.0; en-US) Presto/2.12.231 Version/12.00',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/4.0)',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/5331 (KHTML, like Gecko) Chrome/36.0.893.0 Mobile Safari/5331',
        'Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X; en-US) AppleWebKit/535.39.4 (KHTML, like Gecko) Version/3.0.5 Mobile/8B119 Safari/6535.39.4',
        'Mozilla/5.0 (iPad; CPU OS 7_0_2 like Mac OS X; en-US) AppleWebKit/535.32.5 (KHTML, like Gecko) Version/4.0.5 Mobile/8B116 Safari/6535.32.5',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/5.1)',
        'Mozilla/5.0 (compatible; MSIE 11.0; Windows 98; Trident/3.0)',
        'Mozilla/5.0 (X11; Linux i686; rv:6.0) Gecko/20130821 Firefox/35.0'
    ]
    return random.choice(fake_user_agents)


def get_soup(url: str = None):
    try:
        response = requests.get(url, headers={'User-Agent': get_random_user_agent()})
        soup = BeautifulSoup(response.text, features="html.parser")
        if soup.select_one('title').text == '404 Not Found':
            raise requests.HTTPError
        return soup
    except requests.HTTPError:
        return None
    except Exception:
        time.sleep(3)
        get_soup(url)


def add_categories(url: str) -> None:
    soup = get_soup(url)
    categories = soup.select('ul.category-dropdown>li.dropdown-submenu')
    for category in categories:
        category_name = category.select_one('a.dropdown-toggle').text
        category_obj = Category(name=category_name)
        if category_obj.name not in ['Услуги', 'Платный ремонт', 'Мобильные телефоны']:
            try:
                category_obj.save()
            except:
                pass
        for subcategory in category.select('div.dropdown-menu div.dropdown-inner ul li a'):
            subcategory_obj = Subcategory(category_id=category_obj.id,
                                          name=subcategory.text,
                                          url=f"{BASE_URL}{subcategory['href']}")
            try:
                subcategory_obj.save()
            except:
                pass


def get_product_data(url: str) -> dict:
    product_data = {}
    soup = get_soup(url)
    try:
        product_data['code'] = int(soup.select_one('span.code').text)
    except:
        product_data['code'] = None

    try:
        product_data['price'] = float(soup.select_one('div.price>div.new-price').text.split()[0])
    except:
        product_data['price'] = None

    try:
        product_data['available'] = True if soup.select_one('span.instock').text == 'есть в наличии' else False
    except:
        product_data['available'] = None

    try:
        product_data['specifications'] = [specification.text for specification in soup.select('table.excel3 tbody td')]
    except:
        product_data['specifications'] = None

    try:
        product_data['img'] = BASE_URL + soup.select_one('a.highslide')['href']
    except:
        product_data['img'] = None

    return product_data


def add_subcategory_products(url: str, category: int, subcategory: int) -> None:
    counter = 1
    soup = get_soup(f'{url}/page-{counter}')
    while soup is not None:
        product_urls = soup.select('div.caption>div.name>a')
        for product_url in product_urls:
            product_data = get_product_data(url=f"{BASE_URL}{product_url['href']}")
            new_product = Products(category=category,
                                   subcategory=subcategory,
                                   code=product_data['code'],
                                   name=product_url.text,
                                   price=product_data['price'],
                                   available=product_data['available'],
                                   specifications=product_data['specifications'],
                                   img=product_data['img'])
            try:
                new_product.save()
            except:
                pass
        counter += 1
        soup = get_soup(f'{url}/page-{counter}')


def run():
    add_categories(BASE_URL)
    subcategories = Subcategory.objects.all()
    for subcategory in tqdm(subcategories):
        add_subcategory_products(url=subcategory.url,
                                 category=subcategory.category,
                                 subcategory=subcategory)


if __name__ == '__main__':
    run()
