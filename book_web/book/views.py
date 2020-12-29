from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect
import pymysql
# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request,"index.html")
# 两个内嵌框架的链接
def nav(request):
    if request.method == "GET":
        return render(request, "nav.html")
def footer(request):
    if request.method=="GET":
        return render(request, "footer.html")
# 各个页面的链接
def fl(request):
    if request.method == "GET":
        xhlist={}
        bdlist={}
        pslist={}
        for i in range (1,10):
            if i<=4:
                pslist[i]=i
            if i>=4:
                bdlist[i]=i
            xhlist[i]=i
        return render(request, "fl.html",{"bdlist":bdlist,"xh_showbook":xhlist,"pslist":pslist})
def lt(request):
    if request.method == "GET":
        return render(request, "lt.html")

def login(request):
    global name,pwd
    if request.method == "GET":
        return render(request, "Login_Registered.html")
    else:
        name = request.POST.get("username")
        pwd = request.POST.get("userpwd")
        email = request.POST.get("useremail")
        rl_code= request.POST.get("rl_code")
        print(name,pwd,email,rl_code)
        ###注册功能
        if rl_code == 'false':
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123123', db='book_web')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            sql = "insert into user_info(name,pwd,email,identy) values('%s','%s','%s','%s')"
            try:
                cursor.execute(sql % (name,pwd,email,"hy"))
                conn.commit()
                print("成功!!")
                return JsonResponse({"status": 200, "msg": "ok", "data": "/index/"})
            except:
                conn.rollback()
                print('Insert operation error')
                raise
            finally:
                cursor.close()
                conn.close()
        else:##登录功能

            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123123', db='book_web')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)#
            try:
                cursor.execute("select name,pwd from user_info where name='%s'"%(name))
                results = cursor.fetchall()
                db_name =results[0]['name']
                db_pwd = results[0]['pwd']
                print(db_name,db_pwd)
                if name == db_name and pwd == db_pwd:
                    print("数据核对成功")
                    return JsonResponse({"msg":"ok", "data":"/index/"})
            except:
                print('没有此用户！！')
                return JsonResponse({"err": "没有找到此用户！", "msg": "NO", "data": "/login/"})
            finally:
                cursor.close()
                conn.close()


def sos(request):
    if request.method == "GET":
        return render(request, "sos.html")
def wuliu(request):
    if request.method == "GET":
        return render(request, "wuliu.html")
def huiyuan(request):
    if request.method == "GET":
        return render(request,"huiyuan.html")
