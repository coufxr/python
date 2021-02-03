#!/use/bin/python
import pymysql, time, os,re, tkinter
from tkinter import filedialog

xhlist = []
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
def update_xh(cursor, eqId):
    # 查询设备对应的信号表
    cursor.execute(
        "SELECT * FROM cfgsignaltemplate WHERE EQUIPTEMPLATEID = '%s'" % (eqId))
    temp = cursor.fetchall()
    ##将元组转为列表
    template = list(list(items) for items in list(temp))
    ##将列表按照二维首列进行排序
    template = sorted(template, key=(lambda x: x[0]))
    for msg in template:
        msg[10]=""
        vue = re.search(r"QF.*电流I$", msg[3])
        if vue != None:
            msg[10] ="" #msg[3]
        # print(msg)
    ##更新数据库
    for sg in template :
        sgId = sg[0]  ##信号id
        sgkzzd = sg[10]  ##信号id

        # print(newName, sgId,sg[3])
        cursor.execute(
            "UPDATE cfgsignaltemplate SET EXTENDFIELD1='%s' WHERE EQUIPTEMPLATEID = '%s' AND SIGNALID ='%s' " % (
                sgkzzd, eqId, sgId))
    print("    ", eqId, "扩展字段1更新完成")



def main():
    print('''
    注意事项：
        1.本脚本的数据库连接为：'localhost', 'root', 'root', 'sgdatabase'
        4.数据库已存在的告警和告警条件会被更新掉
        5.不需要处理的设备表不要放入需处理的文件夹内
        6.使用前，数据库请备份！！
        7.重点：不会报错！！！发生错误会直接结束程序窗口！！！
    ''')
    input("按下回车开始")
    ##将获取模板表和文件夹GUI化选择
    root = tkinter.Tk()
    root.withdraw()
    ##获取需处理文件夹
    ##获取需处理文件夹的路径
    print("请选择文件夹：")
    folderpath = filedialog.askdirectory()
    print("需处理的路径：", folderpath)
    time_start = time.time()  # 开始计时
    openFolder(folderpath)
    ##打开数据库
    db = pymysql.connect("localhost", "root", "root", "sgdatabase")
    cursor = db.cursor()
    ##更新数据库，文件名相对应的
    for filename in fileNameList:
        print(filename + "更新开始！！")
        eqId = get_eqid(cursor, filename)
        update_xh(cursor, eqId)
        print(filename + "已更新完成！！\n")
    ##关闭数据库
    cursor.close()
    db.close()
    time_end = time.time()  # 结束计时
    time_c = time_end - time_start  # 运行所花时间
    print('更新耗时：', time_c, 's')
    input("按下回车退出")


if __name__ == '__main__':
    main()
