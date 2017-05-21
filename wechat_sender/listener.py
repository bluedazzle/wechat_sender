# coding: utf-8
from __future__ import unicode_literals

import os
import time
import datetime
import psutil
import logging
import tornado.web
from tornado.options import define, options

from objects import WxBot
from wechat_sender.utils import StatusWrapperMixin, STATUS_BOT_EXCEPTION, STATUS_PERMISSION_DENIED, \
    STATUS_TORNADO_EXCEPTION, DEFAULT_REMIND_TIME, STATUS_ERROR, DEFAULT_REPORT_TIME

wxbot = None
process = None


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/message", MessageHandle),
            (r"/delay_message", DelayMessageHandle),
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
                print e
                self.status_code = STATUS_BOT_EXCEPTION
                self.write(e)


class DelayMessageHandle(StatusWrapperMixin, tornado.web.RequestHandler):
    def __init__(self, application, request, *args, **kwargs):
        self.ioloop = tornado.ioloop.IOLoop.instance()
        super(DelayMessageHandle, self).__init__(application, request, *args, **kwargs)

    def post(self, *args, **kwargs):
        content = self.get_argument('content', '')
        title = self.get_argument('title', '')
        task_time = self.get_argument('time', None)
        remind = int(self.get_argument('remind', DEFAULT_REMIND_TIME))
        token = self.get_argument('token', None)
        if wxbot.token:
            if wxbot.token != token:
                self.status_code = STATUS_PERMISSION_DENIED
                self.write('Token is missing')
                return
        if task_time:
            try:
                timestamp = time.mktime(
                    (datetime.datetime.strptime(task_time, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(
                        seconds=remind)).timetuple())
            except ValueError as e:
                self.status_code = STATUS_ERROR
                self.write(e)
                return
        else:
            task_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        try:
            self.ioloop.call_at(timestamp, self.delay_task, title, content, task_time)
            self.write('Success')
        except Exception as e:
            self.status_code = STATUS_TORNADO_EXCEPTION
            self.write(e)

    @staticmethod
    def delay_task(title, content, task_time):
        msg = '标题：{title}\n时间：{time}\n详情：{content}'.format(title=title, time=task_time, content=content)
        # try:
        wxbot.send_msg(msg)
        logging.info('Send delay message {0} at {1:%Y-%m-%d %H:%M:%S}'.format(msg, datetime.datetime.now()))
        # except Exception as e:


def check_bot():
    if wxbot.bot.alive:
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(process.create_time())
        memory_usage = process.memory_info().rss
        msg = '[当前时间] {now:%H:%M:%S}\n[运行时间] {uptime}\n[内存占用] {memory}\n[发送消息] {messages}'.format(
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
    tornado.ioloop.PeriodicCallback(check_bot, DEFAULT_REPORT_TIME).start()
    tornado.ioloop.IOLoop.current().start()
