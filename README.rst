Wechat\_Sender
==============

随时随地发送消息到微信

简介
----

wechat\_sender 是基于 `wxpy`_ 和 `tornado`_
实现的一个可以将你的网站、爬虫、脚本等其他应用中各种消息
（日志、报警、运行结果等） 发送到微信的工具

初衷
----

wxpy 基于 itchat 提供了较为完备的微信个人号 API
，而我想使用个人微信来接收我的网站的报警信息以及一些爬虫的结果，因此我写了这个工具。

安装
----

.. code:: python

    pip install wechat_sender

运行环境
--------

Python 2.7 及以上
Python 3 及以上


使用
----

1. 登录微信并启动 wechat_sender 服务.

.. code:: python

   from wxpy import *
   from wechat_sender import *
   bot = Bot()
   listen(bot)
   # 之后 wechat_sender 将持续运行等待接收外部消息

2. 在外部向微信发送消息.

.. code:: python

   from wechat_sender import Sender
   Sender().send('Hello From Wechat Sender')
   # Hello From Wechat Sender 这条消息将通过 1 中登录微信的文件助手发送给你


如果你是 wxpy 的使用者，只需更改一句即可使用 wechat\_sender：

例如这是你本来的代码：

.. code:: python

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

使用 wechat\_sender：

.. code:: python

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

之后如果你想在其他程序或脚本中向微信发消息，只需要：

.. code:: python

    # coding: utf-8
    from wechat_sender import Sender
    Sender().send("Hello From Wechat Sender")


交流
----

**扫描二维码，验证信息输入 ‘wechat\_sender’ 或 ‘加群’ 进入微信交流群**

|screenshot|

.. _wxpy: https://github.com/youfou/wxpy
.. _tornado: https://github.com/tornadoweb/tornado

.. |screenshot| image:: https://raw.githubusercontent.com/bluedazzle/wechat_sender/master/qr.jpeg
