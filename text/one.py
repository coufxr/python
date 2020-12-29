#!/usr/bin/env python
# encoding: utf-8
'''
@author: coufxr
@contact: mu993364@163.com
@file: one.py
@time: 2019/2/16 18:06
@desc:
'''

import time

# def con(name):]'
#         baozi = yield
#         print("%s个大包子，塞给%s吃!!" % (baozi, name))


# def pro(name):
#     c = con(name);
#     c.__next__()
#     print("我开始做包子了！！")
#     for i in range(1, 10):
#         time.sleep(1)
#         c.send(i)


# # pro("赵渝")
# # pro("范晨")
# def sc(dx):
#     for i in range(1, dx):
#         # print(i)
#         if i % 2 == 0:
#             print(i)
#             continue


# # str = input("请输入")  # 字符串格式
# print(str)
# # sc(int(str))


def shengfa():
    for i in range(1, 10):  # 左下角
        for j in range(1, i+1):
            print("%s*%s=%s " % (i, j, i * j), end=" ")  # end:语句执行完后显示的东西
        print(" ")
    for i in range(1, 10):  # 右下角
        for k in range(1, 10 - i):
            print(end="       ")
        for j in range(1, i + 1):
            print("%s*%s=%s" % (i, j, i * j), end=" ")
        print("")


if __name__ == "__main__":
    shengfa()
