# coding: utf-8
from __future__ import unicode_literals


class WxBot(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(WxBot, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, bot=None, receiver=None, *args, **kwargs):
        self.bot = bot
        if not receiver:
            receiver = self.bot.file_helper
        self.receiver = receiver
        super(WxBot, self).__init__(*args, **kwargs)

    def send_msg(self, msg):
        self.receiver.send_msg(msg)


class Message(object):
    def __init__(self, content, title=None, time=None, remind=None, interval=None):
        self.title = title
        self.content = content
        self.message_time = time
        self.remind_time = None
        if time and remind:
            self.remind_time = time - remind
        self.nc = remind
        self.message_interval = interval

    @property
    def time(self):
        return self.message_time.strftime('%Y-%m-%d %H:%M:%S') if self.message_time else None

    @property
    def interval(self):
        return '{0}s'.format(self.message_interval.seconds) if self.message_interval else None

    @property
    def remind(self):
        return self.remind_time.strftime('%Y-%m-%d %H:%M:%S') if self.message_time else None

    def render_message(self):
        message = None
        if self.title:
            message = '标题：{0}'.format(self.title)
        if self.message_time:
            message = '{0}\n时间：{1}'.format(message, self.time)
        if message:
            message = '{0}\n内容：{1}'.format(message, self.content)
        else:
            message = self.content
        return message

    def __repr__(self):
        return self.render_message()


class Global(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Global, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def insert(self, name, value):
        setattr(self, name, value)
        return True

    def __call__(self, *args, **kwargs):
        return self.__dict__
