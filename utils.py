import sys
# from abc import ABC, abstractmethod


def get_float_value(mes):
    try:
        value = float(input(mes))
        return value
    except ValueError:
        print('Неверное значение! Значение должно быть в формате числа')
        return get_float_value(mes)


def get_product_name():
    name_of_pr = input("Название продукта: ")
    
    if not name_of_pr.isalpha():
        print("Введите название продукта")
        get_product_name()
    return name_of_pr


def check_of_product():
    product = input('Какой товар хотите добавить, непрод или прод? ').lower()
    if product == "прод" or product == "непрод":
        name_of_pr = get_product_name()
        price = get_float_value("Введите цену: ")
        amount = get_float_value("Введите количество: ")
        
        if product == "прод":
            srok = get_float_value("Введите срок годности: ")
            new_prod = Food(srok, name_of_pr, amount, price)
        elif product == "непрод":
            garant = get_float_value("Введите гарантию: ")
            new_prod = Equipment(garant, name_of_pr, amount, price)
        return new_prod
    else:
        print("Нужно выбрать 'прод' или 'непрод'")
        return check_of_product()
        

def check_request():
    try:
        request = int(input('Что вы хотите сделать? '))
        if request <= 0 or request > 7:
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
                answer = input("Хотите создать склад или выйти?").lower()
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
            answer = input("Хотите завезти? ").lower()
            if answer == "да" or answer == "yes": 
                new_product()
                return
            else:
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
        7 - Выход из программы
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
            exit_from_warh()


def create_new_warh():
    global current_warehouse
    name = input('Введите название склада: ')
    initial_data = []
    current_warehouse = Warehouse(name, initial_data)
    warehouses.append(current_warehouse)
    

def switch_warh():
    global current_warehouse
    answer = ''
    print(f"Список складов: ")
    if warehouses == []:
        print("Список складов пустой")
        while True:
            answer = input("Хотите добавить склад или выйти? ").lower()
            if answer == 'добавить':
                create_new_warh()
                return
            elif answer == "выйти":
                return
            else:
                print("Нет такого варианта")
    else:
        print(*warehouses, sep='\n')
        key = input("Введите название склада: ")
        for i in  warehouses:
            if i.name == key:
                current_warehouse = i
                print(f"Текущий склад: {current_warehouse.name}")
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


class Warehouse:

    def __init__(self, name, initial_data):                                     
        self.name = name
        self.list_of_prod = initial_data  

    # def __iadd__(self, warehouses, current_warehouse):
    #     warehouses.append(current_warehouse.name)

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

    def __iadd__(self, other): 
        if self.name == other.name:
            self.quant += other.quant
            return self.quant

    def __isub__(self, quant):
        if self.quant < quant:
            raise ValueError("Недостаточно товара")
        else:
            self.quant -= quant
            return self

    def __lt__(self, other):
        return self.price < other.price
    
    def __repr__(self):
        return f'{self.name} ({self.quant})'
    

class Food(Product):
    def __init__(self, exp_date, name, quant, price=0):
        super().__init__(name, quant, price)
        self.exp_date = exp_date


class Equipment(Product):
    def __init__(self, war, name, quant, price=0):
        super().__init__(name, quant, price)
        self.war = war


# class Product(ABC):
#     def __init__(self, name, quant, price=0):
#         self.name = name
#         self.price = price
#         self.quant = quant

#     @abstractmethod
#     def __iadd__(self, quant): 
#         pass

#     @abstractmethod
#     def __isub__(self, quant):
#         pass

#     @abstractmethod
#     def __lt__(self, other):
#         pass
    
#     @abstractmethod
#     def __repr__(self):
#         pass
    
# class Food(Product):
#     def __init__(self, exp_date, name, quant, price=0):
#         super().__init__(name, quant, price)
#         self.exp_date = exp_date

#     def __iadd__(self, quant): 
#         self.quant += quant
#         return self

#     def __isub__(self, quant):
#         if self.quant < quant:
#             raise ValueError("Недостаточно товара")
#         else:
#             self.quant -= quant
#             return self

#     def __lt__(self, other):
#         return self.price < other.price
    
#     def __repr__(self):
#         return f'{self.name} ({self.quant})'

# class Equipment(Product):
#     def __init__(self, war, name, quant, price=0):
#         super().__init__(name, quant, price)
#         self.war = war
    
#     def __iadd__(self, quant): 
#         self.quant += quant
#         return self

#     def __isub__(self, quant):
#         if self.quant < quant:
#             raise ValueError("Недостаточно товара")
#         else:
#             self.quant -= quant
#             return self

#     def __lt__(self, other):
#         return self.price < other.price
    
#     def __repr__(self):
#         return f'{self.name} ({self.quant})'
