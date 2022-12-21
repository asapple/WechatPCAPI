# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 14:00
# @Author  : Leon
# @Email   : 1446684220@qq.com
# @File    : test.py
# @Desc    :
# @Software: PyCharm

import os
from WechatPCAPI import WechatPCAPI
import time
wx_inst = None

# 接收消息的回调函数，可自行定义


def on_message(message):
    print(message)
    if isNeededInfo(message) and isAbnormalInfo(message):
        handleFunc(message)
    return

# 判断此消息是否需要留意


def isNeededInfo(message):
    if 'data' in message and 'from_chatroom_wxid' in message['data']:
        return 1
    else:
        return 0

# 判断此消息是否是炸群信息


def isAbnormalInfo(message):
    if message['data']['msg'] == '他们是托':
        return 1
    else:
        return 0

# 异常信息出现时的处理函数


def handleFunc(message):
    global wx_inst
    wx_inst.send_text(to_user='filehelper', msg=message['data']['time'] +
                      ':' + message['data']['from_chatroom_nickname'] + message['data']['msg'])
    return


def main():
    # 初始化wx实例
    global wx_inst
    wx_inst = WechatPCAPI(on_message=on_message)

    # 启动微信 目前仅支持微信V2.7.1.82
    wx_inst.start_wechat(block=True)

    # 等待登陆成功，此时需要人为扫码登录微信
    while not wx_inst.get_myself():
        time.sleep(5)

    # 登录成功了
    print(wx_inst.get_myself())
    time.sleep(10)
    # 更新所有好友信息，数据会通过上面的回调函数返回
    wx_inst.update_frinds()


if __name__ == '__main__':
    main()
