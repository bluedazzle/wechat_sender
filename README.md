# Wechat_Sender

将程序运行结果及报警信息通过微信发送给你自己

## 简介

wechat_sender 是基于 [wxpy][1] 和 [tornado][2] 实现的一个可以将你的网站、爬虫、脚本等其他应用中各种消息 （日志、报警、运行结果等） 发给你的个人微信的工具

## 初衷

wxpy 基于 itchat 提供了较为完备的微信个人号 API ，而我想使用个人微信来接收我的网站的报警信息以及一些爬虫的结果，因此我写了这个工具。

## 安装

```python
pip install wechat_sender
```

## 运行环境

Python 2.7 及以上
Python 3 及以上

## 使用

如果你是 wxpy 的使用者，只需更改一句即可使用 wechat_sender：

例如这是你本来的代码：

```python
# coding: utf-8
from __future__ import unicode_literals

from wxpy import *
bot = Bot('bot.pkl')

my_friend = bot.friends().search('xxx')[0]

my_friend.send('Hello WeChat!')

@bot.register(Friend)
def reply_test(msg):
    msg.reply('test')

bot.join()
```

使用 wechat_sender：

```python
# coding: utf-8
from __future__ import unicode_literals

from wxpy import *
from wechat_sender import listen
bot = Bot('bot.pkl')

my_friend = bot.friends().search('xxx')[0]

my_friend.send('Hello WeChat!')

@bot.register(Friend)
def reply_test(msg):
    msg.reply('test')

listen(bot) # 只需改变最后一行代码
```

之后如果你想在其他地方发送微信消息给你自己，只需要：

```python
# coding: utf-8
from wechat_sender import send
send("test message")
```

## API

#### **wechat_sender.listen(bot, receiver, token, port)**

### **参数**
* bot(_必填_|Bot对象)-wxpy 的 Bot 对象实例
* receiver(_可选_|Chat 对象)-接收消息，wxpy 的 Chat 对象实例, 不填为当前 bot 对象的文件接收者
* token(_可选_|string)- 信令，防止 receiver 被非法滥用，建议加上 token 防止非法使用，如果使用 token 请在 send 时也使用统一 token，否则无法发送。token 建议为 32 位及以上的无规律字符串
* port(_可选_|integer)- 监听端口, 监听端口默认为 10245 ，如有冲突或特殊需要请自行指定，需要和 send 处统一


#### **wechat_sender.send(message, token, port)**

### **参数**
* message(_必填_|string)-需要发送的消息，目前只支持文本消息
* token(_可选_|string)-信令，如果不为空请保持和 listen 中的 token 一致
* port(_可选_|integer)-发送端口，如果不为空请保持和 listen 中的 port 一致

#### **wechat_sender.delay_send(title, content, time, remind, token, port)**

### **参数**
* title(_必填_|string)-需要发送的消息标题，目前只支持文本消息
* content(_必填_|string)-需要发送的消息内容，目前只支持文本消息
* time(_必填_|string or datetime)-发送消息的开始时间，支持 datetime.date、datetime.datetime 格式或者如 '2017-05-21 10:00:00' 的字符串
* remind(_可选_|integer or datetime.timedelta)-消息提醒时移，默认 1 小时，即早于 time 值 1 小时发送消息提醒, 支持 integer（毫秒） 或 datetime.timedelta
* token(_可选_|string)-信令，如果不为空请保持和 listen 中的 token 一致
* port(_可选_|integer)-发送端口，如果不为空请保持和 listen 中的 port 一致


## TODO LIST

- [ ] wxpy 掉线邮件通知
- [ ] wxpy 掉线重连

## 历史

**当前版本： 0.0.2**

2017.05.17 0.0.2:

优化代码

2017.05.11 0.0.1:

发布初版





[1]:https://github.com/youfou/wxpy
[2]:https://github.com/tornadoweb/tornado
