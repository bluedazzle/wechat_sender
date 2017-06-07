Wechat Sender 的控制命令
===============================

我们向 wechat_sender 发送支持的命令来获取 wechat_sender 的信息

.. note::

    wechat_sender 只会响应 default_recevier 的命令

.. note::

    | 关于 default_recevier:
    | 当 :func:`listen` 传入 receivers 时会把第一个 receiver 当做 default_recevier
    | 所有未指定接收者的 :class:`Sender` 都将把消息发给默认接收者

获取运行状态信息
---------------------

@wss
^^^^^^^^^^^

使用 listen 中绑定的 default_receiver 向 wecaht_sender 发送 @wss 即可返回当前运行状态::

    #[当前时间] 09:22:41
    #[运行时间] 1 day, 13:33:47
    #[内存占用] 28.00 MB
    #[发送消息] 67


获取已注册的延时\周期消息
-------------------------------

@wsr
^^^^^^^^^^

使用 listen 中绑定的 default_receiver 向 wecaht_sender 发送 @wsr 即可返回已注册的延时\周期消息::

    #当前已注册延时消息共有1条
    #[ID (序号) ]：D0
    #[消息接收]：rapospectre
    #[发送时间]：2017-06-07 11:57:16
    #[消息时间]：2017-06-07 12:56:16
    #[消息标题]：延迟消息测试

    #当前已注册周期消息共有0条

