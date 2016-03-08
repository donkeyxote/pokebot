#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import configparser
from telegram.bot import TelegramBot

if os.path.isfile('local_config.ini'):
    config_file = 'local_config.ini'
else:
    config_file = 'config.ini'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, config_file))

url = config.get('bot', 'url')
DB = None

if config.get('database', 'dbms') == 'postgres':
    param = {'host': config.get('database', 'host'),
             'port': config.get('database', 'port'),
             'database': config.get('database', 'name'),
             'user': config.get('database', 'user'),
             'password': config.get('database', 'password')}
    import db.postgres
    DB = db.postgres.Database(**param)

bot = TelegramBot(url, timeout=1, offset=None, db=DB)

if __name__ == '__main__':
    while True:
        bot.check_updates()

