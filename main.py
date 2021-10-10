import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_goods_description(products):
    store_goods = collections.defaultdict(list)
    for product in products.to_dict(orient='records'):
        category_name = product['Категория']
        store_goods[category_name].append(product)
    return store_goods


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    foundation_year = 1921

    products = pandas.read_excel(
        'wine.xlsx',
        usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
        na_values=['N/A', 'NA'],
        keep_default_na=False
    )
    store_goods = get_goods_description(products)

    rendered_page = template.render(
        age_winery=datetime.date.today().year - foundation_year,
        store_goods=store_goods
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
