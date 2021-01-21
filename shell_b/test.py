import xlrd,re
xhlist=[]

path=r"H:\gz\zly\中联密云名称告警修改\壁挂仪表\CRAH-A101-1.xls"

t1 = xlrd.open_workbook(path)  # 打开t1
t1shname = t1.sheets()[0]
nrows = t1shname.nrows
for i in range(nrows):
    if i > 0:  # 不需要每个表的首行列明
        rv = t1shname.row_values(i)
        xhlist.append(rv)
meaninglist={}
for xh in xhlist:
    if xh[8]!="":
        retlist = []
        str= xh[8].split(";")
        for i in range(len(str)):
            if str[i]:
                retlist.append(str[i].split(':'))
        # print(retlist)
        meaninglist[xh[0]]=retlist
# print(meaninglist)
#
#         # str.insert(0,i[0])
#         # meaninglist.append(str)
#
for k,v in meaninglist.items():
    print(k, v[0], v[1])
    for y in v:
        print(k,y[0], y[1])