#!/use/bin/python
import xlrd
from xlutils.copy import copy
import os
import re

sjlist = []
sjtjlist = []
filelist = []

def openFolder(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if re.search(r'.xls$', file_path) != None:
            # print(file_path)
            filelist.append(file_path)
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
                    w2_sheet.write(k, w, ret[w])
                # print(k, ret)
                k = k + 1
        else:
            w2_sheet = t2_book.get_sheet(2)
            k = 0
            for ret in sjtjlist:
                for w in range(len(ret)):
                    w2_sheet.write(k, w, ret[w])
                # print(k, ret)
                k = k + 1
    t2_book.save(filename)


def init(moban):
    t1 = xlrd.open_workbook(moban)  # 打开t1
    for i in range(1, 3):
        if i == 1:
            t1shname = t1.sheets()[i]
            nrows = t1shname.nrows
            for i in range(nrows):
                rv = t1shname.row_values(i)
                sjlist.append(rv)
        else:
            t1shname = t1.sheets()[i]
            nrows = t1shname.nrows
            for i in range(nrows):
                rv = t1shname.row_values(i)
                sjtjlist.append(rv)

def main():
    print('''
       只套用一层文件夹
       模板套用的为事件模板和事件条件模板及导出xls文件第2，3表。
       ''')
    moban = input("请输入模板路径+名称：")
    init(moban)
    yibfolder = input("请输入需复制文件夹：")
    openFolder(yibfolder)
    for filename in filelist:
        wt(filename)
        print(filename + "已完成！！")
    s = input("输入任意值退出")
# r"E:\ZG\gz\告警\UPS\UPS_UPS-21-11.xls"
if __name__ == '__main__':
    main()
