#!/use/bin/python
import xlrd
import os
import re
from xlutils.copy import copy

vuelist = []

def openFile(path):
    wb = xlrd.open_workbook(path)  # 打开t1
    ws = wb.sheets()[0]
    nrows = ws.nrows
    for i in range(nrows):
        rv = ws.row_values(i)
        vuelist.append(rv)
    for v in vuelist[1:-1]:
        vue = v[1]
        vue = re.sub(r'_', "-", vue)  # 将空格替换为下划线
        str = vue.split("-")
        if "壁挂仪表" in str[1]:
            v[15] = str[1] + "-" + str[3] + "-" + str[4]+ "-" + str[5][:1]
        elif "列头柜" in str[1]:
            v[15] = str[2] + "-" + str[3] + "-" + str[4]
        elif "ATS" in str[1]:
            v[-1] = str[1] + "-" + str[3] + "-" + str[4] + "-" + str[5][:1]
        # if len(str)==7:
        #     str[-2]=str[-2][0]
        # elif len(str)==6:
        #     str[-1] = str[-1][0]
        # v[15]=str[1]+"-"+str[3]+"-"+str[4]+"-"+str[5]
        # print(v)
    wb_w = copy(wb)
    ws_w = wb_w.get_sheet(0)
    k = 0
    for ret in vuelist:
        for w in range(len(ret)):
            ws_w.write(k, w, ret[w])
        k = k + 1

    wb_w.save(path)
    print("扩展字段修改完成")
def main():
    print('''
           名称内建议不要有空格
           1.P9_壁挂仪表-二期预留SR104强电间-ALH-1F-4通讯状态
           拼接：壁挂仪表,ALH,1F,4
           2.P8_ATS-二期预留SR104强电间-ALB-1F-4S1-Uab
           拼接:ATS,ALB,1F,4
           目前没有其他拼接方法
           ''')
    # path = input("请输入需修改的文件名称：")
    path=r"E:\ZG\gz\zly\20201225\中联-10-10-25-26.xls"
    openFile(path)
if __name__ == '__main__':
    main()
