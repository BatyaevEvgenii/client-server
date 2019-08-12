# server
# for connection
from socket import socket

# обработка командной строки
import yaml
import json
import logging
from argparse import ArgumentParser

# из нашего модуля protocol импортируем
from protocol import validate_request, make_response

from resolvers import resolve

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
'''
if __name__ == '__main__': можем убрать после того как файл переименовали в __main__,
тем самым перевели python на модульное выполнение(директория client)
'''

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
        '''
        данные подтянем из конфига $ python server -c config.yaml,
        а если их нет - возьмем из переменных
        host = file_config.get('host', host)
        port = file_config.get('port', port)
        но можем и сделать их "глобальными" значениями по-умолчанию:
        '''
        default_config.update(file_config)

host, port = (default_config.get('host'), default_config.get('port'))

''' блок логирования '''
# logger = logging.getLogger('main')
# logger.setLevel(logging.DEBUG)
#
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#
# handler = logging.FileHandler('main.log')
# handler.setFormatter(formatter)
# handler.setLevel(logging.DEBUG)
#
# logger.addHandler(handler)
''' '''

''' упрощаем журналирование, минуя блок логирования'''
logging.basicConfig(
    level=logging.DEBUG,
    format= '%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


try:
    sock = socket()
    sock.bind((host, port))
    sock.listen(5) # слушаем 5 соединений клиентов

    ''' здесь и далее заменяем все ранее установленные print на logger.info'''
    logging.info(f'Сервер запущен... {host}:{port}')
    # print(f'Сервер запущен... {host}:{port}')

    # ожидание клиентского подключения
    while True:
        client, address = sock.accept()
        logging.info(f'Клиент подключился: {address[0]}:{address[1]}')
        # print(f'Клиент подключился: {address[0]}:{address[1]}')
        byte_request = client.recv(default_config.get('buffersize'))

        # в строку потом в словарь
        request = json.loads(byte_request.decode())

        # проходим валидацию
        if validate_request(request):
            action_name = request.get('action')
            # извлекаем контроллер
            controller = resolve(action_name)
            # if action == 'echo':
            if controller:
                try:
                    ''' фиксируем debug '''
                    logging.debug(f'Controller {action_name} resolved with request: {request}')
                    # print(f'Controller {action_name} resolved with request: {request}')

                    response = controller(request)
                except Exception as err:
                    ''' фикусируем критическую ситуацию '''
                    logging.critical(f'Controller {action_name} error: {err}')
                    # print(f'Controller {action_name} error: {err}')
                    response = make_response(request, 500, 'Internal server error')
            else:
                ''' фиксируем симантические ошибки '''
                logging.error(f'Controller {action_name} not found')
                # print(f'Controller {action_name} not found')
                response = make_response(request, 404, f'Action with name "{action_name}"   not supported')
        else:
            ''' фиксируем симантические ошибки '''
            logging.error(f'Controller wrong request: {request}')
            # print(f'Controller wrong request: {request}')
            response = make_response(request, 400, 'Wrong request format!')

        client.send(
            json.dumps(response).encode()
        )

        client.close()
        # print(f'Клиент отключился...')

    # обработаем исключение
except KeyboardInterrupt:
    logging.info('Сервер выключен.')
    # print('Сервер выключен.')




'''
python __main__.py -c config.yaml
python __main__.py --help
python client
python server -c config.yaml
fab server
fab client
fab kill
'''

