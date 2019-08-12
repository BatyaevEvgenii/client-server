# client
# обработка командной строки
import yaml
import json
import hashlib
from datetime import datetime
from socket import socket
from argparse import ArgumentParser

# конструктор объекта
parser = ArgumentParser()

# конфигурируем
parser.add_argument(
    # внутри описание того что будем парсить
    # shortcut, имя конфигурационного файла, тип аргумента
    '-c', '--config', type=str,
    # аргумент опционален(запуск со стандартными настройками), за что отвечает(help text)
    required=False, help='установки пути конфига'
)

# if __name__ == '__main__': можем убрать после того как файл переименовали в __main__,
# тем самым перевели python на модульное выполнение(директория client)
args = parser.parse_args()

# значение по умолчанию
# host = 'localhost'
# port = 8000
default_config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}

# если в args попал конфиг, то...
if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        # данные подтянем из конфига $ python client -c config.yaml,
        # а если их нет - возьмем из переменных
        # host = file_config.get('host', host)
        # port = file_config.get('port', port)
        # но можем и сделать их "глобальными" значениями по-умолчанию:
        default_config.update(file_config)

sock = socket()
sock.connect(
    (default_config.get('host'), default_config.get('port'))
)

print(f'Клиент запущен... ')

# генерация хэша

hash_obj = hashlib.sha256()
hash_obj.update(
    str(datetime.now().timestamp()).encode()
)

action = input('Введите действие: ')
data = input('Введите данные: ')

# запрос клиента
# сгенерирует токен на основе timestamp
request = {
    'action': action,
    # timestamp поможет нам с отображением даты в дальнейшем
    'time': datetime.now().timestamp(),
    'data': data,
    'token': hash_obj.hexdigest()

}

# строковое представление запроса
string_request = json.dumps(request)


# формируем байтовую последовательность
sock.send(string_request.encode())
print(f'Клиент отправил данные: {data}')
byte_response = sock.recv(default_config.get('buffersize'))
print(f'{byte_response.decode()}')



'''
python __main__.py -c config.yaml
python __main__.py --help
python client
python client -c config.yaml
'''
