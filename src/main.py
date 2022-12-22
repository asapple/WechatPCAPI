# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 14:00
# @Author  : Leon
# @Email   : 1446684220@qq.com
# @File    : test.py
# @Desc    :
# @Software: PyCharm

import codecs

import keyboard
from WechatPCAPI import WechatPCAPI
import time
wx_inst = None
friendsInfo = ''
banword_list = []

# 接收消息的回调函数，可自行定义


def on_message(message):
    # global friendsInfo
    # friendsInfo += str(message) + '\n'
    print(message)
    if isNeededInfo(message) and check_for_banned_words(message['data']['msg']):
        handleFunc(message)
    return

# 判断此消息是否需要留意


def isNeededInfo(message):
    if 'data' in message and 'from_chatroom_wxid' in message['data'] and 'from_member_wxid' in message['data'] and message['data']['from_member_wxid']:
        return 1
    else:
        return 0

# 异常信息出现时的处理函数


def handleFunc(message):
    global wx_inst
    send_msg = '云捷巡警-异常消息提醒：' + '\n'\
        '群聊：' + message['data']['from_chatroom_nickname'] + '\n' + \
        '用户：' + message['data']['from_member_wxid'] + '\n' + \
        '发送消息：' + message['data']['msg']
    wx_inst.send_text(to_user='18534946954@chatroom', msg=send_msg)
    # wx_inst.send_text(to_user='filehelper', msg=send_msg)
    return


def check_for_banned_words(msg):
    # Iterate through banword_list and check if msg contains any of the banned words
    for word in banword_list:
        if word in msg:
            return True
    # If none of the banned words are found, return False
    return False


def update_banned_word_list():
    banwords = ''
    global banword_list
    with codecs.open('banWord.txt', 'r', encoding='utf-8') as f:
        banwords = f.read()
    # Split banwords string into a list
    banword_list = banwords.split('/')
    print("完成更新违禁表！")


def main():
    update_banned_word_list()
    keyboard.add_hotkey('ctrl+shift+b', update_banned_word_list)
    # 初始化wx实例
    global wx_inst
    wx_inst = WechatPCAPI(on_message=on_message)
    # wx_inst = WechatPCAPI(on_message=None)
    # 启动微信 目前仅支持微信V2.7.1.82
    wx_inst.start_wechat(block=True)

    # 等待登陆成功，此时需要人为扫码登录微信
    while not wx_inst.get_myself():
        time.sleep(5)

    # 登录成功了
    # print(wx_inst.get_myself())
    # 更新所有好友信息，数据会通过上面的回调函数返回
    time.sleep(10)
    wx_inst.update_frinds()
    # global friendsInfo
    # with codecs.open('friends.txt', 'w', encoding='utf-8') as f:
    #     # 将字符串写入文件
    #     f.write(friendsInfo)


if __name__ == '__main__':
    main()
