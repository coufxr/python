#!/use/bin/python
import xlrd
import re
from xlutils.copy import copy

vuelist = []
wb = None


def openFile(path):
    global wb
    wb = xlrd.open_workbook(path)  # 打开t1
    ws = wb.sheets()[0]
    nrows = ws.nrows
    for i in range(nrows):
        rv = ws.row_values(i)
        vuelist.append(rv)


def splitVue():
    for v in vuelist[1:-1]:  # 去除了首行的列名和最后一行的设备状态信息
        vue = v[1]
        vue = re.sub(r'_', "-", vue)  # 将空格替换为下划线
        str = vue.split("-")
        if str[1] == "低压温控仪" or str[1] == "温控仪" or str[1] == "仪表":
            v[-1] = str[1] + "-" + str[2] + "-" + str[3] + "-" + str[4]
        elif str[1] == "低压仪表" or str[1] == "高压仪表" or str[1] == "综保":
            if str[2] == "水泵控制室":
                v[-1] = str[1] + "-" + str[2] + "-" + str[3] + "-" + str[4]
            else:
                v[-1] = str[1] + "-" + str[2]
        elif str[1] == "UPS":
            if str[2] == "UPS":
                v[-1] = str[2] + "-" + str[3] + "-" + str[4]
            else:
                v[-1] = str[1] + "-" + str[2] + "-" + str[3]
        elif str[1] == "列头柜":
            v[-1] = str[2] + "-" + str[3] + "-" + str[4]
        elif str[1] == "ATS" or str[1] == "壁挂仪表":
            v[-1] = str[1] + "-" + str[2] + "-" + str[3] + "-" + str[4]
        elif str[1] == "直流屏":
            v[-1] = str[1]
        elif str[1] == "柴发":
            if str[3] != "通讯状态":
                v[-1] = str[1] + "-" + str[2] + "-" + str[3][:3]
            else:
                v[-1] = str[1] + "-" + str[2]
                print(v, "柴发此项需检查修改")
        elif str[1] == "油路":
            Newyl = re.findall(r'^[a-zA-Z]\d\d', str[3])
            if len(Newyl) != 0:
                v[-1] = str[1] + "-" + str[2] + "-" + Newyl[0]
            else:
                v[-1] = str[1] + "-" + str[2]
        else:
            print("不存在对应规则")
        # print(v)


def savefile(wb, path):
    wb_w = copy(wb)
    ws_w = wb_w.get_sheet(0)
    k = 0  # 从首行列名算起
    for ret in vuelist:
        for w in range(len(ret)):
            ws_w.write(k, w, ret[w])
        k = k + 1

    wb_w.save(path)
    print("扩展字段修改完成")


def main():
    print('''
            名称内不能存在空格，建议提前替换、去除
            目前支持:
                仪表(高压、低压、综保、壁挂)
                温控仪(低压)、UPS
                ATS、油路、柴发、直流屏
            根据"_"或者"-"进行分割，请将各个名称中分割好,否则存在拼接错误
            例如：低压仪表12AA11；请将其替换为：低压仪表-12AA11，或者：低压仪表_12AA11
            请注意直流屏的名称！！！
            仪表、温控仪、油路、柴发会将名称带上，请注意！
            程序执行完请检查excel表，可能存在错误
           ''')
    path = input("请输入需修改的文件名称：")
    # path = "E:\ZG\gz\zly\电力监控点表分化\中联-WR101-07_25.xls"
    openFile(path)
    splitVue()
    savefile(wb, path)


if __name__ == '__main__':
    main()
