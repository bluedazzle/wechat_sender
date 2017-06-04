# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import json

import datetime
import requests
import logging

from wechat_sender.utils import STATUS_SUCCESS, DEFAULT_REMIND_TIME
from functools import reduce


class Sender(object):
    def __init__(self, token=None, receiver=None, host='http://localhost', port=10245):
        self.token = token
        self.receiver = receiver
        self.host = host
        self.port = port
        self.remote = '{0}:{1}/'.format(self.host, self.port)
        self.data = {}
        self.timeout = 5

    def _wrap_post_data(self, **kwargs):
        self.data = kwargs
        if self.token:
            self.data['token'] = self.token
        if self.receiver:
            self.data['receiver'] = self.receiver
        return self.data

    def send(self, message):
        url = '{0}message'.format(self.remote)
        data = self._wrap_post_data(content=message)
        res = requests.post(url, data=data, timeout=self.timeout)
        if res.status_code == requests.codes.ok:
            res_data = json.loads(res.content)
            if res_data.get('status') == STATUS_SUCCESS:
                return True, res_data.get('message')
            return False, res_data.get('message')
        res.raise_for_status()
        return False, 'Request or Response Error'

    def delay_send(self, content, time, title='', remind=DEFAULT_REMIND_TIME):
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
            res_data = json.loads(res.content)
            if res_data.get('status') == STATUS_SUCCESS:
                return True, res_data.get('message')
            return False, res_data.get('message')
        res.raise_for_status()
        return False, 'Request or Response Error'

    def periodic_send(self, content, interval, title=''):
        url = '{0}periodic_message'.format(self.remote)
        if isinstance(interval, datetime.timedelta):
            interval = interval.seconds
        if not isinstance(interval, int):
            raise ValueError
        data = self._wrap_post_data(title=title, content=content, interval=interval)
        res = requests.post(url, data, timeout=self.timeout)
        if res.status_code == requests.codes.ok:
            res_data = json.loads(res.content)
            if res_data.get('status') == STATUS_SUCCESS:
                return True, res_data.get('message')
            return False, res_data.get('message')
        res.raise_for_status()
        return False, 'Request or Response Error'

    def send_to(self, content, search):
        url = '{0}send_to_message'.format(self.remote)
        if isinstance(search, dict):
            search = json.dumps(search)
        elif isinstance(search, list):
            search = reduce(lambda x, y: '{0} {1}'.format(x, y), search)
        data = self._wrap_post_data(content=content, search=search)
        res = requests.post(url, data=data, timeout=self.timeout)
        if res.status_code == requests.codes.ok:
            res_data = json.loads(res.content)
            if res_data.get('status') == STATUS_SUCCESS:
                return True, res_data.get('message')
            return False, res_data.get('message')
        res.raise_for_status()
        return False, 'Request or Response Error'


class LoggingSenderHandler(logging.Handler, Sender):
    def __init__(self, name=None, token=None, receiver=None, host='http://localhost', port=10245, level=30):
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
