from tkinter import filedialog

import os
import pymysql
import re
import tkinter
import xlrd
from xlutils.copy import copy

xhlist = []
sjlist = []
sjtjlist = []
fileNameList = []
meaninglist = {}
wb = None


##打开需处理的文件夹
def openFolder(path):
    for root, dirs, files in os.walk(path, True):
        for f in files:
            filename = f[0:-4]
            fileNameList.append(filename)


##打开模板文件
def openMoban(path):
    global wb
    wb = xlrd.open_workbook(path)  # 打开t1
    for i in range(0, 3):
        if i == 0:
            t1shname = wb.sheets()[i]
            nrows = t1shname.nrows
            for j in range(nrows):
                rv = t1shname.row_values(j)
                xhlist.append(rv)
        elif i == 1:
            t1shname = wb.sheets()[i]
            nrows = t1shname.nrows
            for j in range(nrows):
                rv = t1shname.row_values(j)
                sjlist.append(rv)
        else:
            t1shname = wb.sheets()[i]
            nrows = t1shname.nrows
            for j in range(nrows):
                rv = t1shname.row_values(j)
                sjtjlist.append(rv)


##图形化选择模板文件
def open_Moban_Ui():
    root = tkinter.Tk()
    root.withdraw()
    print("请选择模板文件：")
    path = filedialog.askopenfilename(title='打开模板文件', filetypes=[('Excel', '*.xls')])
    print("模板的路径：", path)
    return path


##图形化选择需处理文件夹
def open_Folder_Ui():
    root = tkinter.Tk()
    root.withdraw()
    print("请选择文件夹：")
    folderpath = filedialog.askdirectory()
    print("需处理的路径：", folderpath)
    return folderpath


##扩展字段的字符串分割
def splitVue():
    for v in xhlist[1:]:  # 去除了首行的列名和最后一行的设备状态信息
        if v[1]=="设备通讯状态":
            continue
        vue = v[1]
        vue = re.sub(r'_', "-", vue)  # 将空格替换为下划线
        str = vue.split("-")
        if str[1] == "低压温控仪" or str[1] == "温控仪" or str[1] == "仪表":
            v[-1] = str[1] + "_" + str[2] + "-" + str[3] + "-" + str[4]
        elif str[1] == "低压仪表" or str[1] == "高压仪表" or str[1] == "综保":
            if str[2] == "水泵控制室":
                v[-1] = str[1] + "_" + str[2] + "-" + str[3] + "-" + str[4]
            else:
                v[-1] = str[1] + "_" + str[2]
        elif str[1] == "UPS":
            if str[2] == "UPS":
                v[-1] = str[2] + "_" + str[3] + "-" + str[4]
            else:
                v[-1] = str[1] + "_" + str[2] + "-" + str[3]
        elif str[1] == "列头柜":
            v[-1] = str[2] + "-" + str[3] + "-" + str[4]
        elif str[1] == "ATS" or str[1] == "壁挂仪表":
            v[-1] = str[1] + "_" + str[2] + "_" + str[3] + "-" + str[4]
        elif str[1] == "直流屏":
            v[-1] = str[1]
        elif str[1] == "柴发":
            v[-1] = str[1] + "_" + str[2]
        elif str[1] == "油路":
            v[-1] = str[1] + "_" + str[2]
        else:
            print(vue,"不存在对应规则")
        # print(v)


##保存文件
def savefile(path):
    wb_w = copy(wb)
    ws_w = wb_w.get_sheet(0)
    k = 0  # 从首行列名算起
    for ret in xhlist:
        for w in range(len(ret)):
            ws_w.write(k, w, ret[w])
        k = k + 1
    wb_w.save(path)
    print("扩展字段修改完成")


##打开数据库
def open_Mysql():
    db = pymysql.connect("localhost", "root", "root", "sgdatabase")
    cursor = db.cursor()
    return db, cursor


##关闭数据库
def close_Mysql(cursor, db):
    cursor.close()
    db.close()


##获取设备的设备id
def get_eqid(cursor, filename):
    cursor.execute(
        "SELECT EQUIPTEMPLATEID FROM cfgequiptemplate WHERE EQUIPTEMPLATENAME = '%s'" % (filename))
    eqId = cursor.fetchone()[0]
    return eqId


##更新信号名
def update_Xh_Name(cursor, eqId):
    ##查询设备对应的信号表
    cursor.execute(
        "SELECT * FROM cfgsignaltemplate WHERE EQUIPTEMPLATEID = '%s'" % (eqId))
    temp = cursor.fetchall()
    ##将元组转为列表
    template = list(list(items) for items in list(temp))
    ##将列表按照二维首列进行排序
    template = sorted(template, key=(lambda x: x[0]))
    ##更新数据库
    for (xh, sg) in zip(xhlist[1:], template):
        newName = xh[1]  ##新的信号名
        sgId = sg[0]  ##信号id
        cursor.execute(
            "UPDATE cfgsignaltemplate SET SIGNALNAME='%s' WHERE EQUIPTEMPLATEID = '%s' AND SIGNALID ='%s' " % (
                newName, eqId, sgId))
    print("    ", eqId, "信号名更新完成")


# 添加告警事件
def insert_gj(cursor, eqId):
    # 添加事件模板
    for ret in sjlist[1:]:
        id = ret[0]
        name = ret[1]
        bds = ret[2]
        ms = ret[3]
        # print(ret)
        ##REPLACE 会将主键已存在的覆盖掉
        cursor.execute(
            "INSERT INTO cfgeventtemplate(EVENTID, EQUIPTEMPLATEID,EVENTNAME,STARTEXPRESSION,DESCRIPTION) VALUES('%s','%s','%s','%s','%s')" % (
                id, eqId, name, bds, ms))
    print("    ", eqId, "添加告警事件完成")


# 添加告警事件条件
def insert_gjsj(cursor, eqId):
    # 添加条件模板
    for ret in sjtjlist[1:]:
        gjtjID = ret[2]  # 条件id
        gjID = ret[0]  # 事件序号id
        startfu = ret[5]  # 开始比较符
        startvue = ret[6]  # 开始比较值
        if ret[7] == "":
            ret[7] = 0
        startys = ret[7]  # 开始延时
        if ret[10] == "":
            ret[10] = 0
        endys = ret[10]  # 结束延时
        hanyi = ret[3]  # 条件含义
        lv = ret[4]  # 条件等级
        # print(ret)
        # print(ret[2],ret[0],eqid,ret[5],ret[6],ret[7],ret[10],ret[3],ret[4])
        # 告警条件编号,事件告警编号,设备模板编号,开始运算符,开始比较值,条件含义,事件等级
        sql = "INSERT INTO cfgeventcondition(CONDITIONID, EVENTID, EQUIPTEMPLATEID, STARTOPERATION, STARTCOMPAREVALUE, STARTDELAY,ENDDELAY, MEANING, EVENTSEVERITY) VALUES(%s,%s,%s,'%s',%s,%s,%s,'%s',%s)"
        cursor.execute(sql % (gjtjID, gjID, eqId, startfu, startvue, startys, endys, hanyi, lv))
        # # 1,      1,      325, '<',       207,     60,      0, '电压过低', 3
    print("    ", eqId, "添加告警事件条件完成")


# 判断是否存在对应的事件，事件条件
# 存在：删除已存在的告警事件和事件条件，再添加
# 不存在：添加
def update_Gj(cursor, eqId):
    cursor.execute(
        "SELECT * FROM cfgeventtemplate WHERE EQUIPTEMPLATEID = '%s'" % (eqId))
    gj_tmp = cursor.fetchall()
    cursor.execute(
        "SELECT * FROM cfgeventcondition WHERE EQUIPTEMPLATEID = '%s'" % (eqId))
    gjsj_tmp = cursor.fetchall()
    # 判断设备id对应的告警事件和告警事件条件是否存在
    # 存在就删除再添加，不存在就直接添加
    if len(gj_tmp) != 0:
        # 删除告警事件
        cursor.execute(
            "DELETE FROM cfgeventtemplate WHERE EQUIPTEMPLATEID = '%s'" % (eqId))
        print("    ", eqId, "删除告警事件完成")
        insert_gj(cursor, eqId)
    else:
        insert_gj(cursor, eqId)

    if len(gjsj_tmp) != 0:
        # 删除告警事件条件
        cursor.execute(
            "DELETE FROM cfgeventcondition WHERE EQUIPTEMPLATEID = '%s'" % (eqId))
        print("    ", eqId, "删除告警事件条件完成")
        insert_gjsj(cursor, eqId)
    else:
        insert_gjsj(cursor, eqId)


# 更新信号含义
def update_Meaning(cursor, eqId):
    for xh in xhlist[1:]:
        if xh[8] != "":
            retlist = []
            str = xh[8].split(";")
            for i in range(len(str)):
                if str[i]:
                    retlist.append(str[i].split(':'))
            meaninglist[xh[0]] = retlist
    # 删除信号含义
    cursor.execute("DELETE FROM cfgsignalmeaning WHERE EQUIPTEMPLATEID = '%s'" % (eqId))
    print("    ", eqId, "删除信号含义成功！")
    # 添加信号含义
    for k, v in meaninglist.items():
        for y in v:
            # print(k,y[0],y[1])
            cursor.execute(
                "INSERT INTO cfgsignalmeaning(SIGNALID,EQUIPTEMPLATEID,MEANING,STATEVALUE)VALUES('%s','%s','%s','%s')" % (
                    k, eqId, y[1], y[0]))
    print("    ", eqId, "添加信号含义成功！")


def main():
    print('''
    注意事项：
        1.本脚本的数据库连接为：'localhost', 'root', 'root', 'sgdatabase';使用本脚本前，数据库请备份！！
        2.扩展字段目前对字段格式要求较高，请谨慎使用。
        3.请确定模板的正确性，需要处理的文件夹内应为模板的同类型设备。
        4.本脚本是根据需处理文件夹内的“文件名”进行处理的，与文件本身无关！
        5.所有处理不包含“信号表达式”。
        4.请注意本脚本不会报错！！！如发生错误会直接结束程序窗口！
    ''')
    input("按下任意键开始")
    while True:
        print('''
        ---------------------------------
        1:扩展字段
        2:更新信号名称
        3:更新告警和告警含义
        4:更新信号表(包括信号,告警和告警含义)
        5:更新信号含义
        0:退出
        ''')
        inp = input("请输入对应的值:")
        if inp == "0":
            return
        elif inp == "1":
            print('''
            -----------------------------------------------
            字段分割请使用‘-’、‘_’这两种字符,不可存在空格
            目前仅支持标准格式:  P7_列头柜_M101-RPP-1A_通讯状态
            ''')
            path = open_Moban_Ui()
            openMoban(path)
            splitVue()
            savefile(path)
        elif inp == "2":
            openMoban(open_Moban_Ui())
            openFolder(open_Folder_Ui())
            db, cursor = open_Mysql()
            for filename in fileNameList:
                eqId = get_eqid(cursor, filename)
                update_Xh_Name(cursor, eqId)
                print(filename + "  的信号名称已更新完成！！")
            close_Mysql(cursor, db)
        elif inp == "3":
            openMoban(open_Moban_Ui())
            openFolder(open_Folder_Ui())
            db, cursor = open_Mysql()
            for filename in fileNameList:
                eqId = get_eqid(cursor, filename)
                update_Gj(cursor, eqId)
                print(filename + "  的告警和告警含义已更新完成！！")
            close_Mysql(cursor, db)
        elif inp == "4":
            openMoban(open_Moban_Ui())
            openFolder(open_Folder_Ui())
            db, cursor = open_Mysql()
            for filename in fileNameList:
                eqId = get_eqid(cursor, filename)
                update_Xh_Name(cursor, eqId)
                update_Gj(cursor, eqId)
                print(filename + "  信号表已更新完成！！")
            close_Mysql(cursor, db)
        elif inp == "5":
            openMoban(open_Moban_Ui())
            openFolder(open_Folder_Ui())
            db, cursor = open_Mysql()
            for filename in fileNameList:
                eqId = get_eqid(cursor, filename)
                update_Meaning(cursor, eqId)
                print(filename + "  信号含义已更新完成！！")
            close_Mysql(cursor, db)


if __name__ == '__main__':
    main()
