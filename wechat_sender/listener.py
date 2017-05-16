# coding: utf-8
from __future__ import unicode_literals

import os
import tornado.web
from tornado.options import define, options

from objects import WxBot
from wechat_sender.utils import StatusWrapperMixin, STATUS_BOT_EXCEPTION, STATUS_PERMISSION_DENIED

wxbot = None


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


def listen(bot, receiver=None, token=None, port=10245):
    global wxbot
    tornado.options.parse_command_line()
    app = Application()
    wxbot = WxBot(bot, receiver, token)
    define("port", default=port, help="run on the given port", type=int)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
