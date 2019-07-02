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

# if __name__ == '__main__': можем убрать после того как файл переименовали в __main__
parser.parse_args()








# (venv) 192-168-1-103:3 marat$ python client.py -c config.yml
# (venv) 192-168-1-103:3 marat$ python client.py --help
# (venv) 192-168-1-103:3 marat$ python client
# /Users/marat/venv/bin/python: can't find '__main__' module in 'client'
