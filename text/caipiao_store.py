#!/usr/bin/env python
# encoding: utf-8
'''
@author: coufxr
@contact: mu993364@163.com
@time: 2019/5/17 10:18
@desc:
'''
import random

def random_num():
    global rannum
    rannum = random.randint(1000001, 10000000)
    return rannum

def main():
    while True:
        print('''
             ————彩票购买界面————
            1.手动购买  2.自动购买
            3.查询彩票  4.是否中奖''')
        global haoma
        print("输入号码执行对应操作(exit-->退出程序)")
        num = input("请输入：")
        if num.isdigit():
            if int(num) == 1:
                print("————1.手动购买————")
                print("请输入彩票号码：")
                while True:
                    i = input("号码:")
                    if len(i) == 7:
                        haoma = i
                        print("号码已保存")
                        break
                    else:
                        print("彩票号码长度错误！")
                print("请输入注数(不能超过10注)")
                while True:
                    zhushu = input("注数:")
                    if int(zhushu) > 0 and int(zhushu) < 11:
                        print("购买成功")
                        break
                    else:
                        print("注数过大！请重新输入")
            if int(num) == 2:
                print("————2.自动购买————")
                random_num()
                print("是否选择此号码？:", rannum)
                while True:
                    y_n = input("yes or no?")
                    if y_n == "yes":
                        print("购买成功")
                        haoma = rannum
                        break
                    elif y_n == "no":
                        random_num()
            if int(num) == 3:
                print("————3.查看号码————")
                if haoma!=None:
                    print("你的彩票号码为：",haoma)
                    continue
                else:
                    print("你没有彩票号码！！")
                    continue
            if int(num) == 4:
                print("————4.开奖情况————")
                random_num()
                print("中奖的号码为：", rannum)
                if haoma!=None:
                    if rannum == haoma:
                        print("恭喜您中奖了！！！")
                        break
                    else:
                        print("抱歉，您没有中奖")
                        break
                else:
                    print("你没有购买彩票！！")
        elif num == "exit":
            exit(0)
        else:
            print("输入错误！")
            continue
main()
