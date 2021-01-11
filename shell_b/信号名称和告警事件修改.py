#!/use/bin/python
import pymysql, xlrd, os

xhlist = []
sjlist = []
sjtjlist = []
fileNameList = []


def openFolder(path):
    for root, dirs, files in os.walk(path, True):
        for f in files:
            # filename = os.path.join(root, f)
            filename = f[0:-4]
            fileNameList.append(filename)


def moban(path):
    t1 = xlrd.open_workbook(path)  # 打开t1
    for i in range(0, 3):
        if i == 0:
            t1shname = t1.sheets()[i]
            nrows = t1shname.nrows
            for i in range(nrows):
                if i > 0:  # 不需要每个表的首行列明
                    rv = t1shname.row_values(i)
                    xhlist.append(rv)
        elif i == 1:
            t1shname = t1.sheets()[i]
            nrows = t1shname.nrows
            for i in range(nrows):
                if i > 0:
                    rv = t1shname.row_values(i)
                    sjlist.append(rv)
        else:
            t1shname = t1.sheets()[i]
            nrows = t1shname.nrows
            for i in range(nrows):
                if i > 0:
                    rv = t1shname.row_values(i)
                    sjtjlist.append(rv)


# 查询获取到设备的设备id
def get_eqid(cursor, filename):
    cursor.execute(
        "SELECT EQUIPTEMPLATEID FROM cfgequiptemplate WHERE EQUIPTEMPLATENAME = '%s'" % (filename))
    eqId = cursor.fetchone()[0]
    return eqId


# 更新信号名称
def update_xh(cursor, eqId):
    # 查询设备对应的信号表
    cursor.execute(
        "SELECT * FROM cfgsignaltemplate WHERE EQUIPTEMPLATEID = '%s'" % (eqId))
    temp = cursor.fetchall()
    ##将元组转为列表
    template = list(list(items) for items in list(temp))
    ##将列表按照二维首列进行排序
    template = sorted(template, key=(lambda x: x[0]))
    # for eq in template:
    #     print(eq)
    ##更新数据库
    for (xh, sg) in zip(xhlist, template):
        newName = xh[1]  ##新的信号名
        sgId = sg[0]  ##信号id
        # print(newName, sgId,sg[3])
        cursor.execute(
            "UPDATE cfgsignaltemplate SET SIGNALNAME='%s' WHERE EQUIPTEMPLATEID = '%s' AND SIGNALID ='%s' " % (
                newName, eqId, sgId))
    print("    ", eqId, "信号名更新完成")


# 添加告警事件
def insert_gj(cursor, eqId):
    # 添加事件模板
    for ret in sjlist:
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
    for ret in sjtjlist:
        gjtjID = ret[2]  # 条件id
        gjID = ret[0]  # 事件序号id
        startfu = ret[5]  # 开始比较符
        startvue = ret[6]  # 开始比较值
        if ret[7] == "":
            ret[7] = 0
        startys = ret[7]  # 开始延时
        if ret[10] == "":
            ret[10] = 0
        endys = 0  # ret[10]  # 结束延时
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
def delete_gj(db, cursor, eqId):
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
        # print(gjsj_tmp)
        # 删除告警事件条件
        cursor.execute(
            "DELETE FROM cfgeventcondition WHERE EQUIPTEMPLATEID = '%s'" % (eqId))
        print("    ", eqId, "删除告警事件条件完成")
        insert_gjsj(cursor, eqId)
    else:
        insert_gjsj(cursor, eqId)


def main():
    print('''
    注意事项：
    1.本脚本的数据库连接为：'localhost', 'root', 'root', 'sgdatabase'
    2.请确定模板的正确性，否则会中断程序运行
    3.需处理文件夹为模板的同类型设备
    4.数据库已存在的告警和告警条件会被更新掉
    5.不需要处理的设备表不要放入需处理的文件夹内
    6.重点：不会报错！！！发生错误会直接结束程序窗口！！！
    
    
    ''')
    ##将模板中三个表取出来
    path = input("请输入模板路径+名称：")
    moban(path)
    ##获取需处理文件夹
    ffPath = input("请输入需告警仪表文件夹：")
    openFolder(ffPath)
    ##打开数据库
    db = pymysql.connect("localhost", "root", "root", "sgdatabase")
    cursor = db.cursor()

    ##更新数据库，文件名相对应的
    for filename in fileNameList:
        eqId = get_eqid(cursor, filename)
        update_xh(cursor, eqId)
        delete_gj(db, cursor, eqId)
        print(filename + "已更新完成！！")
    ##关闭数据库
    cursor.close()
    db.close()
    input("输入任意字符退出")


if __name__ == '__main__':
    main()
