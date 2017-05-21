# coding: utf-8
from __future__ import unicode_literals

import datetime

from wechat_sender import delay_send, send

print delay_send('test title', 'test content', '2017-05-21 19:20:00', remind=datetime.timedelta(seconds=30), token='test')
