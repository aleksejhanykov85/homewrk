from datetime import datetime as dt

def get_float_value(mes):
    try:
        value = float(input(mes))
        return value
    except ValueError:
        print('Неверное значение! Значение должно быть в формате числа')
        return get_float_value(mes)


def check_request():
    try:
        request = get_float_value('Что вы хотите сделать? ')
        if request <= 0 or request > 9:
            raise ValueError
        return request
    except ValueError:
        print('Неверное значение! Нужно вводить цифры из списка')
        return check_request()


def check_date(mes):
    try:
        value = dt.strptime(input(mes), "%Y-%m-%d")
        if value <= dt.now():
            raise ValueError
        return value
    except ValueError:
        print("Неверное формат!")
        return check_date(mes)


def chek_type_product(mes):
    prod_type = input(mes).lower()
    if prod_type not in ['прод','непрод']:
        print("Неверный ввод")
        return chek_type_product(mes)
    return prod_type

def get_float_input(mes):
    try:
        value = float(input(mes))
        return value
    except ValueError:
        print('Неверное значение! Значение должно быть в формате числа')
        return get_float_input(mes)

def get_int_input(mes):
    try:
        value = int(input(mes))
        return value
    except ValueError:
        print('Неверное значение! Значение должно быть целым числом')
        return get_int_input(mes)