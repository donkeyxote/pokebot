#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2


class Database:

    __dbms = 'postgres'

    def __init__(self, dsn=None, database=None, user=None, password=None, host=None, port=None,
                 connection_factory=None, cursor_factory=None, async=False):
        self.__conn = None

        self.__param = {'dsn': dsn,
                        'database': database,
                        'user': user,
                        'password': password,
                        'host': host,
                        'port': port,
                        'connection_factory': connection_factory,
                        'cursor_factory': cursor_factory,
                        'async': async
                        }

    def get_connection(self):
        try:
            conn = psycopg2.connect(**self.__param)
            return conn
        except Exception as e:
            raise e

    def insert(self, table, columns, data):
        conn = self.get_connection()
        cur = conn.cursor()
        sql = 'INSERT INTO {} ({}) VALUES ({});'.format(table, ', '.join(columns), str('%s, ' * columns.__len__())[:-2])
        for row in data:
            cur.execute(sql, row)
        conn.commit()
        conn.close()

    def get(self, table, where=None):
        conn = self.get_connection()
        cur = conn.cursor()
        where_sql, row = self.parse_where(where)
        sql = 'SELECT * FROM {} {};'.format(table, where_sql)
        cur.execute(sql, row)
        return cur

    def update(self, table, columns, data, where):
        set_sql, set_row = self.parse_set(columns=columns, data=data)
        where_sql, where_row = self.parse_where(where=where)
        row = (*set_row, *where_row)
        conn = self.get_connection()
        cur = conn.cursor()
        sql = 'UPDATE {} {} {};'.format(table, set_sql, where_sql)
        cur.execute(sql, row)
        conn.commit()
        conn.close()

    @staticmethod
    def parse_where(where=None):
        if where is None:
            return '', ''
        else:
            row = []
            sql = 'WHERE {} {} {} AND {}'
            for k, v in where.items():
                sql = sql.format(k,
                                 'LIKE' if (str(v).__contains__('%') or str(v).__contains__('_')) else '=',
                                 '%s',
                                 '{} {} {} AND {}')
                row.append(v)
            sql = sql[:-len(' AND {} {} {} AND {}')]
            return sql, (*row,)

    @staticmethod
    def parse_set(columns, data):
        if columns is None or data is None:
            return '', ''
        else:
            sql = 'SET {} = {}, {}'
            row = []
            for i in range(columns.__len__()):
                sql = sql.format(columns[i], '%s', '{} = {}, {}')
                row.append(data[i])
            sql = sql[:-len(', {} = {}, {}')]
            return sql, (*row,)
