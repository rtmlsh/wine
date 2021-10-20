import argparse
import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_goods_description(goods_specification):
    store_goods = collections.defaultdict(list)
    for specification in goods_specification.to_dict(orient='records'):
        category_name = specification['Категория']
        store_goods[category_name].append(specification)
    return store_goods


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Скрипт запускает сайт интернет-магазина')
    parser.parse_args()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    foundation_year = 1920

    goods_specification = pandas.read_excel(
        'wine.xlsx',
        usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
        na_values=['N/A', 'NA'],
        keep_default_na=False
    )
    store_goods = get_goods_description(goods_specification)

    rendered_page = template.render(
        winery_age=datetime.date.today().year - foundation_year,
        store_goods=store_goods
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
