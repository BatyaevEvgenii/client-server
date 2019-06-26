# для определения кодировки
import chardet

import csv
from glob import glob
from datetime import date
import datetime

import json
from pathlib import Path

import yaml

headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
out_file = 'db/main_data.csv'


def get_data():

    for file_i in glob('db/info_*.txt'):
        rawdata = open(file_i, 'rb').read()
        result = chardet.detect(rawdata)
        charenc = result['encoding']

        with open(file_i, encoding=charenc) as infile, open(out_file, 'a') as outfile:
            reader = csv.reader(infile, delimiter=':')

            matching = [row for row in reader if any(subrow in row for subrow in headers)]
            my_dict = dict(matching)

            writer = csv.DictWriter(outfile, fieldnames=headers, quoting=csv.QUOTE_NONNUMERIC)

            # добавление заголовка один раз
            if outfile.tell() == 0:
                writer.writeheader()

            writer.writerow(my_dict)


def write_order_to_json():
    item = input('Товар: ')
    quantity = int(input('Количество: '))
    price = float(input('Цена: '))
    buyer = input('Покупатель: ')

    date_entry = input('Введите дату в формате YYYY-MM-DD: ')
    year, month, day = map(int, date_entry.split('-'))
    date1 = datetime.date(year, month, day)
    my_date = date1.strftime('%Y-%m-%d')

    path = Path('db/orders.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    data['orders'].append({'item':item, 'quantity':quantity, 'price':price, 'buyer':buyer, 'date':my_date})
    path.write_text(json.dumps(data, indent=4), encoding='utf-8')




def get_yaml():
    array_yaml = {
        'dict': {'a': 1, 'b': 2, 'c': 3},
        'int': 123,
        'list': ['a', 'b', 'c']
    }




get_data()
write_order_to_json()




