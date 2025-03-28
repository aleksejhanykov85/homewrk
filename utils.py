class Warehouse:
    def __init__(self, name, list_of_prod):
        self.name = name
        self.list_of_prod = list_of_prod        


class Product:
    def __init__(self, name, price, quant): #def __init__(self, name, price, unit_of_wei, quant):
        self.name = name
        self.price = price
        self.quant = quant


class Food(Product):
    def __init__(self, exp_date):
        self.exp_date = exp_date
    
    


class Equipment(Product):
    def __init__(self, war):
        self.war = war
