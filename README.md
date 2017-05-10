# Wechat_Sender

将程序运行结果及报警信息通过微信发送给你自己

## 简介

wechat_sender 是基于 [wxpy][1] 和 [tornado][2] 实现的一个可以将你的网站、爬虫、脚本等其他应用中各种消息 （日志、报警、运行结果等） 发给你的个人微信的工具

## 初衷

wxpy 基于 itchat 提供了较为完备的微信个人号 API ，而我想使用个人微信来接收我的网站的报警信息以及一些爬虫的结果，因此我写了这个工具。

## 安装

```python
pip install wechat_sender
```

## 运行环境

Python 2.7 及以上
Python 3 及以上

## 使用

如果你是 wxpy 的使用者，只需更改一句即可使用 wechat_sender：

例如这是你本来的代码：

```python
# coding: utf-8
from __future__ import unicode_literals

from wxpy import *
bot = Bot('bot.pkl')

my_friend = bot.friends().search('xxx')[0]

my_friend.send('Hello WeChat!')

@bot.register(Friend)
def reply_test(msg):
    msg.reply('test')

bot.join()
```

使用 wechat_sender：

```python
# coding: utf-8
from __future__ import unicode_literals

from wxpy import *
from wechat_sender import listen
bot = Bot('bot.pkl')

my_friend = bot.friends().search('xxx')[0]

my_friend.send('Hello WeChat!')

@bot.register(Friend)
def reply_test(msg):
    msg.reply('test')

listen(bot) # 只需改变最后一行代码
```

之后如果你想在其他地方发送微信消息给你自己，只需要：

```python
# coding: utf-8
from wechat_sender import send
send("test message")
```

[1]:https://github.com/youfou/wxpy
[2]:https://github.com/tornadoweb/tornado
