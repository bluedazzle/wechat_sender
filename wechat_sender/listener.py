# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import copy
import functools
import json
import os
import time
import datetime
import psutil
import logging

import sys
import tornado.web

from wechat_sender.objects import WxBot, Message, Global
from wechat_sender.utils import StatusWrapperMixin, STATUS_BOT_EXCEPTION, STATUS_PERMISSION_DENIED, \
    STATUS_TORNADO_EXCEPTION, DEFAULT_REMIND_TIME, STATUS_ERROR, DEFAULT_REPORT_TIME, DELAY_TASK, PERIODIC_TASK, \
    MESSAGE_REPORT_COMMAND, SYSTEM_TASK, MESSAGE_STATUS_COMMAND

glb = None
_logger = logging.getLogger(__name__)


class Application(tornado.web.Application):
    """
    tornado app 初始化
    """

    def __init__(self):
        handlers = [
            (r"/message", MessageHandle),
            (r"/delay_message", DelayMessageHandle),
            (r"/periodic_message", PeriodicMessageHandle),
            (r"/send_to_message", UserMessageHandle),
        ]
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        super(Application, self).__init__(handlers, **settings)


class MessageHandle(StatusWrapperMixin, tornado.web.RequestHandler):
    """
    普通消息处理 handle
    """

    def post(self, *args, **kwargs):
        message = self.get_argument('content', None)
        token = self.get_argument('token', None)
        receivers = self.get_argument('receivers', None)
        if not message:
            self.status_code = STATUS_ERROR
            self.write('Content is required')
            return

        if glb.token:
            if glb.token != token:
                self.status_code = STATUS_PERMISSION_DENIED
                self.write('Token is missing')
                return
        try:
            msg = Message(message, receivers=receivers)
            glb.wxbot.send_msg(msg)
            self.write('Success')
        except Exception as e:
            _logger.exception(e)
            self.status_code = STATUS_BOT_EXCEPTION
            self.write(e.message)


class DelayMessageHandle(StatusWrapperMixin, tornado.web.RequestHandler):
    """
    延时消息处理 handle
    """

    def __init__(self, application, request, *args, **kwargs):
        self.ioloop = tornado.ioloop.IOLoop.instance()
        super(DelayMessageHandle, self).__init__(application, request, *args, **kwargs)

    def post(self, *args, **kwargs):
        content = self.get_argument('content', '')
        title = self.get_argument('title', '')
        task_time = self.get_argument('time', None)
        remind = int(self.get_argument('remind', DEFAULT_REMIND_TIME))
        token = self.get_argument('token', None)
        receivers = self.get_argument('receivers', None)

        if glb.token:
            if glb.token != token:
                self.status_code = STATUS_PERMISSION_DENIED
                self.write('Token is missing')
                return
        if task_time:
            try:
                task_time = datetime.datetime.strptime(task_time, '%Y-%m-%d %H:%M:%S')
                timestamp = time.mktime(
                    (task_time - datetime.timedelta(
                        seconds=remind)).timetuple())
            except ValueError as e:
                self.status_code = STATUS_ERROR
                self.write(e.message)
                _logger.exception(e)
                return
        else:
            task_time = datetime.datetime.now()
            timestamp = int(time.mktime(task_time.timetuple()))
        try:
            message = Message(content, title, task_time, datetime.timedelta(seconds=remind), receivers=receivers)
            self.ioloop.call_at(timestamp, self.delay_task, DELAY_TASK, message)
            self.write('Success')
        except Exception as e:
            self.status_code = STATUS_TORNADO_EXCEPTION
            self.write(e.message)
            _logger.exception(e)

    @staticmethod
    def delay_task(task_type, message):
        # try:
        glb.wxbot.send_msg(message)
        _logger.info(
            '{0} Send delay message {1} at {2:%Y-%m-%d %H:%M:%S}'.format(task_type, message, datetime.datetime.now()))
        # except Exception as e:


class PeriodicMessageHandle(StatusWrapperMixin, tornado.web.RequestHandler):
    """
    周期消息处理 handle
    """

    def __init__(self, application, request, *args, **kwargs):
        self.ioloop = tornado.ioloop.IOLoop.instance()
        super(PeriodicMessageHandle, self).__init__(application, request, *args, **kwargs)

    def post(self, *args, **kwargs):
        content = self.get_argument('content', '')
        title = self.get_argument('title', '')
        interval = self.get_argument('interval', None)
        token = self.get_argument('token', None)
        receivers = self.get_argument('receivers', None)

        if glb.token:
            if glb.token != token:
                self.status_code = STATUS_PERMISSION_DENIED
                self.write('Token is missing')
                return
        if not interval:
            self.status_code = STATUS_ERROR
            self.write('interval is required')
            return
        try:
            interval = int(interval)
        except Exception as e:
            self.status_code = STATUS_ERROR
            self.write('interval must be a integer')
        try:
            message = Message(content, title=title, interval=datetime.timedelta(seconds=interval), receivers=receivers)
            user_periodic = tornado.ioloop.PeriodicCallback(
                functools.partial(self.periodic_task, PERIODIC_TASK, message),
                interval * 1000, self.ioloop)
            glb.periodic_list.append(user_periodic)
            user_periodic.start()
            self.write('Success')
        except Exception as e:
            self.status_code = STATUS_TORNADO_EXCEPTION
            self.write(e.message)
            _logger.exception(e)

    @staticmethod
    def periodic_task(task_type, message):
        glb.wxbot.send_msg(message)
        _logger.info('{0} Send periodic message {1} at {2:%Y-%m-%d %H:%M:%S}'.format(task_type, message,
                                                                                     datetime.datetime.now()))


class UserMessageHandle(StatusWrapperMixin, tornado.web.RequestHandler):
    """
    指定消息接收处理 handle
    """

    def post(self, *args, **kwargs):
        from wxpy import ensure_one

        content = self.get_argument('content', '')
        search = self.get_argument('search', '')
        token = self.get_argument('token', None)
        default_receiver = self.get_argument('receivers', None)

        if glb.token:
            if glb.token != token:
                self.status_code = STATUS_PERMISSION_DENIED
                self.write('Token is missing')
                return
        try:
            search = json.loads(search)
        except ValueError:
            search = search
        try:
            if isinstance(search, dict):
                receiver = ensure_one(glb.wxbot.bot.search(**search))
            else:
                receiver = ensure_one(glb.wxbot.bot.search(search))
        except ValueError:
            receiver = None
        if receiver:
            receiver.send_msg(content)
        else:
            msg = '消息发送失败，没有找到接收者。\n[搜索条件]: {0}\n[消息内容]：{1}'.format(search, content)
            message = Message(msg, receivers=default_receiver)
            glb.wxbot.send_msg(message)
            _logger.info(msg)
        self.write('Success')


def generate_run_info():
    """
    获取当前运行状态
    """
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(glb.run_info.create_time())
    memory_usage = glb.run_info.memory_info().rss
    msg = '[当前时间] {now:%H:%M:%S}\n[运行时间] {uptime}\n[内存占用] {memory}\n[发送消息] {messages}'.format(
        now=datetime.datetime.now(),
        uptime=str(uptime).split('.')[0],
        memory='{:.2f} MB'.format(memory_usage / 1024 ** 2),
        messages=len(glb.wxbot.bot.messages)
    )
    return msg


def check_bot(task_type=SYSTEM_TASK):
    """
    wxpy bot 健康检查任务
    """
    if glb.wxbot.bot.alive:
        msg = generate_run_info()
        message = Message(content=msg, receivers='status')
        glb.wxbot.send_msg(message)
        _logger.info(
            '{0} Send status message {1} at {2:%Y-%m-%d %H:%M:%S}'.format(task_type, msg, datetime.datetime.now()))
    else:
        # todo
        pass


def timeout_message_report():
    """
    周期/延时 消息报告
    """
    timeout_list = glb.ioloop._timeouts
    delay_task = []
    for timeout in timeout_list:
        if not timeout.callback:
            continue
        if len(timeout.callback.args) == 2:
            task_type, message = timeout.callback.args
            delay_task.append(message)
    msg = '当前已注册延时消息共有{0}条'.format(len(delay_task))
    for i, itm in enumerate(delay_task):
        msg = '{pre}\n[ID (序号) ]：D{index}\n[消息接收]：{receiver}\n[发送时间]：{remind}\n[消息时间]：{time}\n[消息标题]：{message}\n'.format(
            pre=msg, index=i, remind=itm.remind, time=itm.time, message=itm.title or itm.content, receiver=itm.receiver)
    interval_task = [(periodic.callback.args[1], periodic.is_running()) for periodic in glb.periodic_list if
                     len(periodic.callback.args) == 2 and periodic.callback.args[0] == PERIODIC_TASK]
    msg = '{0}\n当前已注册周期消息共有{1}条'.format(msg, len(interval_task))
    for i, itm in enumerate(interval_task):
        msg = '{pre}\n[ID (序号) ]：P{index}\n[消息接收]：{receiver}\n[运行状态]：{status}\n[发送周期]：{interval}\n[消息标题]：{message}\n'.format(
            pre=msg, index=i, interval=itm[0].interval, status='已激活' if itm[1] else '未激活',
            message=itm[0].title or itm[0].content, receiver=itm[0].receiver)
    return msg


def register_listener_handle(wxbot):
    """
    wechat_sender 向 wxpy 注册控制消息 handler
    """
    from wxpy import TEXT

    @wxbot.bot.register(wxbot.default_receiver, TEXT, except_self=False)
    def sender_command_handle(msg):
        command_dict = {MESSAGE_REPORT_COMMAND: timeout_message_report(),
                        MESSAGE_STATUS_COMMAND: generate_run_info()}
        message = command_dict.get(msg.text, None)
        if message:
            return message
        myself = wxbot.bot.registered.get_config(msg)
        registered_copy = copy.copy(wxbot.bot.registered)
        registered_copy.remove(myself)
        pre_conf = registered_copy.get_config(msg)
        if pre_conf:
            my_name = sys._getframe().f_code.co_name
            if my_name != pre_conf.func.__name__:
                pre_conf.func(msg)


def listen(bot, receivers=None, token=None, port=10245, status_report=False, status_receiver=None,
           status_interval=DEFAULT_REPORT_TIME):
    """
    传入 bot 实例并启动 wechat_sender 服务

    :param bot: (必填|Bot对象) - wxpy 的 Bot 对象实例
    :param receivers: (选填|wxpy.Chat 对象|Chat 对象列表) - 消息接收者，wxpy 的 Chat 对象实例, 或 Chat 对象列表，如果为 list 第一个 Chat 为默认接收者。如果为 Chat 对象，则默认接收者也是此对象。 不填为当前 bot 对象的文件接收者
    :param token: (选填|str) - 信令，防止 receiver 被非法滥用，建议加上 token 防止非法使用，如果使用 token 请在初始化 `Sender()` 时也使用统一 token，否则无法发送。token 建议为 32 位及以上的无规律字符串
    :param port: (选填|int) - 监听端口, 监听端口默认为 10245 ，如有冲突或特殊需要请自行指定，需要和 `Sender()` 统一
    :param status_report: (选填|bool) - 是否开启状态报告，如果开启，wechat_sender 将会定时发送状态信息到 status_receiver
    :param status_receiver: (选填|Chat 对象) - 指定 status_receiver，不填将会发送状态消息给默认接收者
    :param status_interval: (选填|int|datetime.timedelta) - 指定状态报告发送间隔时间，为 integer 时代表毫秒

    """
    global glb
    periodic_list = []
    app = Application()
    wxbot = WxBot(bot, receivers, status_receiver)
    register_listener_handle(wxbot)
    process = psutil.Process()
    app.listen(port)

    if status_report:
        if isinstance(status_interval, datetime.timedelta):
            status_interval = status_interval.seconds * 1000
        check_periodic = tornado.ioloop.PeriodicCallback(functools.partial(check_bot, SYSTEM_TASK), status_interval)
        check_periodic.start()
        periodic_list.append(check_periodic)

    glb = Global(wxbot=wxbot, run_info=process, periodic_list=periodic_list, ioloop=tornado.ioloop.IOLoop.instance(),
                 token=token)
    tornado.ioloop.IOLoop.current().start()
