#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

# CREATE TABLE users (
#     id int NOT NULL,
#     first_name varchar(64) NOT NULL,
#     last_name varchar(64),
#     username varchar(64),
#     PRIMARY KEY (id)
# );

TABLE = 'users'
COLUMNS = ('id', 'first_name', 'last_name', 'username')

ID = 0
FIRST_NAME = 1
LAST_NAME = 2
USERNAME = 3

USERID = r'\d+'
NICK = r'@\w+'


class User:

    def __init__(self, user=None, db=None, row=None):
        try:
            if row is not None:
                row = self.load(row=row)
            elif db is not None:
                try:
                    if re.fullmatch(USERID, str(user)):
                        row = self.load(db=db, where={'id': user})
                    elif re.fullmatch(NICK, str(user)):
                        row = self.load(db=db, where={'username': user})

                except Exception as e:
                    print(str(e))
        except Exception as e:
            print(str(e))
        if row is None:
            try:
                self.__id = int(user['id'])
                if user.__contains__('first_name'):
                    self.__first_name = user['first_name']
                else:
                    user.__first_name = None
                if user.__contains__('last_name'):
                    self.__last_name = user['last_name']
                else:
                    self.__last_name = None
                if user.__contains__('username'):
                    self.__username = user['username']
                else:
                    self.__username = None
                if db is not None:
                    self.update(db)
            except Exception as e:
                print(str(e))

    def get_id(self):
        return self.__id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.get_last_name()

    def get_username(self):
        return self.__username()

    def __str__(self):
        if self.__username is not None:
            return self.__username
        elif self.__first_name is not None:
            if self.__last_name is not None:
                return self.__first_name + self.__last_name
            else:
                return self.__first_name
        else:
            return str(self.__id)

    def save(self, db):
        data = (self.__id, self.__first_name, self.__last_name, self.__username)
        db.insert(table=TABLE, columns=COLUMNS, data=[data])

    def update(self, db):
        if db.get(table=TABLE, where={'id': self.__id}).fetchone() is None:
            self.save(db=db)
        else:
            data = (self.__id, self.__first_name, self.__last_name, self.__username)
            db.update(table=TABLE, columns=COLUMNS, data=data, where={'id': self.__id})

    def load(self, row=None, db=None, where=None):
        try:
            if row is None and db is not None:
                row = db.get(TABLE, where).fetchone()
            if row is not None:
                self.__id = row[ID]
                self.__first_name = row[FIRST_NAME]
                self.__last_name = row[LAST_NAME]
                self.__username = row[USERNAME]
            return row
        except Exception as e:
            print(str(e))

    @classmethod
    def get(cls, db, where=None):
        return db.get(table=TABLE, where=where)
