# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и
# содержание соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление
# в формат Unicode и также проверить тип и содержимое переменных.

print(f'Задание 1')
a = 'разработка'
b = 'сокет'
c = 'декоратор'

print(type(a), a)
print(type(b), b)
print(type(c), c)

print('*' * 20)


# 2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность
# кодов (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
print(f'Задание 2')
a = b'class'
b = b'function'
c = b'method'

print(type(a), a, len(a))
print(type(b), b, len(b))
print(type(c), c, len(c))

print('*' * 20)


# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

print(f'Задание 3')
a = 'attribute'
b = 'класс'
c = 'функция'
d = 'type'

a_byte = a.encode('utf-8')
b_byte = b.encode('utf-8')
c_byte = c.encode('utf-8')
d_byte = d.encode('utf-8')

print(type(a_byte), a_byte, len(a_byte))
print(type(b_byte), b_byte, len(b_byte))
print(type(c_byte), c_byte, len(c_byte))
print(type(d_byte), d_byte, len(d_byte))

print('*' * 20)


# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в
# байтовое и выполнить обратное преобразование (используя методы encode и decode).

print(f'Задание 4')

a = 'разработка'
b = 'администрирование'
c = 'protocol'
d = 'standard'

a_byte = a.encode('utf-8')
b_byte = b.encode('utf-8')
c_byte = c.encode('utf-8')
d_byte = d.encode('utf-8')

print(type(a_byte), a_byte, len(a_byte))
print(type(b_byte), b_byte, len(b_byte))
print(type(c_byte), c_byte, len(c_byte))
print(type(d_byte), d_byte, len(d_byte))

a_str = bytes.decode(a_byte, 'utf-8')
b_str = bytes.decode(b_byte, 'utf-8')
c_str = bytes.decode(c_byte, 'utf-8')
d_str = bytes.decode(d_byte, 'utf-8')

print(type(a_str), a_str, len(a_str))
print(type(b_str), b_str, len(b_str))
print(type(c_str), c_str, len(c_str))
print(type(d_str), d_str, len(d_str))

print('*' * 20)


# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип
# на кириллице.

print(f'Задание 5')

import subprocess

args =['ping', 'yandex.ru', '-c', '4']

subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)

for line in subproc_ping.stdout:
    line = line.decode('cp866').encode('utf-8')
    print(line.decode('utf-8'))

print('*' * 20)