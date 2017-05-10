# coding: utf-8
from __future__ import unicode_literals


class WxBot(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(WxBot, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, bot=None, receiver=None, token=None, *args, **kwargs):
        self.bot = bot
        if not receiver:
            receiver = self.bot.file_helper
        self.receiver = receiver
        self.token = token
        super(WxBot, self).__init__(*args, **kwargs)

    def send_msg(self, msg):
        self.receiver.send(msg)
