from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User
import hashlib

# Create your views here.
# 注册
def reg_view(request):
    # 注册
    # GET 返回页面
    # POST 处理提交数据
    # 1.两个密码要保持一致
    # 2.当前用户名是否可用
    # 3.插入数据 [明文处理密码]
    if request.method == 'GET':
        return render(request, 'login/register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password_1 = request.POST['password']
        password_2 = request.POST['confirm_password']
        user_email = request.POST['email']
        user_phone = request.POST['phone_number']
        if password_1 != password_2:
            return HttpResponse('再次密码输入不一致')
        # 哈希算法 － 给定明文，计算出一段定长，不可逆的值；md5,sha-256
        # 特点
        # 1. 定长输出：不管明文输入长度为多少，哈希都是定长的，md5 - 32位16进制
        # 2, 不可逆：无法反向计算出 对应的明文
        # 3. 雪崩效应：输入改变，输出必然变
        # 场景： 1.密码处理,输出必然变
        # 如何使用
        m = hashlib.md5()
        m.update(password_1.encode())
        passwrod_m = m.hexdigest()
        # 2。当前用户名是否可用
        old_users = User.objects.filter(username=username)
        if old_users:
            return HttpResponse('用户名已注册')
        # 3. 插入数据[明文处理密码]
        try:
            user = User.objects.create(username=username, password=passwrod_m, user_phone=user_phone, user_email=user_email)
        except Exception as e:
            # 有可能 报错 - 重复插入 [唯一索引注意并发写入问题]
            print('--create user error %s' % (e))
            return HttpResponse('用户名已注册')

        # 免登录一天
        request.session['username'] = username
        request.session['uid'] = user.id
        # TODO 修改session存储时间为1天

        return HttpResponseRedirect(reverse('index:index_view'))

# 登录
def login_view(request):

    if request.method == 'GET':
        # 获取登录页面
        # 检查页面登录状态，如果登录了，显示.已登录.
        if request.session.get('username') and request.session.get('uid'):
            # return HttpResponse('已登录')
            return HttpResponseRedirect('/index/index')
        # 检查Cookies
        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        if c_username and c_uid:
            # 回写session
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            # return HttpResponse('已登录')
            return HttpResponseRedirect('/index')
        return render(request, 'login/login.html')
    elif request.method == 'POST':
        # 处理数据
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print('--login user error %s' % (e))
            return HttpResponse('用户名或密码错误')
        # 比对密码
        m = hashlib.md5()
        m.update(password.encode())

        if m.hexdigest() != user.password:
            return HttpResponse('用户名或密码错误')

        # 记录会话状态
        request.session['username'] = username
        request.session['uid'] = user.id

        # resp = HttpResponse('---登录成功---')
        resp = HttpResponseRedirect('/index/index')
        # 判断用户是否 占选了 '记住用户名'
        if 'remember' in request.POST:
            resp.set_cookie('username', username, 3600*24*3)
            resp.set_cookie('uid', user.id, 3600*24*3)
        # 点选了 -> Cookies 存储 username,uid 时间3天
        return resp

# 退出登录
def logout_view(request):

    # 删除session值
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']

    resp = HttpResponseRedirect(reverse('user:login_view'))
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp


def show_user(request, pIndex=1):
    """用户展示列表"""
    ulist = User.objects.all()
    pIndex = int(pIndex)

    # 执行分页处理
    page = Paginator(ulist, 10)  # 每页分页10条数据
    maxpages = page.num_pages

    # 判断当前页是否起越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < maxpages:
        pIndex = 1

    list2 = page.page(pIndex)  # 获取当前页的数据
    plist = page.page_range  # 获取页码信息列表

    context = {"userlist": list2, "plist": plist, "pIndex": pIndex, "maxpages": maxpages}
    return render(request, "user/all_user.html", context)


def add_user(request):
    """添加用户"""
    if request.method == 'GET':
        return render(request, "user/add_user.html")
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password_1']
        user_email = request.POST['email']
        user_phone = request.POST['phone']
        User.objects.create(username=username, password=password, user_email=user_email, user_phone=user_phone)
        return HttpResponseRedirect(reverse('user:show_user', args=(1,)))

def update_user(request, user_id):
    """更新用户"""
    try:
        user = User.objects.get(id=user_id)
    except Exception as e:
        print("--update the user information is error %s" % e)
        return HttpResponse("The user is not exist...")
    if request.method == "GET":
        return render(request, "user/update_user.html", locals())
    elif request.method == "POST":
        print("你就说成功了没有 ")

        password = request.POST["password_1"]
        user_phone = request.POST["phone"]
        user_email = request.POST["email"]
        user.user_phone = user_phone
        user.user_email = user_email
        user.password = password
        user.save()
        return HttpResponseRedirect(reverse('user:show_user', args=(1,)))

def delete_user(request):
    """删除用户"""
    user_id = request.GET['user_id']
    try:
        user = User.objects.get(id=user_id)
    except Exception as e:
        print("不存在当前用户")
        return HttpResponse("The user is not exist. %s" % (e))
    user.status = 2
    user.save()
    return HttpResponseRedirect(reverse('user:show_user', args=(1,)))

def detail_user(request, user_id):
    """用户详情"""
    try:
        user = User.objects.get(id=user_id)
    except Exception as e:
        print('error error error %s' % (e))
        return HttpResponse("no user exist")
    if request.method == "GET":
        return render(request, "user/detail_user.html", locals())