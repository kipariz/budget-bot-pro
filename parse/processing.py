import re
from parse.schema import Table


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
            source.append('planning')
        if '+' in meta:
            source.append('incoming')
        else:
            source.append('expense')
    else:
        source.append('expense')

    return source


def parse_input(operation_data: str) -> Table:
    amount = re.findall(r'\d+', operation_data)
    name, category = re.split(r'\d+', operation_data)
    name, meta = get_meta(name)
    source = get_source(meta)

    return Table(name, category, amount, source)

