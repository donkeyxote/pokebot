#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from telegram.user import User
from telegram.chat import Chat


class Message:

    def __init__(self, message, db=None):
        try:
            self.__message_id = message['message_id']
            if message.__contains__('from'):
                self.__from = User(message['from'], db=db)
            else:
                self.__from = None
            self.__date = message['date']
            self.__chat = Chat(message['chat'], db=db)
            if message.__contains__('forward_from'):
                self.__forward_from = User(message['forward_from'], db=db)
            else:
                self.__forward_from = None
            if message.__contains__('forward_date'):
                self.__forward_date = message['forward_date']
            else:
                self.__forward_date = None
            if message.__contains__('reply_to_message'):
                self.__reply_to_message = Message(message['reply_to_message'], db=db)
            else:
                self.__reply_to_message = None
            if message.__contains__('text'):
                self.__text = message['text']
            else:
                self.__text = None
            if message.__contains__('audio'):
                self.__audio = None
            else:
                self.__audio = None
            if message.__contains__('document'):
                self.__document = None
            else:
                self.__document = None
            if message.__contains__('photo'):
                self.__photo = None
            else:
                self.__photo = None
            if message.__contains__('sticker'):
                self.__sticker = None
            else:
                self.__sticker = None
            if message.__contains__('video'):
                self.__video = None
            else:
                self.__video = None
            if message.__contains__('voice'):
                self.__voice = None
            else:
                self.__voice = None
            if message.__contains__('caption'):
                self.__caption = None
            else:
                self.__caption = None
            if message.__contains__('contact'):
                self.__contact = None
            else:
                self.__contact = None
            if message.__contains__('location'):
                self.__location = None
            else:
                self.__location = None
            if message.__contains__('new_chat_participant'):
                self.__new_chat_participant = User(message['new_chat_participant'], db=db)
            else:
                self.__new_chat_participant = None
            if message.__contains__('left_chat_participant'):
                self.__left_chat_participant = User(message['left_chat_participant'], db=db)
            else:
                self.__left_chat_participant = None
            if message.__contains__('new_chat_title'):
                self.__new_chat_title = message['new_chat_title']
            else:
                self.__new_chat_title = None
            if message.__contains__('new_chat_photo'):
                self.__new_chat_photo = None
            else:
                self.__new_chat_photo = None
            if message.__contains__('delete_chat_photo'):
                self.__delete_chat_photo = message['delete_chat_photo']
            else:
                self.__delete_chat_photo = None
            if message.__contains__('group_chat_created'):
                self.__group_chat_created =	message['group_chat_created']
            else:
                self.__group_chat_created = None
            if message.__contains__('supergroup_chat_created'):
                self.__supergroup_chat_created = message['supergroup_chat_created']
            else:
                self.__supergroup_chat_created = None
            if message.__contains__('channel_chat_created'):
                self.__channel_chat_created = message['channel_chat_created']
            else:
                self.__channel_chat_created = None
            if message.__contains__('migrate_to_chat_id'):
                self.__migrate_to_chat_id = message['migrate_to_chat_id']
            else:
                self.__migrate_to_chat_id = None
            if message.__contains__('migrate_from_chat_id'):
                self.__migrate_from_chat_id = message['migrate_from_chat_id']
            else:
                self.__migrate_from_chat_id = None
        except Exception as e:
            print(str(e))

    def get_message_id(self):
        return self.__message_id

    def get_from(self):
        return self.__from

    def get_date(self):
        return self.__date

    def get_chat(self):
        return self.__chat

    def get_forward_from(self):
        return self.__forward_from

    def get_forward_date(self):
        return self.__forward_date

    def get_reply_to_message(self):
        return self.__reply_to_message

    def get_text(self):
        return self.__text

    def get_audio(self):
        return self.__audio

    def get_document(self):
        return self.__document

    def get_photo(self):
        return self.__photo

    def get_sticker(self):
        return self.__sticker

    def get_video(self):
        return self.__video

    def get_voice(self):
        return self.__voice

    def get_caption(self):
        return self.__caption

    def get_contact(self):
        return self.__contact

    def get_location(self):
        return self.__location

    def get_new_chat_participant(self):
        return self.__new_chat_participant

    def get_left_chat_participant(self):
        return self.__left_chat_participant

    def get_new_chat_title(self):
        return self.__new_chat_title

    def get_new_chat_photo(self):
        return self.__new_chat_photo

    def get_delete_chat_photo(self):
        return self.__delete_chat_photo

    def get_group_chat_created(self):
        return self.__group_chat_created

    def get_supergroup_chat_created(self):
        return self.__supergroup_chat_created

    def get_channel_chat_created(self):
        return self.__channel_chat_created

    def get_migrate_to_chat_id(self):
        return self.__migrate_to_chat_id

    def get_migrate_from_chat_id(self):
        return self.__migrate_from_chat_id

    def __str__(self):
        date = datetime.fromtimestamp(self.__date).strftime('%Y-%m-%d %H:%M:%S')
        if self.__text is not None:
            string = 'New message from user {} in {} at {}:\n{}'
            return string.format(self.__from.__str__(),
                                 self.__chat.__str__(),
                                 date,
                                 self.__text)
        elif self.__new_chat_title is not None:
            return 'New name for {} by user {} at {}'.format(self.__chat.__str__(), self.__from.__str__(), date)
        else:
            return 'Message not managed'
