from databaseclass import Database
db = Database('Projectwarehouse.sqlite3')
from newutils import *

current_warehouse = None

def main_menu():
    global current_warehouse
    print('''
        1 - Создать новый склад
        2 - Выбрать склад, с которым человек будет работать по его имени
        3 - Добавить товар на склад
        4 - Выкупить товар со склада
        5 - Посмотреть товары на складе отсортированные по общей стоимости
        6 - Проверить наличие товара на складе по его названию
        7 - Проверить срок годности/гарантию товара
        8 - Удалить склад
        9 - Выход из программы
        ''')
    if current_warehouse:
        data = db.list_of_products(current_warehouse, 'name')
        print(*data, sep ='\n')
    request = check_request()
    match request:
        case 1:
            name = input('Введите название склада: ').strip()
            new_warehouse = db.create_warehouse(name)
            if new_warehouse:
                print('Склад создан! \n')
                current_warehouse = new_warehouse
            else:
                print('Не удалось создать склад')
        case 2:
            print(*db.list_of_warehouses(), sep = '\n')
            name = input('Введите название склада: ').strip()
            new_warehouse = db.current_warehouse(name)
            if new_warehouse:
                print('Склад изменен! \n')
                current_warehouse = new_warehouse
            else:
                print('Не удалось поменять склад')
        case 3:
            name_of_product = input("Введите название продукта: ")
            amount = get_float_value("Сколько товара вы хотите заказать: ")
            price = get_float_value("Какая цена товара: ")
            type = chek_type_product("прод или непрод: ")
            date = check_date("Какой срок годности формат(гггг-мм-дд): ")
            db.add_product(name_of_product, amount, price, type, date, current_warehouse)    
        case 4:
            id = get_float_value('Введите id продукта: ')
            amount = get_float_value('Введите количество, которое хотите купить: ')
            db.delete_product(amount,id)
        case 5:  
            data = db.list_of_products(current_warehouse, 'price')
            print(*data)
        case 6:
            info_id = get_float_value('Введите id для получения информации о продукте: ')
            info = db.get_info_product(info_id)
            print(*info)
        case 7:
            prod_id = get_float_value('Введите id продукта: ')
            check_guarantee = db.check_date_of_product(prod_id)
            print(check_guarantee, 'дней')
        case 8:
            name = input('Введите названия склад, который хотите удалить: ')
            db.delete_warehouse(name)
        case 9:
            exit()
