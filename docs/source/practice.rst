最佳实践
===========

在服务器 XXX.XXX.XXX.XXX 部署 wechat_sender 服务::

    from wxpy import *
    from wechat_sender import *

    bot = Bot('bot.pkl', console_qr=True)
    bot.enable_puid()
    master = ensure_one(bot.friends().search(puid='xxxx'))
    log_group = ensure_one(bot.groups().search(puid='xxxxxx'))
    other = ensure_one(bot.friends().search('xxxxxx'))
    token = 'xxxxxxxxxxxxxxxxxxxxx'
    listen(bot, [master, other, log_group], token=token, port=9090, status_report=True, status_receiver=log_group)


在其他地方进行消息发送::

    from wechat_sender import Sender
    host = 'XXX.XXX.XXX.XXX'
    token = 'xxxxxxxxxxxxxxxxxxxxx'
    sender = Sender(token=token, receiver='xxx', host=host, port='9090')


在其他应用中加入 wechat_sender logging handler::

    # 假如这是你另一台服务器上的脚本
    # spider.py

    import logging
    from wechat_sender import LoggingSenderHandler

    logger = logging.getLogger(__name__)

    # spider code here
    def test_spider():
        ...
        logger.exception("EXCEPTION: XXX")

    def init_logger():
        token = 'xxxxxxxxxxxxxxxxxxxxx'
        sender_logger = LoggingSenderHandler('spider', token=token, port=9090, host='XXX.XXX.XXX.XXX', receiver='xxx', level=logging.EXCEPTION)
        logger.addHandler(sender_logger)

    if __name__ == '__main__':
        init_logger()
        test_spider()

只需要在原有 logger 中加入 wechat_sender 的 log handler 即可实现把日志发送到微信