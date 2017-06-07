# coding: utf-8
from __future__ import unicode_literals
import codecs

STATUS_SUCCESS = 0
STATUS_PERMISSION_DENIED = 1
STATUS_BOT_EXCEPTION = 2
STATUS_TORNADO_EXCEPTION = 3
STATUS_ERROR = 4

DEFAULT_REMIND_TIME = 60 * 60
DEFAULT_REPORT_TIME = 60 * 60 * 1000

DELAY_TASK = 'DELAY_TASK'
PERIODIC_TASK = 'PERIODIC_TASK'
SYSTEM_TASK = 'SYSTEM_TASK'

MESSAGE_REPORT_COMMAND = '@wsr'
MESSAGE_STATUS_COMMAND = '@wss'


def _read_config_list():
    """
    配置列表读取
    """
    with codecs.open('conf.ini', 'w+', encoding='utf-8') as f1:
        conf_list = [conf for conf in f1.read().split('\n') if conf != '']
        return conf_list


def write_config(name, value):
    """
    配置写入
    """
    name = name.lower()
    new = True
    conf_list = _read_config_list()
    for i, conf in enumerate(conf_list):
        if conf.startswith(name):
            conf_list[i] = '{0}={1}'.format(name, value)
            new = False
            break
    if new:
        conf_list.append('{0}={1}'.format(name, value))

    with codecs.open('conf.ini', 'w+', encoding='utf-8') as f1:
        for conf in conf_list:
            f1.write(conf + '\n')
    return True


def read_config(name):
    """
    配置读取
    """
    name = name.lower()
    conf_list = _read_config_list()
    for conf in conf_list:
        if conf.startswith(name):
            return conf.split('=')[1].split('#')[0].strip()
    return None


class StatusWrapperMixin(object):
    """
    返回状态码 Mixin
    """
    status_code = STATUS_SUCCESS
    status_message = ''

    def write(self, chunk):
        context = {'status': self.status_code,
                   'message': chunk}
        super(StatusWrapperMixin, self).write(context)
