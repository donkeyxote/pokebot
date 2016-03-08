#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

# CREATE TABLE pokemons_types (
#     pokemon varchar(64) NOT NULL,
#     type varchar(32) NOT NULL,
#     PRIMARY KEY (pokemon, type),
#     FOREIGN KEY (pokemon) REFERENCES pokemons(name),
#     FOREIGN KEY (type) REFERENCES types(name)
# );

TABLE = 'pokemons_types'
COLUMNS = ('pokemon', 'type')

POKEMON = 0
TYPE = 1

POKENAME = r'(\w|-)+'
TYPENAME = r'\w+'


class PokeType:

    def __init__(self, pokemon=None, type=None, db=None, row=None):
        self.__pokemon = None
        self.__type = None
        if row is not None:
            row = self.load(row=row)
        elif db is not None:
            try:
                if re.fullmatch(POKENAME, pokemon) and re.fullmatch(TYPENAME, type):
                    row = self.load(db=db, where={'pokemon': pokemon, 'type': type})
            except Exception as e:
                print(str(e))
        if row is None and (re.fullmatch(POKENAME, pokemon) and re.fullmatch(TYPENAME, type)):
            try:
                self.__pokemon = pokemon
                self.__type = type
                if db is not None:
                    self.save(db)
            except Exception as e:
                print(str(e))

    def get_pokemon(self):
        return self.__pokemon

    def get_type(self):
        return self.__type

    def save(self, db):
        data = (self.__pokemon, self.__type)
        db.insert(table=TABLE, columns=COLUMNS, data=[data])

    def load(self, row=None, db=None, where=None):
        try:
            if row is None and db is not None:
                row = db.get(TABLE, where).fetchone()
            if row is not None:
                self.__pokemon = row[POKEMON]
                self.__type = row[TYPE]
            return row
        except Exception as e:
            print(str(e))

    @classmethod
    def get(cls, db, where=None):
        return db.get(table=TABLE, where=where)
