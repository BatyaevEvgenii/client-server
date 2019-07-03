# for connection
from socket import socket

# обработка командной строки
import yaml
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
default_config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}
# host = 'localhost'
# port = 8000

# если в args попал конфиг, то...
if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        # данные подтянем из конфига $ python server -c config.yaml,
        # а если их нет - возьмем из переменных
        # host = file_config.get('host', host)
        # port = file_config.get('port', port)
        # но можем и сделать их "глобальными" значениями по-умолчанию:
        default_config.update(file_config)

host, port = (default_config.get('host'), default_config.get('port'))


try:
    sock = socket()
    sock.bind((default_config.get('host'), default_config.get('port')))
    sock.listen(5) # слушаем 5 соединений клиентов

    print(f'Сервер запущен... {host}:{port}')

    # ожидание клиентского подключения
    while True:
        client, address = sock.accept()
        print(f'Клиент подключился: {address[0]}:{address[1]}')
        byte_request = client.recv(default_config.get('buffersize'))
        print(f'Клиент послал сообщение: {byte_request.decode()}')
        client.send(byte_request)
        client.close()

    # обработаем исключение
except KeyboardInterrupt:
    print('Сервер выключен.')




# python __main__.py -c config.yaml
# python __main__.py --help
# python client
# python server -c config.yaml