#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
from pokemon.damage import Damage

# CREATE TABLE types (
#     id int NOT NULL,
#     name varchar(32) NOT NULL,
#     PRIMARY KEY (name)
# );

TABLE = 'types'
COLUMNS = ('id', 'name')

ID = 0
NAME = 1

TYPENAME = r'\w+'
TYPEID = r'\d+'

URL = 'http://pokeapi.co/api/v2/type/{}'
HTTP_OK = 200
HTTP_404 = 404


class Type:

    def __init__(self, name='', db=None, row=None):
        self.__id = None
        self.__name = None
        self.__damaged = dict()
        if row is not None:
            row = self.load(row=row)
        elif db is not None:
            try:
                if re.fullmatch(TYPEID, str(name)):
                    row = self.load(db=db, where={'id': name})
                elif re.fullmatch(TYPENAME, name):
                    row = self.load(db=db, where={'name': name})
            except Exception as e:
                print(str(e))
        if row is None and (re.fullmatch(TYPENAME, name) or re.fullmatch(TYPEID, str(name))):
            try:
                res = requests.get(URL.format(name.lower()))
                if res.status_code == HTTP_OK:
                    data = res.json()
                    self.__id = data['id']
                    self.__name = data['name']
                    if db is not None:
                        self.save(db)
                    damage_relations = data['damage_relations']
                    for relation in damage_relations['no_damage_from']:
                        if db is not None and self.get(db=db, where={'name': relation['name']}).fetchone() is None:
                            Type(name=relation['name'], db=db)
                        self.__damaged[relation['name']] = Damage(attacker=relation['name'],
                                                                  defender=self.__name, multiplier=0, db=db)
                    for relation in damage_relations['half_damage_from']:
                        if db is not None and self.get(db=db, where={'name': relation['name']}).fetchone() is None:
                            Type(name=relation['name'], db=db)
                        self.__damaged[relation['name']] = Damage(attacker=relation['name'],
                                                                  defender=self.__name, multiplier=0.5, db=db)
                    for relation in damage_relations['double_damage_from']:
                        if db is not None and self.get(db=db, where={'name': relation['name']}).fetchone() is None:
                            Type(name=relation['name'], db=db)
                        self.__damaged[relation['name']] = Damage(attacker=relation['name'],
                                                                  defender=self.__name, multiplier=2, db=db)
            except Exception as e:
                print(str(e))

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_damage(self):
        return self.__damaged

    def save(self, db):
        data = (self.__id, self.__name)
        db.insert(table=TABLE, columns=COLUMNS, data=[data])

    def load(self, row=None, db=None, where=None):
        try:
            if row is None and db is not None:
                row = db.get(TABLE, where).fetchone()
            if row is not None:
                self.__id = row[ID]
                self.__name = row[NAME]
                for res in Damage.get(db=db, where={'defender': self.get_name()}).fetchall():
                    damage = Damage(row=res, db=db)
                    self.__damaged[damage.get_attacker()] = damage
            return row
        except Exception as e:
            print(str(e))

    @classmethod
    def get(cls, db, where=None):
        return db.get(table=TABLE, where=where)
