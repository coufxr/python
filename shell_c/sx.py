#!/use/bin/python
import tkinter
from tkinter import filedialog

import xlrd
from xlutils.copy import copy
import os
import re

sheet1 = []
sheet2 = []
t2_sheet1 = []
t2_sheet2 = []
xhlist=[]

def opent1(path):
    wb = xlrd.open_workbook(path)  # 打开t1
    for i in range(0, 2):
        if i == 0:
            t1shname = wb.sheets()[i]
            nrows = t1shname.nrows
            for j in range(nrows):
                rv = t1shname.row_values(j)
                sheet1.append(rv)
        elif i == 1:
            t1shname = wb.sheets()[i]
            nrows = t1shname.nrows
            for j in range(nrows):
                rv = t1shname.row_values(j)
                sheet2.append(rv)
def opent2(path):
    wb = xlrd.open_workbook(path)  # 打开t1
    for i in range(0, 2):
        if i == 0:
            t1shname = wb.sheets()[i]
            nrows = t1shname.nrows
            for j in range(nrows):
                rv = t1shname.row_values(j)
                t2_sheet1.append(rv)
        elif i == 1:
            t1shname = wb.sheets()[i]
            nrows = t1shname.nrows
            for j in range(nrows):
                rv = t1shname.row_values(j)
                t2_sheet2.append(rv)

##图形化选择模板文件
def open_Moban_Ui():
    root = tkinter.Tk()
    root.withdraw()
    print("请选择模板文件：")
    path = filedialog.askopenfilename(title='打开模板文件', filetypes=[('Excel', '*.xls')])
    print("模板的路径：", path)
    return path
##保存文件
def savefile(path):
    wb = xlrd.open_workbook(path)  # 打开t1
    wb_w = copy(wb)
    ws_w = wb_w.get_sheet(0)
    k = 0  # 从首行列名算起
    for ret in xhlist:
        for w in range(len(ret)):
            ws_w.write(k, w, ret[w])
        k = k + 1
    wb_w.save(path)
def ff():
    for bz in sheet2:
        for cd in t2_sheet1:
            if bz[0]==cd[1] and bz[1]==cd[1]:
                if bz[2]==cd[5]:
                    xhlist.append(cd)
def main():
    opent1(open_Moban_Ui())
    opent2(open_Moban_Ui())
    ff()
    savefile(open_Moban_Ui())
if __name__ == '__main__':
    main()
