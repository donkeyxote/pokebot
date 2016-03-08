#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
from pokemon.type import Type
from pokemon.poketype import PokeType

# CREATE TABLE pokemons (
#     id int NOT NULL,
#     name varchar(64) NOT NULL,
#     base_experience int,
#     height int,
#     order_number int,
#     weight int,
#     PRIMARY KEY (id)
# );

TABLE = 'pokemons'
COLUMNS = ('id', 'name', 'base_experience', 'height', 'order_number', 'weight')

ID = 0
NAME = 1
BASE_EXPERIENCE = 2
HEIGHT = 3
ORDER_NUMBER = 4
WEIGHT = 5

POKENAME = r'(\w|-)+'
POKEID = r'\d+'
POKESRC = r'(\w|%|.)+'

TYPE_COLUMNS = ('id', 'name')

URL = 'http://pokeapi.co/api/v2/pokemon/{}'
HTTP_OK = 200
HTTP_404 = 404


class Pokemon:

    def __init__(self, name='', db=None, row=None):
        self.__id = None
        self.__name = None
        self.__base_experience = None
        self.__height = None
        self.__order_number = None
        self.__weight = None
        self.__types = []
        self.__abilities = None
        self.__stats = None
        self.__damage = dict()
        if row is not None:
            row = self.load(row=row)
        elif db is not None:
            try:
                if re.fullmatch(POKEID, str(name)):
                    row = self.load(db=db, where={'id': name})
                elif re.fullmatch(POKENAME, name):
                    row = self.load(db=db, where={'name': name})
                elif re.fullmatch(POKESRC, name):
                    name = name.replace('*', '%').replace('.', '_')
                    row = self.load(db=db, where={'name': name})
            except Exception as e:
                print(str(e))
        if row is None and (re.fullmatch(POKENAME, name) or re.fullmatch(POKEID, str(name))):
            try:
                res = requests.get(URL.format(name.lower()))
                if res.status_code == HTTP_OK:
                    data = res.json()
                    self.__id = data['id']
                    self.__name = data['name']
                    self.__base_experience = data['base_experience']
                    self.__height = data['height']
                    self.__order_number = data['order']
                    self.__weight = data['weight']
                    if db is not None:
                        self.save(db)
                    for type in data["types"]:
                        self.__types.append(Type(type['type']['name'], db=db))
                    for type in self.__types:
                        PokeType(pokemon=self.get_name(), type=type.get_name(), db=db)
                    self.update_damage()
            except Exception as e:
                print(str(e))

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_base_experience(self):
        return self.__base_experience

    def get_height(self):
        return self.__height

    def get_order_number(self):
        return self.__order_number

    def get_weight(self):
        return self.__weight

    def get_types(self):
        return self.__types

    def get_abilities(self):
        return self.__abilities

    def get_stats(self):
        return self.__stats

    def get_damage(self):
        return self.__damage

    def update_damage(self):
        for type in self.__types:
            for attacker, damage in type.get_damage().items():
                if self.__damage.__contains__(attacker):
                    self.__damage[attacker] *= damage.get_multiplier()
                    if self.__damage[attacker] == 1:
                        self.__damage.pop(attacker)
                else:
                    self.__damage[attacker] = damage.get_multiplier()

    def save(self, db):
        data = (self.__id, self.__name, self.__base_experience, self.__height, self.__order_number, self.__weight)
        db.insert(table=TABLE, columns=COLUMNS, data=[data])

    def load(self, row=None, db=None, where=None):
        try:
            if row is None and db is not None:
                row = db.get(TABLE, where).fetchone()
            if row is not None:
                self.__id = row[ID]
                self.__name = row[NAME]
                self.__base_experience = row[BASE_EXPERIENCE]
                self.__height = row[HEIGHT]
                self.__order_number = row[ORDER_NUMBER]
                self.__weight = row[WEIGHT]
                for type in PokeType.get(db=db, where={'pokemon': self.get_name()}):
                    poketype = PokeType(row=type, db=db)
                    self.__types.append(Type(name=poketype.get_type(), db=db))
                self.update_damage()
            return row
        except Exception as e:
            print(str(e))

    @classmethod
    def get(cls, db, where=None):
        return db.get(table=TABLE, where=where)
