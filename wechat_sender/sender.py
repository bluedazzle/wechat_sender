# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import json

import datetime
import requests
import logging

from wechat_sender.utils import STATUS_SUCCESS, DEFAULT_REMIND_TIME
from wechat_sender.compatible import PY2, SYS_ENCODE
from functools import reduce


class Sender(object):
    """
    sender 对象，任何外部程序向微信发送消息都需要初始化 sender 对象::

        from wechat_sender import Sender
        sender = Sender(token='test', receiver='wechat_name,xxx,xxx')

        # 向 receiver 发送消息
        sender.send('Hello From Wechat Sender')

    """

    def __init__(self, token=None, receivers=None, host='http://localhost', port=10245):
        """
        :param token: (选填|str) - 信令，如果不为空请保持和 listen 中的 token 一致
        :param receivers: (选填|str) - 接收者，wxpy 的 puid 或 微信名、昵称等，多个发送者请使用半角逗号 ',' 分隔。不填将发送至 default_receiver
        :param host: (选填|str) - 远程地址，本地调用不用填写
        :param port: (选填|int) - 发送端口，默认 10245 端口，如不为空请保持和 listen 中的 port 一致
        """
        self.token = token
        if isinstance(receivers, list):
            self.receivers = ','.join(receivers)
        else:
            self.receivers = receivers
        self.host = host
        self.port = port
        self.remote = '{0}:{1}/'.format(self.host, self.port)
        self.data = {}
        self.timeout = 5

    def _wrap_post_data(self, **kwargs):
        self.data = kwargs
        if self.token:
            self.data['token'] = self.token
        if self.receivers:
            self.data['receivers'] = self.receivers
        return self.data

    def _convert_bytes(self, msg):
        if not PY2:
            if isinstance(msg, bytes):
                return str(msg, encoding=SYS_ENCODE)
        return msg

    def send(self, message):
        """
        发送基本文字消息

        :param message: (必填|str) - 需要发送的文本消息
        :return: * status：发送状态，True 发送成，False 发送失败
                 * message：发送失败详情
        """
        url = '{0}message'.format(self.remote)
        data = self._wrap_post_data(content=message)
        res = requests.post(url, data=data, timeout=self.timeout)
        if res.status_code == requests.codes.ok:
            res_data = json.loads(self._convert_bytes(res.content))
            if res_data.get('status') == STATUS_SUCCESS:
                return True, res_data.get('message')
            return False, res_data.get('message')
        res.raise_for_status()
        return False, 'Request or Response Error'

    def delay_send(self, content, time, title='', remind=DEFAULT_REMIND_TIME):
        """
        发送延时消息

        :param content: (必填|str) - 需要发送的消息内容
        :param time: (必填|str|datetime) - 发送消息的开始时间，支持 datetime.date、datetime.datetime 格式或者如 '2017-05-21 10:00:00' 的字符串
        :param title: (选填|str) - 需要发送的消息标题
        :param remind: (选填|int|datetime.timedelta) - 消息提醒时移，默认 1 小时，即早于 time 值 1 小时发送消息提醒, 支持 integer（毫秒） 或 datetime.timedelta
        :return: * status：发送状态，True 发送成，False 发送失败
                 * message：发送失败详情
        """
        url = '{0}delay_message'.format(self.remote)
        if isinstance(time, (datetime.datetime, datetime.date)):
            time = time.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(remind, datetime.timedelta):
            remind = remind.seconds
        if not isinstance(remind, int):
            raise ValueError
        data = self._wrap_post_data(title=title, content=content, time=time, remind=remind)
        res = requests.post(url, data=data, timeout=self.timeout)
        if res.status_code == requests.codes.ok:
            res_data = json.loads(self._convert_bytes(res.content))
            if res_data.get('status') == STATUS_SUCCESS:
                return True, res_data.get('message')
            return False, res_data.get('message')
        res.raise_for_status()
        return False, 'Request or Response Error'

    def periodic_send(self, content, interval, title=''):
        """
        发送周期消息

        :param content:  (必填|str) - 需要发送的消息内容
        :param interval: (必填|int|datetime.timedelta) - 发送消息间隔时间，支持 datetime.timedelta 或 integer 表示的秒数
        :param title: (选填|str) - 需要发送的消息标题
        :return: * status：发送状态，True 发送成，False 发送失败
                 * message：发送失败详情
        """
        url = '{0}periodic_message'.format(self.remote)
        if isinstance(interval, datetime.timedelta):
            interval = interval.seconds
        if not isinstance(interval, int):
            raise ValueError
        data = self._wrap_post_data(title=title, content=content, interval=interval)
        res = requests.post(url, data, timeout=self.timeout)
        if res.status_code == requests.codes.ok:
            res_data = json.loads(self._convert_bytes(res.content))
            if res_data.get('status') == STATUS_SUCCESS:
                return True, res_data.get('message')
            return False, res_data.get('message')
        res.raise_for_status()
        return False, 'Request or Response Error'

    def send_to(self, content, search):
        """
        向指定好友发送消息

        :param content: (必填|str) - 需要发送的消息内容
        :param search: (必填|str|dict|list)-搜索对象，同 wxpy.chats.search 使用方法一样。例如，可以使用字符串进行搜索好友或群，或指定具体属性搜索，如 puid=xxx 的字典
        :return: * status：发送状态，True 发送成，False 发送失败
                 * message：发送失败详情
        """
        url = '{0}send_to_message'.format(self.remote)
        if isinstance(search, dict):
            search = json.dumps(search)
        elif isinstance(search, list):
            search = reduce(lambda x, y: '{0} {1}'.format(x, y), search)
        data = self._wrap_post_data(content=content, search=search)
        res = requests.post(url, data=data, timeout=self.timeout)
        if res.status_code == requests.codes.ok:
            res_data = json.loads(self._convert_bytes(res.content))
            if res_data.get('status') == STATUS_SUCCESS:
                return True, res_data.get('message')
            return False, res_data.get('message')
        res.raise_for_status()
        return False, 'Request or Response Error'


class LoggingSenderHandler(logging.Handler, Sender):
    """
    wechat_sender 的 LoggingHandler 对象，可以使用 logging.addHandler() 的方式快速使外部应用支持微信日志输出。在外部应用中::

        # spider.py
        # 假如在一个爬虫脚本，我们想让此脚本的警告信息直接发到微信

        import logging
        from wechat_sender import LoggingSenderHandler

        logger = logging.getLogger(__name__)

        # spider code here
        def test_spider():
            ...
            logger.exception("EXCEPTION: XXX")

        def init_logger():
            sender_logger = LoggingSenderHandler('spider', level=logging.EXCEPTION)
            logger.addHandler(sender_logger)

        if __name__ == '__main__':
            init_logger()
            test_spider()

    """

    def __init__(self, name=None, token=None, receiver=None, host='http://localhost', port=10245, level=30):
        """
        :param name:  (选填|str) - 标识日志来源，不填将取应用所在服务器地址为名称
        :param token: (选填|str) - 信令，如果不为空请保持和 listen 中的 token 一致
        :param receiver: (选填|str) - 接收者，wxpy 的 puid 或 微信名、昵称等，不填将发送至 default_receiver
        :param host: (选填|str) - 远程地址，本地调用不用填写
        :param port: (选填|int) - 发送端口，默认 10245 端口，如不为空请保持和 listen 中的 port 一致
        :param level: (选填|int) - 日志输出等级，默认为 logging.WARNING
        """
        super(LoggingSenderHandler, self).__init__(level)
        Sender.__init__(self, token, receiver, host, port)
        if not name:
            import socket
            ip = socket.gethostbyname_ex(socket.gethostname())[0]
            name = ip
        self.name = name
        self.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))

    def emit(self, record):
        self.send('[{0}]\n{1}'.format(self.name, self.format(record)))
