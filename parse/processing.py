import re


def get_meta(merged: str):
    """
    get meta info about operation (+ for income, ? for planning operation)
    """
    index = 1
    if '?' in merged and '+' in merged:
        index = 2

    meta = merged[-index:]
    name = merged[0:-index]

    return name, meta.replace(" ", "")


def get_source(meta: str):
    source = []

    if meta:
        if '?' in meta:
            source.append('planning ?')
        if '+' in meta:
            source.append('incoming +')
        else:
            source.append('expense -')
    else:
        source.append('expense -')

    return source


def parse_input(operation_data: str):
    number = re.findall(r'\d+', operation_data)
    name, cat = re.split(r'\d+', operation_data)
    name, meta = get_meta(name)
    source = get_source(meta)

    print()

"""
readme
формат:
название сумма катгория (optional)
нельзя использовать цифры в названии категории
+ для дохода
? планирую

TODO:
статистика по категориям (таблица)
логирование (планирумое vs реальное)
"""

if __name__ == '__main__':
    # parse_input("мак 100 eat outside")
    # parse_input("зарплата сохнут +1000 зарплата")
    # parse_input("hp ?+2000 зарплата")
    # parse_input("hp +?2000 зарплата")
    parse_input("зубы ?1000 здоровье")

