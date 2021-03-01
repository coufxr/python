#!/use/bin/python
from tkinter import filedialog

import os
import pymysql
import re
import tkinter
import xlrd
from xlutils.copy import copy

xhlist = []
fileNameList = []
ret = []
wtlist = []

def openFolder(path):
    for root, dirs, files in os.walk(path, True):
        for f in files:
            filename = f[0:-4]
            fileNameList.append(filename)
# 查询获取到设备的设备id
def get_eqid(cursor, filename):
    cursor.execute(
        "SELECT EQUIPTEMPLATEID FROM cfgequiptemplate WHERE EQUIPTEMPLATENAME = '%s'" % (filename))
    eqId = cursor.fetchone()[0]
    return eqId
def update_xh(cursor, eqId):
    # 查询设备对应的信号表
    cursor.execute(
        "SELECT * FROM cfgsignaltemplate WHERE EQUIPTEMPLATEID = '%s'" % (eqId))
    temp = cursor.fetchall()
    ##将元组转为列表
    template = list(list(items) for items in list(temp))
    ##将列表按照二维首列进行排序
    template = sorted(template, key=(lambda x: x[0]))
    for msg in template:
        vue = re.search(r"QF.*电流I$", msg[3])
        if vue != None:
            ret.append(msg)
def one(cursor):
    xhlist = sorted(ret, key=(lambda x: [x[3][:5], x[1], x[0]]))
    for i in range(0, len(xhlist), 2):
        l2 = xhlist[i:i + 2]
        # print(l2)
        for j in range(0, len(l2), 2):
            cursor.execute(
                "SELECT EQUIPTEMPLATENAME FROM cfgequiptemplate WHERE EQUIPTEMPLATEID = '%s'" % (l2[j][1]))
            eqName = cursor.fetchone()
            name = eqName[0][:-1] + "_" + l2[j][3][:5] + "合计电流"
            sumvue = l2[j][8] + "+" + l2[j + 1][8]
            wtlist.append([name, sumvue])
def save(path):
    t1 = xlrd.open_workbook(path)  # 打开t1
    wb = copy(t1)
    wtlists = sorted(wtlist, key=(lambda x: [x[0][:11]]))
    for i in range(0, 1):
        w2_sheet = wb.get_sheet(0)
        k = 1
        for i in wtlists:
            print(i)
            w2_sheet.write(k, 1, i[0])
            w2_sheet.write(k, 7, i[1])
            k += 1
    wb.save(path)
def main():
    input("按下回车开始")
    root = tkinter.Tk()
    root.withdraw()
    print("请选择文件夹：")
    folderpath = filedialog.askdirectory()
    print("需处理的路径：", folderpath)
    openFolder(folderpath)
    ##打开数据库
    db = pymysql.connect("localhost", "root", "root", "sgdatabase")
    cursor = db.cursor()

    path = r"H:\gz\zly\中联密云名称告警修改\列头柜合计电流.xls"

    for filename in fileNameList:
        # print(filename + "更新开始！！")
        eqId = get_eqid(cursor, filename)
        update_xh(cursor, eqId)
    one(cursor)
    save(path)
    cursor.close()
    db.close()

    input("按下回车退出")

if __name__ == '__main__':
    main()