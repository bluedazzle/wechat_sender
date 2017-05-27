# Wechat_Sender

随时随地发送消息到微信

## 简介

wechat_sender 是基于 [wxpy][1] 和 [tornado][2] 实现的一个可以将你的网站、爬虫、脚本等其他应用中各种消息 （日志、报警、运行结果等） 发给到微信的工具

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

之后如果你想在其他程序或脚本中发送微信消息，只需要：

```python
# coding: utf-8
from wechat_sender import Sender
Sender().send("test message")
```

## API

### **wechat_sender.listen(bot, receiver=None, token=None, port=10245, status_report=False, status_receiver=None,
           status_interval=60 * 60 * 1000)**

#### **参数**
* bot(_必填_|Bot对象)-wxpy 的 Bot 对象实例
* receivers(_可选_|Chat 对象|Chat 对象列表)-消息接收者，wxpy 的 Chat 对象实例, 或 Chat 对象列表，如果为 list 第一个 Chat 为默认接收者。如果为 Chat 对象，则默认接收者也是此对象。 不填为当前 bot 对象的文件接收者
* token(_可选_|string)- 信令，防止 receiver 被非法滥用，建议加上 token 防止非法使用，如果使用 token 请在 send 时也使用统一 token，否则无法发送。token 建议为 32 位及以上的无规律字符串
* port(_可选_|integer)- 监听端口, 监听端口默认为 10245 ，如有冲突或特殊需要请自行指定，需要和 send 处统一
* status_report(_可选_|bool)- 是否开启状态报告，如果开启，wechat_sender 将会定时发送状态信息到 status_receiver
* status_receiver(_可选_|Chat 对象)- 指定 status_receiver，不填将会发送状态消息给默认接收者
* status_interval(_可选_|integer|datetime.timedelta)- 指定状态报告发送间隔时间，为 integer 时代表毫秒



### **class wechat_sender.Sender(token=None, host="http://localhost", port=10245)**

#### **属性**
* token(_可选_|str)-信令，如果不为空请保持和 listen 中的 token 一致
* host(_可选_|str)-远程地址，本地调用不用填
* port(_可选_|integer)-发送端口，如果不为空请保持和 listen 中的 port 一致

#### **方法**

### **send(self, content)**

#### **参数**
* content(_必填_|string)-需要发送的消息内容，目前只支持文本消息

### **delay_send(self, content, time, title='', remind=3600)**

#### **参数**
* content(_必填_|string)-需要发送的消息内容，目前只支持文本消息
* time(_必填_|string or datetime)-发送消息的开始时间，支持 datetime.date、datetime.datetime 格式或者如 '2017-05-21 10:00:00' 的字符串
* title(_可选_|string)-需要发送的消息标题
* remind(_可选_|integer or datetime.timedelta)-消息提醒时移，默认 1 小时，即早于 time 值 1 小时发送消息提醒, 支持 integer（毫秒） 或 datetime.timedelta

### **periodic_send(self, content, interval, title='')**

#### **参数**
* content(_必填_|string)-需要发送的消息内容，目前只支持文本消息
* interval(_必填_|integer or datetime.timedelta)-发送消息间隔时间，支持 datetime.timedelta 或 integer 表示的秒数
* title(_可选_|string)-需要发送的消息标题

### **send_to(self, content, search)**

#### **参数**
* content(_必填_|string)-需要发送的消息内容，目前只支持文本消息
* search(_必填_|str|dict|list)-搜索对象，同 wxpy.chats.search 使用方法一样。例如，可以使用字符串进行搜索好友，或指定具体属性搜索，如 puid=xxx 的字典

## wechat_sender 微信命令

通过给指定的 receiver 发送一些 wechat_sender 支持的命令可以获取 wechat_sender 的一些信息：

目前支持：

### 获取 wxpy 运行状态：向 receiver 发送 `@wss`

命令返回：

```
[当前时间] 22:35:05
[运行时间] 0:00:27
[内存占用] 33.00 MB
[发送消息] 10
```

### 获取 wechat_sender 延时与周期消息： 向 receiver 发送 `@wsr`

命令返回：

```
当前已注册延时消息共有1条
[ID (序号) ]：D0
[发送时间]：2017-05-27 10:00:00
[消息时间]：2017-05-27 11:00:00
[消息标题]：延迟消息测试

当前已注册周期消息共有1条
[ID (序号) ]：P0
[运行状态]：已激活
[发送周期]：10s
[消息标题]：周期消息测试test
```

## TODO LIST

- [x] 多 receiver
- [ ] wxpy 掉线邮件通知
- [ ] wxpy 掉线重连

## 历史

**当前版本： 0.1.1**

2017.05.27 0.1.1:

增加多 receiver 支持;

2017.05.27 0.1.0:

增加延时消息；

增加周期消息；

增加指定接收方消息；

增加 wechat_sender 控制命令;

增加 wxpy 状态监测功能；

优化代码；

2017.05.17 0.0.2:

优化代码

2017.05.11 0.0.1:

发布初版





[1]:https://github.com/youfou/wxpy
[2]:https://github.com/tornadoweb/tornado
