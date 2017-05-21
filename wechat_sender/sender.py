# coding: utf-8
from __future__ import unicode_literals

import json

import datetime
import requests

from wechat_sender.utils import STATUS_SUCCESS, DEFAULT_REMIND_TIME


def send(message, token=None, port=10245):
    url = 'http://localhost:{0}/message'.format(port)
    data = {'content': message}
    if token:
        data['token'] = token
    res = requests.post(url, data=data, timeout=2)
    if res.status_code == 200:
        res_data = json.loads(res.content)
        if res_data.get('status') == STATUS_SUCCESS:
            return True, res_data.get('message')
        return False, res_data.get('message')
    return False, 'Request or Response Error'


def delay_send(title, content, time, remind=DEFAULT_REMIND_TIME, token=None, port=10245):
    url = 'http://localhost:{0}/delay_message'.format(port)
    if isinstance(remind, datetime.timedelta):
        remind = remind.seconds
    if not isinstance(remind, (int, long)):
        raise ValueError
    data = {'title': title,
            'content': content,
            'time': time,
            'remind': remind}
    if token:
        data['token'] = token
    res = requests.post(url, data=data, timeout=2)
    if res.status_code == 200:
        res_data = json.loads(res.content)
        if res_data.get('status') == STATUS_SUCCESS:
            return True, res_data.get('message')
        return False, res_data.get('message')
    return False, 'Request or Response Error'
