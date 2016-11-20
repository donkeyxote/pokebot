#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from telegram.update import Update
from pokemon.pokemon import Pokemon
from utils.colorprint import colorprint

LOG = {'col': 'green'}
ERR = {'col': 'red'}

BASE_DIR = ''
media = {'pictures': dict(), 'video': dict()}


class TelegramBot:

    def __init__(self, url='', timeout=1, offset=None, db=None):
        self.__url = url + '{}'
        self.__timeout = timeout
        self.__offset = offset
        self.__db = db

    @staticmethod
    def format_pokemon(pkmn):
        res = ''
        if pkmn.get_name() is not None and pkmn.get_id() is not None:
            res += '*#{} {}:*\n'.format(str(pkmn.get_id()), pkmn.get_name().capitalize())
        if pkmn.get_damage() is not None:
            res += '\n*Debolezze e resistenze:*\n'
            damage = dict()
            for k, v in pkmn.get_damage().items():
                try:
                    damage[v].append(k)
                except KeyError:
                    damage[v] = [k]
            for key in sorted(damage.keys(), reverse=True):
                mul = key
                if mul < 1 and mul != 0:
                    mul = '1/{}'.format(str(int(1/mul)))
                else:
                    mul = str(int(mul))
                res += '*{}x*:\t'.format(mul)
                res += '{}, ' * damage[key].__len__()
                res = res[:-2] + '\n'
                res = res.format(*(sorted(damage[key])))
        if pkmn.get_name() is not None:
            res += '\nGuarda altri dettagli su [bulbapedia]' \
                   '(http://bulbapedia.bulbagarden.net/wiki/{})\n'.format(pkmn.get_name())
        return res

    def parse(self, update):
        try:
            res = None
            message = update.get_message()
            if message is not None:
                text = message.get_text()
                if text is not None and text.startswith('/'):
                    command = text.split(sep=' ', maxsplit=1)[0][1:]
                    if command == 'cerca':
                        name = text.split(sep=' ', maxsplit=3)[1]
                        pkmn = Pokemon(name=name, db=self.__db)
                        if pkmn.get_name() is not None:
                            res = self.format_pokemon(pkmn)
                if res:
                    requests.get(self.__url.format('sendMessage'),
                                 params={'parse_mode': 'Markdown', 'chat_id': message.get_chat().get_id(), 'text': res})
        except Exception as e:
            colorprint(str(e), **ERR)

    def check_updates(self):
        try:
            res = requests.get(self.__url.format('getUpdates'),
                               params={'timeout': self.__timeout, 'offset': self.__offset})
            updates = res.json()['result']
            if updates:
                for update in updates:
                    try:
                        upd = Update(data=update, db=self.__db)
                        colorprint(upd.__str__(), **LOG)
                        self.parse(upd)
                        self.__offset = upd.get_update_id() + 1
                    except Exception as e:
                        colorprint(str(e), **ERR)
        except Exception as e:
            colorprint(str(e), **ERR)
