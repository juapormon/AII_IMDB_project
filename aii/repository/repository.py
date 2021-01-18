import sqlite3


class Repository:
    def __init__(self, db_uri='../db/practica1.db'):
        self.db = db_uri

    def connect(self):
        conn = sqlite3.connect(self.db)
        conn.text_factory = str
        return conn

    def write(self, command):
        conn = self.connect()
        conn.execute(command)
        # conn.commit()
        # conn.close()
        return conn

    # def insert(self, table_name, map):
    #
    #     values = map.values()
    #     keys = map.keys()
    #     verbose = \
    #         f"INSERT INTO {table_name.upper()} [({map.keys().__str__().replace('[','')})]" \
    #         " VALUES (value1, value2, value3,...valueN);"

    def read(self, command):
        conn = self.connect()
        conn.execute(command)
        conn.close()

    def initialize(self):
        sample = open('../db/createTables.sql')
        content = sample.read()
        content = content.split(';')
        for command in content:
            self.write(command)
        else:
            print('Content Write!')
