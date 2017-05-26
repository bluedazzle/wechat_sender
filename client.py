# coding: utf-8
from __future__ import unicode_literals

import datetime

from wechat_sender import Sender
import requests

# print delay_send('tce服务运维交流', '邀请建磊给大家讲一下tce一些运维的操作。\n中航矮楼-F2-09 (14) Zoom - 能量桶', '2017-05-23 16:00:00',
#                  token='test', host='http://114.215.153.187')
sender = Sender('test')
# print sender.delay_send('延迟消息测试', time='2017-05-26 11:00:00')
# print sender.periodic_send('周期消息测试test', 10)

# print sender.send_to('test send to', {"puid": 'ffb83a71'})
# from UserDict import UserDict
# import os
# import time
# import datetime
# import psutil
# import logging
# import tornado.web
# from tornado.options import define, options
#
#
# class Application(tornado.web.Application):
#     def __init__(self):
#         handlers = [
#             (r"/message", MessageHandle),
#         ]
#         settings = dict(
#             static_path=os.path.join(os.path.dirname(__file__), "static"),
#         )
#         super(Application, self).__init__(handlers, **settings)
#
#
# class MessageHandle(tornado.web.RequestHandler):
#     def __init__(self, application, request, *args, **kwargs):
#         self.ioloop = tornado.ioloop.IOLoop.instance()
#         super(MessageHandle, self).__init__(application, request, *args, **kwargs)
#
#     def get(self, *args, **kwargs):
#         tornado.ioloop.PeriodicCallback(self.tp, 10000).start()
#         # print self.ioloop.__dict__
#         print self.ioloop._timeouts[0]
#         self.write('success')
#
#     def tp(self):
#         print 'get tp'
#
#
# def test_periodic():
#     print 'tp'
#
#
# # tornado.options.parse_command_line()
# # app = Application()
# # process = psutil.Process()
# # app.listen(8888)
# # tornado.ioloop.PeriodicCallback(test_periodic, 10000).start()
# # tornado.ioloop.IOLoop.current().start()
#
# def foo(a, b):
#     print '{0}{1}'.format(a, b)
#
# import functools
# dd = functools.partial(foo, 1, 2, 3)
# print dd.args, dd.func, dd.keywords
# print dd()
#
