#!/use/bin/python
import pymysql
import xlrd
import os

sjlist = []
sjtjlist = []
filelist = []
id = ""
name = ""
bds = ""
ms = ""


def openFolder(folder):
    for root, dirs, files in os.walk(folder, True):
        for f in files:
            # filename = os.path.join(root, f)
            filename = f[0:-4]
            filelist.append(filename)


def init(moban):
    t1 = xlrd.open_workbook(moban)  # 打开t1
    for i in range(1, 3):
        if i == 1:
            t1shname = t1.sheets()[i]
            nrows = t1shname.nrows
            for i in range(nrows):
                if i >1:
                    rv = t1shname.row_values(i)
                    sjlist.append(rv)
        else:
            t1shname = t1.sheets()[i]
            nrows = t1shname.nrows
            for i in range(nrows):
                if i >1:
                    rv = t1shname.row_values(i)
                    sjtjlist.append(rv)


def sql(cursor, filename):
    global id, name, bds, ms
    # 取得设备id
    cursor.execute(
        "SELECT EQUIPTEMPLATEID FROM cfgequiptemplate WHERE EQUIPTEMPLATENAME = '%s'" % (filename))
    eqid = cursor.fetchone()[0]
    # print(eqid)
    # 添加事件模板
    for ret in sjlist:
        id = ret[0]
        name = ret[1]
        bds = ret[2]
        ms = ret[3]
        # print(ret)
        cursor.execute(
        "INSERT INTO cfgeventtemplate(EVENTID, EQUIPTEMPLATEID,EVENTNAME,STARTEXPRESSION,DESCRIPTION) VALUES('%s','%s','%s','%s','%s')" % (
            id,eqid,name,bds,ms))
    # 添加条件模板
    for ret in sjtjlist:
        gjtjID = ret[2]  # 条件id
        gjID = ret[0]#事件序号id
        startfu = ret[5]  # 开始比较符
        startvue = ret[6]  # 开始比较值
        if ret[7]=="":
            ret[7]=0
        startys = ret[7]  # 开始延时
        if ret[10]=="":
            ret[10]=0
        endys = 0#ret[10]  # 结束延时
        hanyi = ret[3]#条件含义
        lv = ret[4]#条件等级
        # print(ret)
        # print(ret[2],ret[0],eqid,ret[5],ret[6],ret[7],ret[10],ret[3],ret[4])
        # 告警条件编号,事件告警编号,设备模板编号,开始运算符,开始比较值,条件含义,事件等级
        sql= "INSERT INTO cfgeventcondition(CONDITIONID, EVENTID, EQUIPTEMPLATEID, STARTOPERATION, STARTCOMPAREVALUE, STARTDELAY,ENDDELAY, MEANING, EVENTSEVERITY) VALUES(%s,%s,%s,'%s',%s,%s,%s,'%s',%s)"
        cursor.execute(sql %(gjtjID, gjID, eqid, startfu, startvue, startys, endys, hanyi, lv))
                            # 1,      1,      325, '<',       207,     60,      0, '电压过低', 3
def main():
    print('''
    本脚本的数据库连接为：'localhost', 'root', 'root', 'sgdatabase'。
    模板套用的为事件模板和事件条件模板及导出xls文件第2，3表。
    告警文件夹为导出的同类仪表。
    请注意文件夹内不能有数据库已存在的告警仪表，否则会报错并卡住。
    ''')
    moban = input("请输入模板路径+名称：")
    init(moban)
    yibfolder = input("请输入需告警仪表文件夹：")
    openFolder(yibfolder)
    db = pymysql.connect("localhost", "root", "root", "sgdatabase")
    cursor = db.cursor()
    # sql(cursor, "11AA06a")
    for filename in filelist:
        sql(cursor,filename)
        print(filename+"已完成！！")
    cursor.close()
    db.close()
    s = input("输入任意值退出")


if __name__ == '__main__':
    main()
