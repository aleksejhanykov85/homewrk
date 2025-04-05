# Импорты
from utils import Warehouse, Food, Equipment


def main():
    warehouses = []
    current_warehouse = None
    # current_warehouse.asingment_wareh()
    # warehouses.name_of_wareh.append(current_warehouse.name)
    while True:
        if current_warehouse:
            print(current_warehouse)
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
                current_warehouse = Warehouse(input("Введите название склада:"), [])
                warehouses.append(current_warehouse.name)
                # Warehouse.data([])
                

            case 2:
                print(f"Список складов: \n{warehouses}")
                current_warehouse = warehouses[warehouses.index(input())]
                print(f"Текущий склад: {current_warehouse}")
            case 3:
                product = input('Кого хотите добавить, непродовольственный или продукт?')
                name_of_pr = input("Название продукта: ")
                price = float(input("Какая цена?: "))
                amount = float(input("В каком количестве?: "))
                if product == "прод":
                    srok = int(input("Какой срок годности?"))
                    new_prod = Food(srok, name_of_pr, amount, price)
                else:
                    garant = int(input("Какой срок гарантии?"))
                    new_prod = Equipment(garant, name_of_pr, amount, price)
                current_warehouse += new_prod
                # print(new_prod)
                # print(repr(new_prod))
            case 4:
                buy = input("Что вы хотите купить?")
                n = int(input("В каком количестве?"))
                current_warehouse.buy_prod(buy, n)
            case 5:  
                print(current_warehouse.sortirovka())
            case 6:
                current_warehouse.check()

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


