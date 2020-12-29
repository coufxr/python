#!/use/bin/python
import numpy as np
from openpyxl import Workbook
import re
import xlrd

vuelist = []
keylist = []
namelist = []
biaolist = []
name = ""
Nonelist = []  # 无编号的值列表
flag = False


def openfile():
    rb = xlrd.open_workbook(r'E:\ZG\GZ\zhonglian\电力监控点表分化\中联-WR101-01\中联-WR101-01.xls')
    rs = rb.sheet_by_name("信号模板")
    rows = rs.nrows
    # 读取每行的值
    for i in range(rows):
        if i != 0:
            rv = rs.row_values(i)
            vuelist.append(rv)
        else:
            rk = rs.row_values(i)
            keylist.append(rk)
    del vuelist[-1]


def spl():
    global flag
    # 进行字符串分割
    for v in vuelist:
        vue = v[1]
        vue = re.sub(r'\s', "_", vue)  # 将空格替换为下划线
        str = vue.split("_")
        # 判断是否全为中文，进行三项拼接
        if str[1].isalpha():
            # 判断是否含有“直流屏”，有则只拼接0和直流屏
            if "直流屏" in str[1]:
                name = str[0] + "_" + str[1]
                namelist.append(name)
            # 判断是否含有“柴发”，有则只拼接0和直流屏
            elif "柴发" in str[1]:
                # 只去除了汉字，但还要编号加字母和数字
                if not str[3].isalpha():
                    msg = re.search(r'\[a-zA-Z]\d+', str[3])
                    if msg != None:
                        str[3] = msg.group(0)
                        name = str[0] + "_" + str[1] + "_" + str[2] + "_" + str[3]
                        namelist.append(name)
                        # flag = False
                # return
            elif "油路" in str[1]:
                if str[3].isalpha():  # 最重要的无编号
                    # print(str)
                    name = str[0] + "_" + str[1] + "_" + str[2]
                    Nonelist.append(v)
                    namelist.append(name)
                    flag = True
                # 判断的是否为【1-9】#的值---【1#】格式
                elif re.match(r'^\d#', str[3]) != None:
                    msp = re.match(r'^\d#', str[3])
                    if msp != None:
                        str[3] = msp.group(0)
                        name = str[0] + "_" + str[1] + "_" + str[2] + "_" + str[3]
                        namelist.append(name)
                # 判断数字加字母加数字开头
                elif re.match(r'^\d[a-zA-Z]+\d+', str[3])!= None:
                    sss = re.match(r'^\d[a-zA-Z]+\d+', str[3])
                    if sss != None:
                        str[3] = sss.group(0)
                        name = str[0] + "_" + str[1] + "_" + str[2] + "_" + str[3]
                        namelist.append(name)
                # # 判断字母加两个数字开头的
                elif re.match(r'^[a-zA-Z]\d{2}', str[3])!= None:
                    grp = re.match(r'^[a-zA-Z]\d{2}', str[3])
                    if grp != None:
                        str[3] = grp.group(0)
                        name = str[0] + "_" + str[1] + "_" + str[2] + "_" + str[3]
                        namelist.append(name)
                else:
                    Nonelist.append(v)
                    flag = True
                    # pass
            else:
                name = str[0] + "_" + str[1] + "_" + str[2]
                namelist.append(name)
        else:  # 不全为中文时，只进行两项拼接
            name = str[0] + "_" + str[1]
            namelist.append(name)


# 判定分割后的字符串是否在名称里面，在则添加到新列表，并删除在的名称防止二次匹配
def pp(name, flag):
    if flag:  # 无编号出表
        for N in Nonelist:
            if name in N[1]:
                biaolist.append(N)
    else:
        for v in vuelist:
            if name in v[1]:
                biaolist.append(v)
    sevefile(name)


def sevefile(name):
    wb = Workbook()
    ws = wb.create_sheet("信号模板")
    for i in range(len(biaolist)):
        id = int(biaolist[i][0])
        kid = 1276
        kstr = "[{kid},{id}]".format(kid=kid, id=id)
        biaolist[i][7] = kstr
        biaolist[i][5] = -2
        biaolist[i][0] = i + 1
    label = np.array(keylist)
    feature = np.array(biaolist, dtype=object)
    feature = np.transpose(feature)  # 翻转矩阵
    # print(feature)
    label_input = []
    for j in range(len(label[0])):
        label_input.append(label[0][j])
    ws.append(label_input)
    # print(label_input)

    for f in range(len(feature[0])):
        ws.append(feature[:, f].tolist())
    wb.save("{name}.xls".format(name=name))
    print(name + "已保存")


def main():
    global namelist, name
    openfile()
    spl()
    # name去重
    namelist = list(set(namelist))
    # 排序
    namelist.sort()
    for k in namelist:
        biaolist.clear()
        pp(k, flag)
        # print(k)


if __name__ == '__main__':
    main()
