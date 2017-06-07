底层 API
==============

| wechat_sender 是基于 http 提供的服务，因此底层 API 也是基于 http 服务构建的。
| 所以非 Python 项目也可以使用 wechat_sender 进行信息发送，你只需要自己封装一个简单的 sender 即可

:func:`listen` 中设定的 port 与 wechat_sender 部署地址即为服务地址，默认: http://localhost:10245

ADDR = http://localhost:10245

返回码说明
-------------

+----------------+---------------------------+
| status结果码   | 状态                      |
+================+===========================+
| 0              | 成功                      |
+----------------+---------------------------+
| 1              | 权限不足(token 不正确)    |
+----------------+---------------------------+
| 2              | bot 故障                  |
+----------------+---------------------------+
| 3              | wechat\_sender 服务故障   |
+----------------+---------------------------+
| 4              | 未知错误                  |
+----------------+---------------------------+

发送普通消息
--------------

POST ADDR/message

参数
~~~~~~~~~~~~~~

:content: (必填|str) - 需要发送的消息
:token: (选填|str) - 令牌
:receiver: (选填|str) - 接收者名称

返回
~~~~~~~~~~~

.. code::

    {
      "status": 1,
      "message": "Token is missing"
    }
    or
    {
      "status": 0,
      "message": "Success"
    }

发送延时消息
--------------

POST ADDR/delay_message

参数
~~~~~~~~~~~~~~

:content: (必填|str) - 需要发送的消息
:title: (选填|str) - 消息标题
:time: (选填|str) - 消息时间, "XXXX-XX-XX XX:XX:XX" 形式
:remind: (选填|int) - 提醒时移，integer 表示的秒
:token: (选填|str) - 令牌
:receiver: (选填|str) - 接收者名称

返回
~~~~~~~~~~~

.. code::

    {
      "status": 1,
      "message": "Token is missing"
    }
    or
    {
      "status": 0,
      "message": "Success"
    }

发送周期消息
--------------

POST ADDR/periodic_message

参数
~~~~~~~~~~~~~~

:content: (必填|str) - 需要发送的消息
:title: (选填|str) - 消息标题
:interval: (选填|int) - 提醒周期，integer 表示的秒
:token: (选填|str) - 令牌
:receiver: (选填|str) - 接收者名称

返回
~~~~~~~~~~~

.. code::

    {
      "status": 1,
      "message": "Token is missing"
    }
    or
    {
      "status": 0,
      "message": "Success"
    }


发送定向消息
--------------

POST ADDR/send_to_message

参数
~~~~~~~~~~~~~~

:content: (必填|str) - 需要发送的消息
:search: (选填|str) - 好友搜索条件

返回
~~~~~~~~~~~~~~

.. code::

    {
      "status": 1,
      "message": "Token is missing"
    }
    or
    {
      "status": 0,
      "message": "Success"
    }
