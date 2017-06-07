Sender 发送者对象
=================

..  module:: wechat_sender

Sender 对象可以理解为在外部程序中（ 非 wechat_sender 服务，例如你的个人脚本、网站等 ）向微信发送消息的发送者

.. autoclass:: Sender

.. automethod:: Sender.__init__

.. automethod:: Sender.send

.. automethod:: Sender.delay_send

发送延时消息

某些情况下，我们希望消息可以延迟发送，例如日程、会议提醒等，这时用 :func:`Sender.delay_send` 即可满足需求::

    # coding: utf-8
    import datetime
    from wechat_sender import Sender

    sender = Sender()
    time = datetime.datetime.now()+datetime.timedelta(hours=1)
    sender.delay_send(content="测试内容", time=time, title="测试标题", remind=datetime.timedelta(minutes=59))

如果返回正常，1 分钟后你将收到这条消息时间是 1 小时后的消息提醒::

    #标题：测试标题
    #时间：2017-06-07 12:56:16
    #内容：延迟消息测试


.. automethod:: Sender.periodic_send

发送周期消息

如果希望某条消息周期性发送到微信，可以使用 :func:`Sender.periodic_send`::

    # coding: utf-8
    import datetime
    from wechat_sender import Sender

    sender = Sender()
    interval = datetime.timedelta(seconds=10)
    sender.periodic_send(content='测试消息', interval=interval, title='测试标题')

如果返回正常，每隔 10 s 你将收到一条消息如下::

    # 标题：测试标题
    # 内容：周期消息测试test

.. tip::

    使用 :doc:`command` 查看已注册的延时\周期消息

.. automethod:: Sender.send_to

发送定向消息

如果你希望某条消息发送给指定的微信好友，你可以使用 :func:`Sender.send_to`::

    # coding: utf-8
    import datetime
    from wechat_sender import Sender

    sender = Sender()
    sender.send_to('Hello From Wechat Sender', '微信好友昵称')

如果返回正常，你指定的微信好友将收到这条消息

.. tip::

    | :func:`Sender.send_to` 的 search 参数使用方法和 wxpy 的 `wxpy.chats().search() <http://wxpy.readthedocs.io/zh/latest/bot.html#id4>`_. 一致
    | 直接搜索昵称或用综合查询条件均可以搜索好友

使用多条件查询好友::

    # coding: utf-8
    import datetime
    from wechat_sender import Sender

    sender = Sender()
    sender.send_to('Hello From Wechat Sender', search={'city': 'xx', 'nick_name': 'xxx'})



Sender 日志对象
=================

Sender 日志对象可以更平滑的接入外部应用的 log 系统中，基本无需更改代码即可使应用日志发送到微信

.. autoclass:: LoggingSenderHandler

.. automethod:: LoggingSenderHandler.__init__