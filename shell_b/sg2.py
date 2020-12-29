#!/use/bin/python
import xlrd
import os
import re
from xlutils.copy import copy

filelist = []
vuelist = []

def openFolder(folder):
    for root, dirs, files in os.walk(folder, True):
        for f in files:
            filename = os.path.join(root, f)
            filelist.append(filename)

def openfd(filename):
    rb = xlrd.open_workbook(filename)
    rs = rb.sheet_by_name("信号模板")
    wt = copy(rb)
    rows = rs.nrows
    # 读取每行的值
    for i in range(rows):
        rv = rs.row_values(i)
        vuelist.append(rv)
    for v in vuelist:
        if "支路" in v[1]:
            str = v[1].split("_")[3:]
            print(str)
            str = str[0]+str[1]
            # print(str)
            mas = re.findall("\d+",str)[0]
            hz= re.split(mas,str)[-1]
            v[1]=hz
    w2_sheet = wt.get_sheet(0)
    k = 0
    for ret in vuelist:
        for w in range(len(ret)):
            w2_sheet.write(k, w, ret[w])
        # print(k, ret)
        k = k + 1
    wt.save(filename)
    vuelist.clear()
def main():
    openFolder(r"E:\ZG\gz\告警\列头柜告警")
    for filename in filelist:
        openfd(filename)
    # openfd(r"E:\ZG\gz\告警\列头柜告警\M101-RPP-2A.xls")
        print(filename + "已完成！！")


if __name__ == '__main__':
    main()
