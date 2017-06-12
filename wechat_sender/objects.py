# coding: utf-8
from __future__ import unicode_literals

import json


class WxBot(object):
    """
    储存微信 bot 相关信息及 wechat_sender 各类 receiver 的类
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(WxBot, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    def __init__(self, bot=None, receivers=None, status_receiver=None, *args, **kwargs):
        """
        :param bot: wxpy bot 对象实例
        :param receivers:  wxpy chat 对象实例
        :param status_receiver: wxpy chat 对象实例
        """
        self.bot = bot
        self.receivers = {}
        self.default_receiver = None
        self.init_receivers(receivers)
        self.status_receiver = status_receiver if status_receiver else self.default_receiver
        self.receivers['status'] = self.status_receiver
        super(WxBot, self).__init__(*args, **kwargs)

    def init_receivers(self, receivers):
        """
        初始化 receivers
        """
        if not receivers:
            self.default_receiver = self.bot.file_helper
            return True
        if isinstance(receivers, list):
            self.default_receiver = receivers[0]
            for receiver in receivers:
                if self.bot.puid_map:
                    self.receivers[receiver.puid] = receiver
                self.receivers[receiver.name] = receiver
        else:
            self.default_receiver = receivers
            if self.bot.puid_map:
                self.receivers[receivers.puid] = receivers
            self.receivers[receivers.name] = receivers

    def send_msg(self, msg):
        """
        wxpy 发送文本消息的基本封装，这里会进行消息 receiver 识别分发
        """
        for receiver in msg.receivers:
            current_receiver = self.receivers.get(receiver, self.default_receiver)
            current_receiver.send_msg(msg)


class Message(object):
    """
    wechat_sender 消息类，是所有 wechat_sender 发送消息的基本类型
    """

    def __init__(self, content, title=None, time=None, remind=None, interval=None, receivers=None):
        """
        :param content: 消息内容
        :param title:  消息标题
        :param time:  消息时间
        :param remind: 消息提醒时间
        :param interval: 消息提醒间隔
        :param receivers: 消息接收者
        """
        self.title = title
        self.content = content
        self.message_time = time
        self.remind_time = None
        if time and remind:
            self.remind_time = time - remind
        self.nc = remind
        self.message_interval = interval
        self.receivers = [itm for itm in receivers.split(',')] if receivers else ['default']

    @property
    def time(self):
        """
        :return: 以字符串 "xxxx-xx-xx xx:xx:xx" 的形式返回消息的时间
        """
        return self.message_time.strftime('%Y-%m-%d %H:%M:%S') if self.message_time else None

    @property
    def interval(self):
        """
        :return: 返回消息提醒间隔的秒数
        """
        return '{0}s'.format(self.message_interval.seconds) if self.message_interval else None

    @property
    def remind(self):
        """
        :return: 以字符串 "xxxx-xx-xx xx:xx:xx" 的形式返回消息的提醒时间
        """
        return self.remind_time.strftime('%Y-%m-%d %H:%M:%S') if self.message_time else None

    def render_message(self):
        """
        渲染消息

        :return: 渲染后的消息
        """
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
    """
    wechat_sender 的全局对象类
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Global, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def insert(self, name, value):
        setattr(self, name, value)
        return True

    def __call__(self, *args, **kwargs):
        return self.__dict__
