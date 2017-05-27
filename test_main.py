# coding: utf-8
from __future__ import unicode_literals

import logging

import datetime
from wxpy import *
import sys

PY_VERSION = sys.version
PY2 = PY_VERSION < '3'


if PY2:
    bot = Bot('2bt.pkl')
    bot.enable_puid('botpy2.puid')
else:
    bot = Bot('3bt.pkl')
    bot.enable_puid('botpy3.puid')
my_friend = bot.friends(update=True).search('rapospectre')[0]
my_friend.send('Hello WeChat!')
group = bot.groups(update=True).search('Sender 信息群')[0]

print(my_friend.puid)
print(group.puid)


@bot.register(Friend)
def reply_test(msg):
    msg.reply('test')


from wechat_sender import listen

listen(bot, [my_friend, group], token='test', status_report=True, status_receiver=group,
       status_interval=datetime.timedelta(seconds=10))
# bot.join()
