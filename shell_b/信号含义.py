#!/use/bin/python
import pymysql, xlrd, time, os, tkinter
from tkinter import filedialog

xhlist = []
fileNameList = []
meaninglist = {}
def openFolder(path):
    for root, dirs, files in os.walk(path, True):
        for f in files:
            filename = f[0:-4]
            fileNameList.append(filename)

def moban(path):
    t1 = xlrd.open_workbook(path)  # 打开t1
    t1shname = t1.sheets()[0]
    nrows = t1shname.nrows
    for i in range(nrows):
        rv = t1shname.row_values(i)
        xhlist.append(rv)

# 查询获取到设备的设备id
def get_eqid(cursor, filename):
    cursor.execute(
        "SELECT EQUIPTEMPLATEID FROM cfgequiptemplate WHERE EQUIPTEMPLATENAME = '%s'" % (filename))
    eqId = cursor.fetchone()[0]
    return eqId

# 更新信号含义
def update_meaning(cursor, eqId):
    for xh in xhlist[1:-1]:
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
        1.本脚本的数据库连接为：'localhost', 'root', 'root', 'sgdatabase'
        2.此脚本修改告警含义
    ''')
    input("按下回车开始")
    ##将获取模板表和文件夹GUI化选择
    root = tkinter.Tk()
    root.withdraw()
    ##将模板中三个表取出来
    ##获取模板的路径和名字
    print("请选择模板文件：")
    filepath = filedialog.askopenfilename(title='打开模板文件', filetypes=[('Excel', '*.xls')])
    print("模板的路径：", filepath)
    moban(filepath)
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
        update_meaning(cursor, eqId)
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
