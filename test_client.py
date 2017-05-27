# coding: utf-8
from __future__ import unicode_literals

import datetime

from wechat_sender import Sender
sender = Sender('test', '4f8c8e09')
sender.delay_send('延迟消息测试', time=datetime.datetime.now()+datetime.timedelta(hours=1), remind=datetime.timedelta(minutes=59))
sender.periodic_send('周期消息测试test', 10)
s1 = Sender('test', '7bf4594e')
s1.delay_send('延迟消息测试', time='2017-05-27 19:00:00')
s1.periodic_send('周期消息测试test', 10)
sender.send('tttt')
s1.send('ttts')
