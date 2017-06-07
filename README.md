# Wechat_Sender

随时随地发送消息到微信

http://wechat-sender.readthedocs.io/zh_CN/latest/

## 简介

wechat_sender 是基于 [wxpy][1] 和 [tornado][2] 实现的一个可以将你的网站、爬虫、脚本等其他应用中各种消息 （日志、报警、运行结果等） 发给到微信的工具

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

1. 登录微信并启动 wechat_sender 服务.

```python

   from wxpy import *
   from wechat_sender import *
   bot = Bot()
   listen(bot)
   # 之后 wechat_sender 将持续运行等待接收外部消息
```

2. 在外部向微信发送消息.

```python

   from wechat_sender import Sender
   Sender().send('Hello From Wechat Sender')
   # Hello From Wechat Sender 这条消息将通过 1 中登录微信的文件助手发送给你
```

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

之后如果你想在其他程序或脚本中发送微信消息，只需要：

```python
# coding: utf-8
from wechat_sender import Sender
Sender().send("test message")
```
## 文档

http://wechat-sender.readthedocs.io/zh_CN/latest/


## 交流

**扫描二维码，验证信息输入 'wechat_sender' 或 '加群' 进入微信交流群**

![screenshot](https://raw.githubusercontent.com/bluedazzle/wechat_sender/master/qr.jpeg)


## TODO LIST

- [x] 多 receiver
- [x] log handler 支持
- [ ] wxpy 掉线邮件通知
- [ ] wxpy 掉线重连

## 历史

**当前版本： 0.1.3**

2017.06.07 0.1.3:

优化代码，完善文档、注释

2017.06.04 0.1.2:

修复 sender timeout 时间过短问题；

修复初始化 listen 无 receiver 报错问题

增加 LoggingSenderHandler, 提供 log handler 支持

2017.05.27 0.1.1:

增加多 receiver 支持;

2017.05.27 0.1.0:

增加延时消息；

增加周期消息；

增加指定接收方消息；

增加 wechat_sender 控制命令;

增加 wxpy 状态监测功能；

优化代码；

2017.05.17 0.0.2:

优化代码

2017.05.11 0.0.1:

发布初版


[1]:https://github.com/youfou/wxpy
[2]:https://github.com/tornadoweb/tornado
