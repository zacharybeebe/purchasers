from sqlite3 import connect
from os import(environ,
               getcwd,
               makedirs)
from os.path import (exists,
                     isfile,
                     join)
from pickle import (dumps,
                    loads)
import sys
from config import MONTHS


class ORM(object):
    args = None
    exclude = None
    primary_key = None
    foreign_key = None

    # @staticmethod
    # def resource_path(relative_path):
    #     try:
    #         base_path = sys._MEIPASS
    #     except AttributeError:
    #         base_path = getcwd()
    #     return join(base_path, relative_path)
    #
    # @staticmethod
    # def make_directory_for_user_db():
    #     dir_path = join(environ['APPDATA'], 'TimberPlanner')
    #     if not exists(dir_path):
    #         makedirs(dir_path)
    #     file_path = join(dir_path, 'TIMBERSALES.db')
    #     if not isfile(file_path):
    #         ORM.create_tables(file_path)
    #     return file_path

    @staticmethod
    def connect_db(db):
        conn = connect(db)
        cur = conn.cursor()
        return conn, cur

    @staticmethod
    def create_tables(db):
        conn, cur = ORM.connect_db(db)
        subs = sorted(ORM.__subclasses__(), key=lambda x: x.__name__)
        # print(f'subclasses:: {subs}')
        for cls in subs:
            table = f'{cls.__name__.lower()}s'
            fk = cls.foreign_key
            add = ''
            if fk:
                for f in fk:
                    add += f""" , FOREIGN KEY ({f[0]}) REFERENCES {f[1]} ({f[2]})"""
            cols = f"""({', '.join([f'{key} {cls.args[key]}' for key in cls.args])}, PRIMARY KEY ({cls.primary_key}){add});"""
            sql = f"""CREATE TABLE {table} {cols}"""
            # print(f'sql-{table}:: {sql}')
            cur.execute(sql)
        conn.commit()
        conn.close()

    @staticmethod
    def get_last_primary(db, cls):
        conn, cur = ORM.connect_db(db)
        table = f'{cls.__name__.lower()}s'
        primary_key = cls.primary_key
        sql = f"""SELECT {primary_key} FROM {table}"""
        cur.execute(sql)
        data = cur.fetchall()
        conn.close()
        return data[-1][0]

    @staticmethod
    def get_fy_set(db):
        conn, cur = ORM.connect_db(db)
        sql = "SELECT fy FROM sales"
        cur.execute(sql)
        fys = cur.fetchall()
        conn.close()
        return sorted(list({i[0] for i in fys}))

    @staticmethod
    def select(db, cls, primary_value):
        conn, cur = ORM.connect_db(db)
        table = f'{cls.__name__.lower()}s'
        primary_key = cls.primary_key
        sql = f"""SELECT * FROM {table} WHERE {primary_key} = ?"""
        cur.execute(sql, [primary_value])
        data = cur.fetchone()
        conn.close()
        args = []
        for i in data:
            if isinstance(i, bytes):
                args.append(loads(i))
            else:
                args.append(i)
        return_class = cls(*args)
        return_class.set_db(db)
        return return_class

    @staticmethod
    def select_by_name(db, cls, name):
        conn, cur = ORM.connect_db(db)
        table = f'{cls.__name__.lower()}s'
        primary_key = 'name'
        sql = f"""SELECT * FROM {table} WHERE {primary_key} = ?"""
        cur.execute(sql, [name])
        data = cur.fetchone()
        conn.close()
        args = []
        for i in data:
            if isinstance(i, bytes):
                args.append(loads(i))
            else:
                args.append(i)
        return_class = cls(*args)
        return_class.set_db(db)
        return return_class

    @staticmethod
    def select_all_sales(db):
        cls = {i.__name__: i for i in ORM.__subclasses__()}['Sale']
        conn, cur = ORM.connect_db(db)
        sql = f"""SELECT * FROM sales"""
        cur.execute(sql)
        sales = cur.fetchall()
        conn.close()
        master = []
        for s in sales:
            args = []
            for i in s:
                if isinstance(i, bytes):
                    args.append(loads(i))
                else:
                    args.append(i)
            sale = cls(*args)
            sale.set_db(db)
            sale.get_bids()
            sale.get_stats()
            master.append(sale)
        master = sorted(master, key=lambda x: (x.fy, x.qtr, MONTHS[x.month]), reverse=True)
        return {i.name: i for i in master}

    @staticmethod
    def select_all_purchasers(db):
        cls = {i.__name__: i for i in ORM.__subclasses__()}['Purchaser']
        conn, cur = ORM.connect_db(db)
        sql = f"""SELECT * FROM purchasers"""
        cur.execute(sql)
        purchasers = cur.fetchall()
        conn.close()
        master = []
        for p in purchasers:
            args = []
            for i in p:
                if isinstance(i, bytes):
                    args.append(loads(i))
                else:
                    args.append(i)
            purchaser = cls(*args)
            purchaser.set_db(db)
            purchaser.get_bids()
            purchaser.get_stats()
            master.append(purchaser)
        master = sorted(master, key=lambda x: x.num_bids, reverse=True)
        return {i.name: i for i in master}

    @staticmethod
    def delete(db, cls, primary_value):
        conn, cur = ORM.connect_db(db)
        table = f'{cls.__name__.lower()}s'
        primary_key = cls.primary_key

        sql = f"""DELETE FROM {table} WHERE {primary_key} = ?"""
        cur.execute(sql, [primary_value])
        conn.commit()
        conn.close()

    @staticmethod
    def f_price(value):
        val_list = [i for i in str(round(value, 2))]
        if '.' not in val_list:
            add_to = ['.', '0', '0']
            for i in add_to:
                val_list.append(i)
        else:
            if len(val_list[-(len(val_list) - val_list.index('.')):]) < 3:
                val_list.append('0')
        temp = [i for i in reversed(val_list)]
        added = 0
        for i in range(3, len(val_list)):
            if i != 3 and i % 3 == 0:
                temp.insert(i + added, ',')
                added += 1
        return '${}'.format(''.join([i for i in reversed(temp)]))

    def __init__(self, ref):
        self.ref = ref
        self.db = None

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def set_db(self, db):
        self.db = db

    def insert_self(self):
        conn, cur = self.connect_db(self.db)
        table = f'{self.__class__.__name__.lower()}s'
        args = [i for i in self.args if i not in self.exclude]
        d = self.__dict__
        vals = []
        for key in d:
            if key not in self.exclude:
                if self.args[key] == 'BLOB':
                    vals.append(dumps(d[key]))
                else:
                    vals.append(d[key])
        sql = f"""INSERT into {table} ({', '.join(args)}) VALUES ({', '.join(['?' for _ in vals])})"""
        cur.execute(sql, vals)
        conn.commit()
        conn.close()

    def update_self(self):
        conn, cur = self.connect_db(self.db)
        table = f'{self.__class__.__name__.lower()}s'
        primary_key = self.primary_key
        args = [i for i in self.args if i not in self.exclude]
        d = self.__dict__
        vals = []
        for key in d:
            if key not in self.exclude:
                if self.args[key] == 'BLOB':
                    vals.append(dumps(d[key]))
                else:
                    vals.append(d[key])
        sql = f"""UPDATE {table}
                  SET ({', '.join(args)}) = ({', '.join(['?' for _ in vals])})
                  WHERE {primary_key} = ?;"""
        vals.append(self[primary_key])
        cur.execute(sql, vals)
        conn.commit()
        conn.close()