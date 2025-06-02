import sqlite3
import datetime as dt

class Database():
    def __init__(self,name):
        self.connection = sqlite3.connect(name)
        self.create_tables()

    def create_tables(self):
        cur = self.connection.cursor()
        cur.execute("""create table if not exists warehouses
                    (id integer primary key autoincrement, name)
                    """)
        cur.execute('''create table if not exists products
        (
                    id integer primary key autoincrement, 
                    name varchar(20),
                    amount float, price float, type varchar(7) , 
                    date date, 
                    warehouse_id integer, 
                    foreign key (warehouse_id) references warehouses(id))''')
        self.connection.commit()

    def add_product(self,name, amount, price, type, date, warehouse_id):
        cur = self.connection.cursor()
        cur.execute('select id from products where name = ? and price = ? and type = ? and date = ? and warehouse_id = ?',[name,price,type,date,warehouse_id])
        data = cur.fetchone()
        if not data:
            cur.execute('''insert into products(
                        name,amount,price,type,date,warehouse_id)
                        values(?,?,?,?,?,?)
                        ''',[name,amount,price,type,date,warehouse_id])
        else:
            cur.execute('''update products
                        set(amount = amount+?)
                        where id = ?
            ''',[amount, data[0]])
        self.connection.commit()

    def delete_product(self, amount, id):
        cur = self.connection.cursor()
        cur.execute('select amount from products where id = ?', [id])
        last_amount = cur.fetchone()[0]
        if last_amount == amount:
            cur.execute('delete from products where id = ?',[id])
        else:
            cur.execute('update products set(amount = amount-?) where id = ?', [amount, id])
        self.connection.commit()

    def get_info_product(self, id):
        cur = self.connection.cursor()
        cur.execute('select * from products where id = ?', [id])
        return cur.fetchone() 

    def list_of_products(self,warehouse_id, order_by = 'name'):
        cur = self.connection.cursor()
        cur.execute('select * from products where warehouse_id = ? order by ?', [warehouse_id, order_by])
        return cur.fetchall()
    
    def check_date_of_product(self,id):
        cur = self.connection.cursor()
        cur.execute('select date from products where id = ?',[id])
        guarantee = dt.datetime.strptime(cur.fetchone()[0],'%Y-%m-%d').date()
        return (guarantee - dt.datetime.now().date()).days
    
    def list_of_warehouses(self):
        cur = self.connection.cursor()
        cur.execute('select * from warehouses')
        return cur.fetchall()

    def create_warehouse(self, name):
        if not name:
            return None
        cur = self.connection.cursor()
        cur.execute('select id from warehouses where name = ?',[name])
        data = cur.fetchone()
        if not data:
            cur.execute('''insert into warehouses(
                        name)
                        values(?)
                        ''',name)
            cur.execute('select id from warehouses where name = ?', [name])
            res = cur.fetchone()
            self.connection.commit()
            return res[0]
        else:
            return None

    def delete_warehouse(self,name):
        cur = self.connection.cursor()
        cur.execute('delete from warehouses where name = ?', [name])
        self.connection.commit()

    def current_warehouse(self,name):
        cur = self.connection.cursor()
        cur.execute('select id from warehouses where name = ?', [name])
        data = cur.fetchone()
        if data:
            return data[0]
        else:
            return None
        
