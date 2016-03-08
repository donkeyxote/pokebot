#!/usr/bin/python
# -*- coding: utf-8 -*-

from telegram.message import Message


class Update:

    def __init__(self, data, db=None):
        self.__update_id = data['update_id']
        if data.__contains__('message'):
            self.__message = Message(data['message'], db=db)
        else:
            self.__message = None
        if data.__contains__('inline_query'):
            self.__inline_query = None
        else:
            self.__inline_query = None
        if data.__contains__('chosen_inline_result'):
            self.__chosen_inline_result = None
        else:
            self.__chosen_inline_result = None

    def get_update_id(self):
        return self.__update_id

    def get_message(self):
        return self.__message

    def get_inline_query(self):
        return self.__inline_query

    def get_chosen_inline_result(self):
        return self.__chosen_inline_result

    def __str__(self):
        message = self.get_message()
        if message is not None:
            return message.__str__()
        else:
            return 'update non managed yet'
