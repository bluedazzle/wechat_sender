listen 方法
=============

..  module:: wechat_sender

listen() 方法用于监听 wxpy 的 bot 对象实例并启动 wechat_sender 服务，为外部发送消息到微信提供支持。

.. autofunction:: listen

.. tip::

    | 专门申请一个微信号负责发送应用消息及日志信息
    | 避免使用自己的个人微信造成不便
    | 可以把接收者指定为个人微信

指定接收者
--------------

.. code:: python

    from wxpy import *
    from wechat_sender import listen

    # 这里登录单独申请的微信号
    bot = Bot()
    # 这里查询你的个人微信, search 填入你的微信昵称
    my = bot.friends().search('your name')[0]
    # 传入你的私人微信作为接收者
    listen(bot, receivers=my)

向你的私人微信发送消息::

    from wechat_sender import Sender
    Sender().send('hello')

指定多个接收者
---------------------

.. code:: python

    from wxpy import *
    from wechat_sender import listen

    # 这里登录单独申请的微信号
    bot = Bot()
    # 这里查询你的个人微信, search 填入你的微信昵称
    my = bot.friends().search('your name')[0]
    group = bot.groups().search('group name')[0]
    # 传入接收者列表
    listen(bot, receivers=[my, group])

向 group 发送消息::

    from wechat_sender import Sender
    Sender('group name').send('hello')

.. note::

    | 关于接收者:
    | 当 :func:`listen` 传入 receivers 时会把第一个 receiver 当做默认接收者，所有未指定接收者的 :class:`Sender` 都将把消息发给默认接收者


使用 token 以防 sender 被滥用
------------------------------------------

.. warning::

    wechat_sender 基于 http 服务提供消息发送服务，如果部署在服务器上有潜在盗用风险，所以 :func:`listen` 初始化时务必传入 token 以防止盗用


.. warning::

    注意保证 token 安全，不要被泄漏

.. code:: python

    # 同样，基于 http 的服务需要一个端口与外部通信，listen 默认端口是 10245 ，你可以改成任何空闲端口，例如 8888
    listen(bot, receiver, token='your secret', port=8888)

.. note::

    如果传入了 token 或 port 请务必保证 :class:`Sender` 在初始化时也传入相同的 token 和 port


开启 wechat_sender 的状态报告
------------------------------------------

鉴于微信个人号接口的不稳定性，我们可以开启 wechat_sender 的状态报告，定时向 status_receiver 发送状态信息

.. code:: python

    listen(bot, my, token='your secret', status_report=True, status_receiver=my)

.. note::

    | 不指定 status_receiver 时状态报告将发送到默认接收者
    | 默认每隔一小时进行一次状态报告
