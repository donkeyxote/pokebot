#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

# CREATE TABLE damages (
#     attacker varchar(32) NOT NULL,
#     defender varchar(32) NOT NULL,
#     multiplier float NOT NULL,
#     PRIMARY KEY (attacker, defender),
#     FOREIGN KEY (attacker) REFERENCES types(name),
#     FOREIGN KEY (defender) REFERENCES types(name)
# );

TABLE = 'damages'
COLUMNS = ('attacker', 'defender', 'multiplier')

ATTACKER = 0
DEFENDER = 1
MULTIPLIER = 2

MULTIPLIER_REGEXP = r'\d+(.\d*)?'
TYPENAME = r'\w+'


class Damage:

    def __init__(self, attacker=None, defender=None, multiplier=None, db=None, row=None):
        self.__attacker = None
        self.__defender = None
        self.__multiplier = 1
        if row is not None:
            row = self.load(row=row)
        elif db is not None:
            try:
                if re.fullmatch(TYPENAME, attacker) and re.fullmatch(TYPENAME, defender):
                    row = self.load(db=db, where={'attacker': attacker, 'defender': defender})
            except Exception as e:
                print(str(e))
        if row is None and (not (
                not re.fullmatch(TYPENAME, attacker) or not re.fullmatch(TYPENAME, defender) or not re.fullmatch(
                MULTIPLIER_REGEXP, str(multiplier)))):
            try:
                self.__attacker = attacker
                self.__defender = defender
                self.__multiplier = multiplier
                if db is not None:
                    self.save(db)
            except Exception as e:
                print(str(e))

    def get_attacker(self):
        return self.__attacker

    def get_defender(self):
        return self.__defender

    def get_multiplier(self):
        return self.__multiplier

    def save(self, db):
        data = (self.__attacker, self.__defender, self.__multiplier)
        db.insert(table=TABLE, columns=COLUMNS, data=[data])

    def load(self, row=None, db=None, where=None):
        try:
            if row is None and db is not None:
                row = db.get(TABLE, where).fetchone()
            if row is not None:
                self.__attacker = row[ATTACKER]
                self.__defender = row[DEFENDER]
                self.__multiplier = row[MULTIPLIER]
            return row
        except Exception as e:
            print(str(e))

    @classmethod
    def get(cls, db, where=None):
        return db.get(table=TABLE, where=where)
