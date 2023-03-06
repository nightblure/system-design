"""
URL-SHORTENER

Допустим, что имеются следующие исходные данные:
    * генерируется 100M url-адресов в день
    * операций чтения в 10 раз больше 
    * сервис должен работать не менее 10 лет
    * сокращаемый url в среднем имеет длину 100 символов
    * допустимые символы для короткой ссылки: [0-9, A-Z, a-z]

Необходимо реализовать сократитель ссылок с как можно меньшей длиной выходной ссылки

Анализ исходных данных:
    * 1160 операций записи в секунду и 11600 RPS операций чтения
    * объемы данных: 10 лет * 365 дней * 100M ссылок в день = 365 миллиардов записей в БД

Решение:
    1. длина алфавита равна 25 букв англ. алфавита * 2 + 10 цифр = 62 символа

    2. наименьшая необходимая длина ссылки = 7 символов, 
        т.к. 62^7 = 3,5 триллиона уникальных ссылок (62^6 будет меньше 365 миллиардов)

    3. каждый символ для короткой ссылки будет взят как 
        символ алфавита с индексом равным остатку от деления первичного ключа на длину алфавита
        первичный ключ это простое инкрементируемое значение в БД
    
"""

NUMS = '0123456789'
ENG_SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABET = NUMS + ENG_SYMBOLS.lower() + ENG_SYMBOLS

ALPHABET_LENGTH = len(ALPHABET)
BASE_URL = 'https://tinyurl.com/'

def get_short_url(pk):
    from collections import deque
    encode_value = deque()

    while pk >= 1:
        remainder = pk % ALPHABET_LENGTH
        encode_value.appendleft(ALPHABET[remainder])
        pk //= ALPHABET_LENGTH

    short_url = ''.join(x for x in encode_value)
    return f'{BASE_URL}{short_url}'

tests_data = {
    11157: '2TX',
    2009215674938: 'zn9edcu'
}

for pk in tests_data:
    assert get_short_url(pk) == f'{BASE_URL}{tests_data[pk]}'