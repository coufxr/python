#!/use/bin/python
import xlrd,re,tkinter
from tkinter import filedialog
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
        print(ret)
    wb_w.save(path)
    print("扩展字段修改完成")

def open_Moban_Ui():
    root = tkinter.Tk()
    root.withdraw()
    print("请选择模板文件：")
    path = filedialog.askopenfilename(title='打开模板文件', filetypes=[('Excel', '*.xls')])
    print("模板的路径：", path)
    return path
def open_Folder_Ui():
    root = tkinter.Tk()
    root.withdraw()
    print("请选择文件夹：")
    folderpath = filedialog.askdirectory()
    print("需处理的路径：", folderpath)
    return folderpath
def main():
    path= open_Moban_Ui()
    openFile(path)
    splitVue()
    savefile(wb, path)


if __name__ == '__main__':
    main()
