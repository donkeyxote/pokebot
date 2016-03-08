#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

# CREATE TABLE chats (
#     id bigint NOT NULL,
#     type varchar(64) NOT NULL,
#     title varchar(256),
#     username varchar(64),
#     first_name varchar(64),
#     last_name varchar(64),
#     PRIMARY KEY (id)
# );

TABLE = 'chats'
COLUMNS = ('id', 'type', 'title', 'username', 'first_name', 'last_name')

ID = 0
TYPE = 1
TITLE = 2
USERNAME = 3
FIRST_NAME = 4
LAST_NAME = 5

TYPES = ('private', 'group', 'supergroup', 'channel')

CHATID = r'\d+'
NICK = r'@\w+'


class Chat:

    def __init__(self, chat=None, db=None, row=None):
        try:
            if row is not None:
                row = self.load(row=row)
            elif db is not None:
                try:
                    if re.fullmatch(CHATID, str(chat)):
                        row = self.load(db=db, where={'id': chat})
                    elif re.fullmatch(NICK, str(chat)):
                        row = self.load(db=db, where={'username': chat})
                except Exception as e:
                    print(str(e))
        except Exception as e:
            print(str(e))
        if row is None:
            try:
                self.__id = int(chat['id'])
                self.__type = chat['type']
                if chat.__contains__('title'):
                    self.__title = chat['title']
                else:
                    self.__title = None
                if chat.__contains__('username'):
                    self.__username = chat['username']
                else:
                    self.__username = None
                if chat.__contains__('first_name'):
                    self.__first_name = chat['first_name']
                else:
                    self.__first_name = None
                if chat.__contains__('last_name'):
                    self.__last_name = chat['last_name']
                else:
                    self.__last_name = None
                if db is not None:
                    self.update(db)
            except Exception as e:
                print(str(e))

    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__type

    def get_title(self):
        return self.__title

    def get_username(self):
        return self.__username()

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.get_last_name()

    def is_private(self):
        return self.__type == 'private'

    def is_group(self):
        return self.__type == 'group'

    def __str__(self):
        if self.is_private():
            return 'private chat (id: {})'.format(str(self.__id))
        elif self.is_group():
            return 'group {} (id: {})'.format(self.__title, self.__id)
        else:
            return 'chat id: {}'.format(self.__id)

    def save(self, db):
        data = (self.__id, self.__type, self.__title, self.__username, self.__first_name, self.__last_name)
        db.insert(table=TABLE, columns=COLUMNS, data=[data])

    def update(self, db):
        if db.get(table=TABLE, where={'id': self.__id}).fetchone() is None:
            self.save(db=db)
        else:
            data = (self.__id, self.__type, self.__title, self.__username, self.__first_name, self.__last_name)
            db.update(table=TABLE, columns=COLUMNS, data=data, where={'id': self.__id})

    def load(self, row=None, db=None, where=None):
        try:
            if row is None and db is not None:
                row = db.get(TABLE, where).fetchone()
            if row is not None:
                self.__id = row[ID]
                self.__type = row[TYPE]
                self.__title = row[TITLE]
                self.__username = row[USERNAME]
                self.__first_name = row[FIRST_NAME]
                self.__last_name = row[LAST_NAME]
            return row
        except Exception as e:
            print(str(e))

    @classmethod
    def get(cls, db, where=None):
        return db.get(table=TABLE, where=where)
