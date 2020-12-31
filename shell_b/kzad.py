#!/use/bin/python
import xlrd
import os
import re
from xlutils.copy import copy

vuelist = []
wb=None
def openFile(path):
    global wb
    wb = xlrd.open_workbook(path)  # 打开t1
    ws = wb.sheets()[0]
    nrows = ws.nrows
    for i in range(nrows):
        rv = ws.row_values(i)
        vuelist.append(rv)
def splitVue():
    for v in vuelist[1:-1]:
        vue = v[1]
        vue = re.sub(r'_', "-", vue)  # 将空格替换为下划线
        str = vue.split("-")
        # if len(str)==7:
        #     str[-2]=str[-2][0]
        # elif len(str)==6:
        #     str[-1] = str[-1][0]
        # v[15]=str[1]+"-"+str[3]+"-"+str[4]+"-"+str[5]
        if str[1]=="低压温控仪":
            v[15] = str[1] + "-" + str[2]+"-"+str[3]+"-"+str[4]
        elif str[1]=="低压仪表" or str[1]=="高压仪表" or str[1]=="综保":
            v[15] = str[1] + "-" + str[2]
        elif str[1]=="UPS":
            v[15] = str[1] + "-" + str[2] + "-" + str[3]
        elif str[1]=="直流屏":
            v[15]=str[1]
        elif str[1]=="柴发":
            if str[3] != "通讯状态":
                v[15] = str[1] + "-" + str[2] + "-" + str[3][:3]
            else:
                v[15] = str[1] + "-" + str[2]
                print(v,"柴发此项需检查修改")
        elif str[1]=="油路":
            sss = re.match(r'^\d[a-zA-Z]\d', str[3])
            if sss != None:
                str[3] = sss.group(0)
                print(str[3])
                # v[15] = str[0] + "_" + str[1] + "_" + str[2] + "_" + str[3]
            # if str[3] != "通讯状态":
            #     v[15] = str[1] + "-" + str[2] + "-" + str[3][:3]
        # print(v)
def savefile(wb,path):
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
    path="E:\ZG\gz\zly\电力监控点表分化\中联-WR101-01\中联-WR101-01.xls"
    openFile(path)
    splitVue()
    # savefile(wb,path)
if __name__ == '__main__':
    main()
