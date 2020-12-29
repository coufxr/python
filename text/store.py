#!/usr/bin/env python
# encoding: utf-8
'''
@author: coufxr
@contact: mu993364@163.com
@time: 2019/5/23 8:26
@desc:
'''

goods_list = [
    ["牙刷", 10],
    ["牙膏", 20],
    ["漱口杯", 20],
    ["十万个为什么", 45],
    ["苹果 Xs", 6000],
    ["苹果 Xs max", 8000],
    ["一加7", 4000],
    ["联想 Y7000", 6000],
    ["蓝山咖啡", 40],
]
goodscar = []  ##购物车
le =  len(goods_list)
# 判断输入的值
def if_num(num):
    while num != "":
        if num == '1':
            for k in goods_list:
                print(goods_list.index(k), k[0], k[1])
            v = input("请输入你要购买的物品编号,q退出：")
            if v != 'q':
                if int(v) <= le:
                    goodscar.append(goods_list[int(v)])
                    print(goodscar)
                else:
                    print("你输入的编号超出")
            else:
                break
        elif num == '2':
            print("{:-^40}".format("购物车"))
            b = []
            for j in goodscar:
                if j not in b:
                    b.append(j)
                    num = goodscar.count(j)
                    # 格式化输出  列对齐模式
                    print("{name:<10}\t{price:>10}\t{num:>5}\t{money:>5}"
                          .format(name=j[0], price=j[1], num=num, money=j[1] * num))  # ,chr(12288)
            yn = input("是否结账(Y/N)")
            if yn == "Y" and yn == "y":
                pass
            elif yn == "N" and yn == "n":
                pass
            else:
                break
# 主函数
def main():
    print("——欢迎来到购物商城——")
    user_money = input("请输入你的购物金额：")
    while user_money != "":
        user_money = int(user_money)
        print('''
                     ————购物商城界面————
                    1.购买商品  2.购物车
                    3.我的信息  q.退出''')
        num = input("请输入你要进行操作的编号：")
        if_num(num)
if __name__ == '__main__':
    main()

