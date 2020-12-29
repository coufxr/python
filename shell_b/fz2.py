#!/use/bin/python
import xlrd
from xlutils.copy import copy
import os

sjlist = []
sjtjlist = []
filelist = []
row=[]
row2=[]

def openFolder(folder):
    for root, dirs, files in os.walk(folder, True):
        for f in files:
            filename = os.path.join(root, f)
            filelist.append(filename)

def wt(filename):
    t2 = xlrd.open_workbook(filename)  # 打开t2
    # 将t2文件修改操作属性，可读可写
    t2_book = copy(t2)
    for i in range(1, 3):
        if i == 1:
            w2_sheet = t2_book.get_sheet(1)
            k = 0
            for ret in sjlist:
                for w in range(len(ret)):
                    w2_sheet.write(row[k], w, ret[w])
                    # w2_sheet.write(k, w, ret[w])
                # print(row[k], ret)
                k = k + 1
        else:
            w2_sheet = t2_book.get_sheet(2)
            k = 0
            for ret in sjtjlist:
                for w in range(len(ret)):
                    # w2_sheet.write(row2[k], w, ret[w])
                    w2_sheet.write(k, w, ret[w])
                # print(k, ret)
                k = k + 1
    t2_book.save(filename)


def init(moban):
    t1 = xlrd.open_workbook(moban)  # 打开t1
    for i in range(1, 3):
        if i == 1:
            t1shname = t1.sheets()[i] #事件取后6
            nrows = t1shname.nrows
            for i in range(nrows-6,nrows):
                rv = t1shname.row_values(i)
                row.append(i)
                # print(i,rv)
                sjlist.append(rv)
        else:
            t1shname = t1.sheets()[i]#时间条件全部
            nrows = t1shname.nrows
            for i in range(nrows):
                rv = t1shname.row_values(i)
                row2.append(i)
                # print(i,rv)
                sjtjlist.append(rv)

def main():
    # moban = input("请输入模板路径+名称：")
    moban = "E:\ZG\gz\告警\列头柜2改\M101-RPP-1A.xls"
    init(moban)
    # yibfolder = input("请输入需告警仪表文件夹：")
    yibfolder = "E:\ZG\gz\告警\列头柜2改"
    openFolder(yibfolder)
    for filename in filelist:
        wt(filename)
        print(filename + "已完成！！")

if __name__ == '__main__':
    main()
