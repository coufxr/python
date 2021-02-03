import xlrd,re
xhlist=[]

path=r"H:\gz\zly\中联密云名称告警修改\列头柜\M101-RPP-1A.xls"

t1 = xlrd.open_workbook(path)  # 打开t1
t1shname = t1.sheets()[0]
nrows = t1shname.nrows
for i in range(nrows):
    rv = t1shname.row_values(i)
    xhlist.append(rv)
for xh in xhlist[1:-1]:
    vue = re.search(r"QF.*电流I$", xh[1])
    if vue!= None:
        xh[-1]=xh[1]
        print(xh)