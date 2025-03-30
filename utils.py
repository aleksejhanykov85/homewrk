class Warehouse:
    def __init__(self, name, list_of_prod):
        self.name = name
        self.list_of_prod = list_of_prod   

    @property
    def __add__(self, other):
        if isinstance(other, Product):
            return self.list_of_prod.append(other.name)
        
    # def __check__(self,other):
    #     if isinstance(other, Product):
    #         if other.quant > 0:
    #             return True
    #         else:
    #             return False       

    def __getitem__(self, other):
        if isinstance(other,) 

class Product:
    def __init__(self, name, price, quant): #def __init__(self, name, price, unit_of_wei, quant):
        self.name = name
        self.price = price
        self.quant = quant

    def __le__(self,other):
        return self.price < other.price
    
    @property
    def __iadd__(self,other): 
        self.quant += other.quant

    # def __bool__(self):

     
        

class Food(Product):
    def __init__(self, exp_date):
        self.exp_date = exp_date

class Equipment(Product):
    def __init__(self, war):
        self.war = war
