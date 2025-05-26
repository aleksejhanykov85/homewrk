import sys
from datetime import datetime as dt
import sqlite3

connection = sqlite3.connect('warh_db.sqlite3')
cur = connection.cursor()

def get_float_value(mes):
    try:
        value = float(input(mes))
        return value
    except ValueError:
        print('Неверное значение! Значение должно быть в формате числа')
        return get_float_value(mes)
    

def get_strptime_value(mes):
    try:
        value = dt.strptime(input(mes), "%d.%m.%Y")
        if value <= dt.now():
            raise ValueError
        return value
    except ValueError:
        print("Неверное значение! формат дд.мм.гг:")
        return get_strptime_value(mes)

def get_product_name(mes):
    name_of_pr = input(mes)
    if not any(char.isalpha() for char in name_of_pr):
        get_product_name(mes)
    return name_of_pr


def check_of_product():
    product = input('Какой товар хотите добавить, непрод или прод? ').lower()
    if product == "прод" or product == "непрод":
        name_of_pr = get_product_name("Название продукта: ")
        price = get_float_value("Введите цену: ")
        amount = get_float_value("Введите количество: ")
        if product == "прод":
            srok = get_strptime_value("Введите срок годности в формате дд.мм.гг: ")

            new_prod = (srok, name_of_pr, amount, price)
        elif product == "непрод":
            garant = get_strptime_value("Введите срок гарантии в формате дд.мм.гг: ")
            new_prod = Equipment(garant, name_of_pr, amount, price)
        return new_prod
    else:
        print("Нужно выбрать 'прод' или 'непрод'")
        return check_of_product()
        

def check_request():
    try:
        request = int(input('Что вы хотите сделать? '))
        if request <= 0 or request > 8:
            raise ValueError
        return request
    except ValueError:
        print('Неверное значение! Нужно вводить цифры из списка')
        return check_request()


def check_of_warh(func):
    def wrapper():
        if current_warehouse is None:
            print("Склад еще не создан!")
            while True:
                answer = input("Хотите создать склад или выйти? ").lower()
                if answer == "создать":
                    create_new_warh()
                    func()
                    return
                elif answer == "выйти":
                    return
        else:
            func()
    return wrapper

def check_warh_prod_availability(func):
    def wrapper():
        if current_warehouse.list_of_prod == []:
            print("Этот склад еще пуст! Сначала завезите товар ")
            while True:
                answer = input("Хотите завезти? ").lower()
                if answer == "да" or answer == "yes": 
                    new_product()
                    func()
                    return
        else:
            func()
    return wrapper


current_warehouse = None
warehouses = []


def main_menu():
    print('''
        1 - Создать новый склад
        2 - Выбрать склад, с которым человек будет работать по его имени
        3 - Добавить товар на склад
        4 - Выкупить товар со склада
        5 - Посмотреть товары на складе отсортированные по общей стоимости
        6 - Проверить наличие товара на складе по его названию
        7 - Проверить срок годности/гарантию товара
        8 - Выход из программы
        ''')
    if current_warehouse:
        print(current_warehouse)
    request = check_request()
    match request:
        case 1:
            create_new_warh()
        case 2:
            switch_warh()
        case 3:
            new_product()
        case 4:
            buy_product()
        case 5:  
            sorting()
        case 6:
            check_availability()
        case 7:
            check_date()
        case 8:
            exit_from_warh()
    

def create_new_warh():
    global current_warehouse
    name = input('Введите название склада: ')
    if not any(char.isalpha() for char in name):
        create_new_warh()
        return
    cur.execute('insert into warehouses(name) values(?)',name)
    connection.commit()
    # current_warehouse = cur.execute('select id from warehouses where name=?',name)
    cur.execute('select last_insert_rowid() from warehouses')
    current_warehouse = cur.fetchone()
    

def switch_warh():
    global current_warehouse
    answer = ''
    print(f"Список складов: ")
    cur.execute('select * from warehouses where trim(`id`) = '' or `id` is null')
    check_null = cur.fetchone()[0]
    if check_null == 0:
        print("Список складов пустой")
        while True:
            answer = input("Хотите добавить склад или выйти? ").lower()
            if answer == 'добавить':
                current_warehouse = create_new_warh()
                return warehouses
            elif answer == "выйти":
                return
            else:
                print("Нет такого варианта")
    else:
        cur.execute('select id, name from warehouse')
        print(cur.fetchone())
        key = input("Введите название склада: ")
        # for i in  warehouses:
        #     if i.name == key:
        #         current_warehouse = i
        #         print(f"Текущий склад: {current_warehouse.name}")
        data = cur.execute('select id from warehouses where name=?',key).fetchone()
        if len(data) > 0:
            current_warehouse = cur.fetchone()
            return  
        print("Такого склада нет в списке")
        while True:
            answer = input("Хотите создать/переключить/выйти? ").lower()
            if answer == "создать":
                create_new_warh()
                return
            elif answer == "переключить":
                switch_warh()
                return
            elif answer == "выйти":
                return
            else:
                print("Нет такого варианта")

@check_of_warh
def new_product():
    global current_warehouse
    new_prod = check_of_product()
    for i in current_warehouse.list_of_prod:
        if type(new_prod) == type(i) and new_prod == i:
            i += new_prod
            return
    current_warehouse += new_prod


@check_of_warh
@check_warh_prod_availability
def buy_product():
    global current_warehouse
    buy = input("Что вы хотите купить? ")
    n = int(input("В каком количестве? "))
    current_warehouse.buy_prod(buy, n)


@check_of_warh
@check_warh_prod_availability
def sorting():
    print(current_warehouse.sortirovka())


@check_of_warh
@check_warh_prod_availability
def check_availability():
    current_warehouse.check()


def exit_from_warh():
    sys.exit(0)

@check_of_warh
@check_warh_prod_availability
def check_date():
    print(current_warehouse.list_of_prod)
    while True:
        item = input("Введите название продукта для проверки даты/гарантии ")
        for i in current_warehouse.list_of_prod:
            if i.name == item: 
                if isinstance(i, Food):
                    date = i.exp_date.date()
                elif isinstance(i, Equipment):
                    date = i.war.date()
                current_datetime = dt.now().date()
                print(item, date, current_datetime)
                difr = date - current_datetime
                print(f"осталось {difr.days} дней")
                return
        answer = ("Такого товар нет, хотите заказать или выйти?") 
        if answer == "заказать":
            new_product()
            check_date()
            return
        elif answer == "выйти":
            return