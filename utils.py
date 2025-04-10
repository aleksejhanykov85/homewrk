# warehouses = []
current_warehouse = None
dict_warehouses = {}


def info():
    print('''
        1 - Создать новый склад
        2 - Выбрать склад, с которым человек будет работать по его имени
        3 - Добавить товар на склад
        4 - Выкупить товар со склада
        5 - Посмотреть товары на складе отсортированные по общей стоимости
        6 - Проверить наличие товара на складе по его названию
        ''')
    if current_warehouse:
        print(current_warehouse)
    request = int(input('Что вы хотите сделать? '))
    match request:
        case 1:
            case1()
        case 2:
            case2()
        case 3:
            case3()
        case 4:
            case4()
        case 5:  
            case5()
        case 6:
            case6()


def case1():
    global current_warehouse, dict_warehouses
    name = input('Введите название склада: ')
    initial_data = []
    current_warehouse = Warehouse(name, initial_data)
    # warehouses.append(current_warehouse)
    dict_warehouses[current_warehouse.name] = initial_data
    

def case2():
    global current_warehouse
    print(f"Список складов: \n{dict_warehouses}")
    key = input("Введите название склада: ")
    current_warehouse = Warehouse(key, dict_warehouses[key])
    print(f"Текущий склад: {current_warehouse.name}")
    # for i in warehouses:
    #     print(i.name)
    # print(dict_warehouses)
    

def case3():
    global current_warehouse
    product = input('Кого хотите добавить, непродовольственный или продукт? ')
    name_of_pr = input("Название продукта: ")
    price = float(input("Какая цена?: "))
    amount = float(input("В каком количестве? "))
    if product == "прод":
        srok = int(input("Какой срок годности? "))
        new_prod = Food(srok, name_of_pr, amount, price)
    else:
        garant = int(input("Какой срок гарантии? "))
        new_prod = Equipment(garant, name_of_pr, amount, price)
    current_warehouse += new_prod


def case4():
    global current_warehouse
    buy = input("Что вы хотите купить? ")
    n = int(input("В каком количестве? "))
    current_warehouse.buy_prod(buy, n)


def case5():
    print(current_warehouse.sortirovka())


def case6():
    current_warehouse.check()


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
        return f'Название: {self.name} \nСписок товаров({self.list_of_prod})'
    
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


class Product:
    def __init__(self, name, quant, price=0):
        self.name = name
        self.price = price
        self.quant = quant

    def __iadd__(self, quant): 
        self.quant += quant
        return self

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

    # def __repr__(self):
    #    return f'Product("{self.name}", {self.quant}, {self.price})'
    

class Food(Product):
    def __init__(self, exp_date, name, quant, price=0):
        super().__init__(name, quant, price)
        self.exp_date = exp_date


class Equipment(Product):
    def __init__(self, war, name, quant, price=0):
        super().__init__(name, quant, price)
        self.war = war
