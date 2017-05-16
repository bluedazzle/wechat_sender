# coding: utf-8
from __future__ import unicode_literals

import json

import requests

from wechat_sender.utils import STATUS_SUCCESS


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
    return False, 'Request Error'
