#!/use/bin/python
import pymysql
import xlrd
import os, re

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


# 查询获取到设备的设备id
def get_eqid(cursor, filename):
    cursor.execute(
        "SELECT EQUIPTEMPLATEID FROM cfgequiptemplate WHERE EQUIPTEMPLATENAME = '%s'" % (filename))
    eqId = cursor.fetchone()[0]
    return eqId


# 更新信号名称
def update_xh(cursor, eqId):
    cursor.execute(
        "UPDATE cfgeventcondition SET MEANING='分闸' WHERE EQUIPTEMPLATEID = '%s' AND CONDITIONID=2 AND MEANING='合闸'" % (
            eqId))
    cursor.execute(
        "UPDATE cfgeventcondition SET MEANING='通讯中断',STARTCOMPAREVALUE='0' WHERE EQUIPTEMPLATEID = '%s' AND EVENTID='1'" % (
            eqId))


def main():
    print('''
    注意事项：
    本脚本的数据库连接为：'localhost', 'root', 'root', 'sgdatabase'
    请确定模板的正确性，可以处理模板的信号名称，但不一定适用
    需处理文件夹为模板的同类型设备
    数据库已存在的告警和告警条件会被更新掉
    不需要处理的设备表不要放入需处理的文件夹内
    ''')

    ##获取需处理文件夹
    filePath = input("请输入需告警仪表文件夹：")
    # filePath=r"H:\gz\zly\二期\bg"
    openFolder(filePath)
    ##打开数据库
    db = pymysql.connect("localhost", "root", "root", "sgdatabase")
    cursor = db.cursor()

    ##更新数据库，文件名相对应的
    for filename in fileNameList:
        eqId = get_eqid(cursor, filename)
        update_xh(cursor, eqId)
        print(filename + "已完成！！")
    ##关闭数据库
    cursor.close()
    db.close()
    input("输入任意字符退出")


if __name__ == '__main__':
    main()
