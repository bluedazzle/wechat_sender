# coding: utf-8
from __future__ import unicode_literals

import os

import datetime
import psutil
import tornado.web
from tornado.options import define, options

from objects import WxBot
from wechat_sender.utils import StatusWrapperMixin, STATUS_BOT_EXCEPTION, STATUS_PERMISSION_DENIED

wxbot = None
process = None


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/message", MessageHandle),
        ]
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        super(Application, self).__init__(handlers, **settings)


class MessageHandle(StatusWrapperMixin, tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        message = self.get_argument('content', None)
        token = self.get_argument('token', None)
        if message:
            if wxbot.token:
                if wxbot.token != token:
                    self.status_code = STATUS_PERMISSION_DENIED
                    self.write('Token is missing')
                    return
            try:
                wxbot.send_msg(message)
                self.write('Success')
            except Exception as e:
                self.status_code = STATUS_BOT_EXCEPTION
                self.write(e)


def check_bot():
    if wxbot.bot.alive:
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(process.create_time())
        memory_usage = process.memory_info().rss
        msg = '[now] {now:%H:%M:%S}\n[uptime] {uptime}\n[memory] {memory}\n[messages] {messages}'.format(
            now=datetime.datetime.now(),
            uptime=str(uptime).split('.')[0],
            memory='{:.2f} MB'.format(memory_usage / 1024 ** 2),
            messages=len(wxbot.bot.messages)
        )
        wxbot.send_msg(msg)
    else:
        # todo
        pass


def listen(bot, receiver=None, token=None, port=10245):
    global wxbot, process
    tornado.options.parse_command_line()
    app = Application()
    wxbot = WxBot(bot, receiver, token)
    process = psutil.Process()
    define("port", default=port, help="run on the given port", type=int)
    app.listen(options.port)
    tornado.ioloop.PeriodicCallback(check_bot, 10000).start()
    tornado.ioloop.IOLoop.current().start()
