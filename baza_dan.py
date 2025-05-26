import sqlite3
connection = sqlite3.connect('warh_db.sqlite3')
cur = connection.cursor()
cur.execute('create table warehouses(id integer primary key autoincrement, name)')
cur.execute('create table products(id integer primary key autoincrement, name varchar(20), amount, price, type, date, warehouse_id integer, foreign key (warehouse_id) references warehouses(id))')
connection.commit()