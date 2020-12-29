
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect
import pymysql

def login(request):
    if request.method == "GET":
        return render(request,"login.html")


def dologin(request):
        print(request.POST)
        name = request.POST.get("username")
        pwd = request.POST.get("password")
        # 创建连接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123123', db='web')
        # 创建游标
        cursor = conn.cursor()
        # SQL语句：查询
        sql = "select name,password from login_info where name='%s'"
        # 异常处理
        try:
            # 执行SQL语句
            cursor.execute(sql %(name))
            # 获取所有的记录列表
            results = cursor.fetchall()
            # 遍历列表
            for row in results:
                # 姓名
                db_username = row[0]
                # 密码
                db_userpwd = row[1]
        except:
            print('Uable to fetch data!')

        # 关闭数据库连接
        conn.close()
        if db_username==name and db_userpwd==pwd:
            return JsonResponse({"status": 200, "msg": "OK", "data": "/alluser/"})
        else:
            return JsonResponse({"status": 500, "msg": "NO", "data": "失败"})

def doreg(request):
    print(request.POST)
    name = request.POST.get("username")
    pwd = request.POST.get("password")
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123123', db='web')
    # 创建游标
    cursor = conn.cursor()
    # SQL语句：查询
    sql = "insert into login_info (name,password) values ('%s','%s')"
    # 异常处理
    try:
        # 执行SQL语句
        cursor.execute(sql % (name,pwd))
        conn.commit()
        return JsonResponse({"status": 200, "msg": "ok", "data": "/alluser/"})
    except:
        conn.rollback()
        print('Insert operation error')
        raise
    finally:
        cursor.close()
        conn.close()



def reg(request):
    if request.method == "GET":
        return render(request, "reg.html")

def getpass(request):
    if request.method == "GET":
        return render(request, "getpass.html")

def alluser(request):
    if request.method=="GET":
        # 创建连接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123123', db='web')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "select * from login_info"
        try:
            cursor.execute(sql)
            # 获取所有的记录列表
            user_list = cursor.fetchall()
        except:
            print('Uable to fetch data!')

        # 关闭数据库连接
        conn.close()

        print(user_list)
        return render(request,"alluser.html",{"datalist":user_list})

def deldata(request):
    id = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123123', db='web')
    cursor = conn.cursor()
    sql = "DELETE FROM login_info WHERE id=%s"
    try:
        cursor.execute(sql % (id))
        conn.commit()
        return redirect("/alluser/")
    except:
        conn.rollback()
        print('Insert operation error')
        raise
    finally:
        cursor.close()
        conn.close()
def updata(request):
    if request.method == "GET":
        id = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123123', db='web')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "select * from login_info where id=%s"
        # sql = "UPDATE login_info SET name='%s' WHERE id = '%s'"
        try:
            cursor.execute(sql % (id))
            datalist = cursor.fetchall()
            return render(request,"updata.html",{"datalist":datalist})
        except:
            conn.rollback()
            print('Insert operation error')
            raise
        finally:
            cursor.close()
            conn.close()

    else:
        edi_id = request.POST.get("id")
        name = request.POST.get("username")
        password = request.POST.get("password")
        print(edi_id,name,password)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123123', db='web')
        cursor = conn.cursor()
        sql = "UPDATE login_info SET name='%s',password='%s' WHERE id = '%s'"
        try:
            cursor.execute(sql % (name,password,edi_id))
            conn.commit()
            return JsonResponse({"status": 200, "msg": "ok", "data": "/alluser/"})
        except:
            conn.rollback()
            print("更新失败")
            raise
        finally:
            cursor.close()
            conn.close()