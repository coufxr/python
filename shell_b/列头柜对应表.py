#!/use/bin/python
import xlrd
import os
import re
from xlutils.copy import copy

idlist = []
filelist = []
vuelist=[]

name=[]

def openFolder(folder):
    for root, dirs, files in os.walk(folder, True):
        for f in files:
            filename = os.path.join(root, f)
            # filename = f[0:-4]
            # print(filename)
            filelist.append(filename)

def openid(filename):
    rb = xlrd.open_workbook(filename)  # 打开t1
    wt = copy(rb)
    for stname in rb.sheet_names():
        rs = rb.sheet_by_name(stname)
        rows = rs.nrows
        idlist.clear()
        name.clear()
        for i in range(rows):
            rv = rs.row_values(i)
            idlist.append(rv)

        for v in idlist:
            vue = v[2]
            str = vue.split("-")
            # print(str)
            if re.match(r'^[\u4e00-\u9fa5]', vue) == None:
                namestr = "{a}-{b}{c}-{d}".format(a=str[0], b=str[1], c=str[2], d=v[1][1:])
                # print(namestr)
                name.append(namestr)
            else:
                name.append(vue)
        update(stname)
        w2_sheet = wt.get_sheet(stname)
        k = 0
        for ret in name:
            w2_sheet.write(k, 5, ret)
            print(k, ret)
            k = k + 1
        print(stname + "已提取并转换")
        wt.save(filename)

def update(stname):
    for i in name:
        print(i)
    print(stname + "已提取并转换")

def main():
    openFolder(r"E:\ZG\gz\zly\列头柜机柜对应表\列头柜对应表二期")
    for filename in filelist:
        openid(filename)
        print(filename + "已完成！！")
if __name__ == '__main__':
    main()