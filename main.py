# Импорты
from utils import Warehouse, Product, Food, Equipment


def main():
    warehouses = []
    current_warehouse = None
    products = {}
    while True:
        request = int(input('Что вы хотите сделать?'))
        '''
        1 - Создать новый склад
        2 - Выбрать склад, с которым человек будет работать по его имени
        3 - Добавить товар на склад
        4 - Выкупить товар со склада
        5 - Посмотреть товары на складе отсортированные по общей стоимости
        6 - Проверить наличие товара на складе по его названию
        '''
        match request:
            case 1:
                current_warehouse = Warehouse(input(), [input().split(',')])
                warehouses.append(current_warehouse.name)
            case 2:
                current_warehouse = warehouses[warehouses.index(input())]
            case 3:
                product = input('Кого хотите добавить, непродовольственный или продукт?')
                name_of_pr = input()
                price = float(input())
                amount = float(input())
                if product == "прод":
                    srok = int(input())
                    new_prod = Food(Product(name_of_pr, price, amount), srok)
                else:
                    garant = int(input())
                    new_prod = Equipment(Product(name_of_pr, price, amount), garant)
                products[name_of_pr] = amount
                
            # case 4:
            # case 5:
                
                
                
        '''
        if request == '3':
            product = input('Кого хотите добавить, непродовольственный или продукт?')
            name = input как будет называться
            price = input какая стоимость
            amount = input в каком количестве
            если продукт то спросить про срок годности
            если непрод то спросить про срок гарантии
            добавить товар на склад
        '''
            
        

if __name__ == '__main__':
    main()


