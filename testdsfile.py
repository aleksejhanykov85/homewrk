import sys
from datetime import datetime as dt

def get_float_value(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print('Неверное значение! Значение должно быть в формате числа')

def get_strptime_value(message):
    while True:
        try:
            value = dt.strptime(input(message), "%d.%m.%Y")
            if value <= dt.now():
                raise ValueError
            return value
        except ValueError:
            print("Неверное значение! формат дд.мм.гг:")

def get_product_name(message):
    while True:
        name = input(message)
        if any(char.isalpha() for char in name):
            return name
        print("Название продукта должно содержать хотя бы одну букву.")

def check_product_type():
    while True:
        product_type = input('Какой товар хотите добавить, непрод или прод? ').lower()
        if product_type in {"прод", "непрод"}:
            return product_type
        print("Нужно выбрать 'прод' или 'непрод'")

def check_of_product():
    product_type = check_product_type()
    name_of_pr = get_product_name("Название продукта: ")
    price = get_float_value("Введите цену: ")
    amount = get_float_value("Введите количество: ")
    
    if product_type == "прод":
        srok = get_strptime_value("Введите срок годности в формате дд.мм.гг: ")
        return Food(srok, name_of_pr, amount, price)
    else:
        garant = get_strptime_value("Введите срок гарантии в формате дд.мм.гг: ")
        return Equipment(garant, name_of_pr, amount, price)

def check_request():
    while True:
        try:
            request = int(input('Что вы хотите сделать? '))
            if 0 < request <= 8:
                return request
            raise ValueError
        except ValueError:
            print('Неверное значение! Нужно вводить цифры из списка')

def warehouse_check(func):
    def wrapper():
        if current_warehouse is None:
            print("Склад еще не создан!")
            while True:
                answer = input("Хотите создать склад или выйти? ").lower()
                if answer in {"создать", "сотворить"}:
                    create_new_warh()
                    func()
                    return
                elif answer in {"выйти", "выход"}:
                    return
        else:
            func()
    return wrapper

def product_availability_check(func):
    def wrapper():
        if not current_warehouse:
            print("Этот склад еще пуст! Сначала завезите товар.")
            while True:
                answer = input("Хотите завезти? ").lower()
                if answer in {"да", "yes"}: 
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
    while True:
        name = input('Введите название склада: ').strip()
        if name:
            break
        print("Название должно содержать хотя бы одну букву.")
        
    new_warehouse = Warehouse(name, [])
    warehouses.append(new_warehouse)

def switch_warh():
    global current_warehouse
    name = input('Введите название склада для переключения: ')
    for warehouse in warehouses:
        if warehouse.name == name:
            current_warehouse = warehouse
            print(f'Склад переключён на: {current_warehouse}')
            return
    print("Такой склад не найден.")

@warehouse_check
def new_product():
    global current_warehouse
    new_prod = check_of_product()
    for i in current_warehouse.list_of_prod:
        if type(new_prod) == type(i) and new_prod == i:
            i += new_prod
            return
    current_warehouse += new_prod


@warehouse_check
@product_availability_check
def buy_product():
    global current_warehouse
    buy = input("Что вы хотите купить? ")
    n = int(input("В каком количестве? "))
    current_warehouse.buy_prod(buy, n)


@warehouse_check
@product_availability_check
def sorting():
    print(current_warehouse.sortirovka())


@warehouse_check
@product_availability_check
def check_availability():
    current_warehouse.check()


def exit_from_warh():
    sys.exit(0)

@warehouse_check
@product_availability_check
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
    

class Warehouse:

    def __init__(self, name, initial_data):                                     
        self.name = name
        self.list_of_prod = initial_data  

    def __getitem__(self, index):
        return self.list_of_prod[index]
    
    def __setitem__(self, index, value):
        self.list_of_prod[index] = value

    def __iadd__(self, item):
        self.list_of_prod.append(item)
        return self

    def __str__(self):
        return f'Название: {self.name}, Список товаров({self.list_of_prod})'

    def __contains__(self, item):
        return item in self.list_of_prod

    def buy_prod(self, name, quant):
        for i in self.list_of_prod:
            if i.name == name:
                try:
                    i -= quant
                except:
                    print("Товвара меньше, чем вы хотите купить")

    def sortirovka(self):
        return sorted(self.list_of_prod)
    
    def __contains__(self, item):
        return item in self.list_of_prod

    def check(self):
        item = input("Введите товар на проверку наличия:")
        if item in self.list_of_prod:
            print("Такой товар имеется в наличии")
        else:
            print("Такого товар нет, хотите заказать?") 


class Product():
    def __init__(self, name, quant, price=0):
        self.name = name
        self.price = price
        self.quant = quant

    def __isub__(self, quant):
        if self.quant < quant:
            raise ValueError("Недостаточно товара")
        else:
            self.quant -= quant
            return self

    def __lt__(self, other):
        return self.price < other.price
    
    def __repr__(self):
        return f'{self.name} ({self.quant}) ({self.price})'
    

class Food(Product):
    def __init__(self, exp_date, name, quant, price=0):
        super().__init__(name, quant, price)
        self.exp_date = exp_date

    def __iadd__(self, other): 
        if self.name == other.name and self.price == other.price and self.exp_date == other.exp_date:
            self.quant += other.quant
            return self
        
    def __eq__(self,other):
        return self.name == other.name and self.price == other.price and self.exp_date == other.exp_date
        

class Equipment(Product):
    def __init__(self, war, name, quant, price=0):
        super().__init__(name, quant, price)
        self.war = war

    def __iadd__(self, other): 
        if self.name == other.name and self.price == other.price and self.war == other.war:
            self.quant += other.quant
            return self
        
    def __eq__(self,other):
        return self.name == other.name and self.price == other.price and self.war == other.war
