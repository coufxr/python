#!/usr/bin/env python
# encoding: utf-8
'''
@author: coufxr
@contact: mu993364@163.com
@file: muen_3.py
@time: 2019/5/23 14:22
@desc:
'''
city = {"北京市": {"朝阳区": {"望京", "大山子", "南皋"}},
        "南京市": {"玄武区": {"南京站", "夫子庙", "紫金山"},
                "栖霞区": {"南京大学", "南京师范", "南京理工"}}
        }
layers = [city]
while True:
    for i in city:
        print(i)
    check = input("请输入：").strip()
    if check == "b":  # 必须在前判断
        city = layers[-1]
        layers.pop()
    elif check == "q":
        print("已退出此程序！！")
        exit()
    elif check not in city:  # 预防输入的值没有在菜单内
        print("请选择相应的地址！！")
        continue
    else:
        layers.append(city)
        city = city[check]
