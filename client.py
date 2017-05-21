# coding: utf-8
from __future__ import unicode_literals

import datetime

from wechat_sender import delay_send, send

print delay_send('test title', 'test content', datetime.datetime.now() + datetime.timedelta(minutes=1),
                 remind=datetime.timedelta(seconds=30), token='test')
