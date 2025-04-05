from dataclasses import dataclass


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
        item = input("Введите товар на проверку наличия: ")
        if item in self.list_of_prod:
            print("Такой товар имеется в наличии")
        else:
            print("Такого товар нет, хотите заказать?") 
            # ans = input()
            # if ans == '':


# class current_warehouse(Warehouse):

#     def __init__(self, cur_wareh, name):
#         super().__init__(name)
#         self.current_warehouse = cur_wareh
    
#     def asingment_wareh(self):
#         self.current_warehouse = Warehouse(input("Введите название склада:"), [])
#         return self.current_warehouse

# @dataclass
# class warehouses:
#     name_of_wareh : current_warehouse.name

#     def __iadd__(self, other_wareh):
#         self.name_of_wareh.append(other_wareh.name)


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

    def __lt__(self,other):
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
