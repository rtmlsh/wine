import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def read_excel():
    products = pandas.read_excel(
        'wine.xlsx',
        usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
        na_values=['N/A', 'NA'],
        keep_default_na=False
    )
    return products


def get_goods_description(products):
    store_goods = collections.defaultdict(list)
    for product in products.to_dict(orient='records'):
        title = product['Категория']
        store_goods[title].append(product)
    return store_goods


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    products = read_excel()
    store_goods = get_goods_description(products)

    rendered_page = template.render(
        age_winery=datetime.date.today().year - 1921,
        store_goods=store_goods
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
