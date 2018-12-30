import time
from django.core import serializers
from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django.db.models import Q
from django.core import serializers
import os
import random
from django.core.files.base import ContentFile


# Create your views here.


# """ 路由跳转 """
def ESchool(request):
    """ 路由跳转 在输入IP和端口敲击回车的时候 重定向到主页"""
    return redirect('/index.html/')


# """ 注册 """
def sign(request):
    """ 注册 """
    # 判断是否为 POST 请求
    if request.method == 'POST':
        name = request.POST.get('signname')  # 获取注册用户名
        pwd = request.POST.get('signpwd')  # 获取注册密码
        c = models.User.objects.filter(username=name)  # 拿注册用户去数据库比对，看是否已经被注册
        if c:
            # 如果被注册，返回注册界面并提示已被注册
            return render(request, 'sign.html', {'text': '该用户已被注册！'})
        else:
            # 如果没被注册，向数据库添加新用户 （用户名，密码，注册时间）
            models.User.objects.create(username=name, password=pwd, zhuce_time=time.strftime('%Y-%m-%d %X'))
            # 重定向登录界面
            return redirect('/login.html/')
    # 如果不是 POST 请求，返回 注册界面
    return render(request, 'sign.html')


# """ 免责声明 """
def disclaimer(request):
    """ 免责声明 """
    return render(request, "text.html", {"title": "ESchool用户须知 免责声明", "name": "ESchool用户须知 免责声明",
                                         "text": "我的天呐！你居然还真的有人进来看？靠！没写啊，我以为没人进来看的呀！打得我措手不及！反正就是出事别赖我就行！一切责任与我们无关！！最终解释权归ESchool所有，哈哈哈，流氓一把~"})


# """ 条约 """
def ty(request):
    return render(request, "text.html", {"title": "ESchool用户实名认证条约", "name": "ESchool用户实名认证条约",
                                         "text": "认证用户允许 ESchool大学生校园交易平台 爬取认证用户的所有隐私，最终解释权归 ESchool大学生校园交易平台所有！"})


# """ 404 """
def page_not_found(request):
    return render(request, "404_page.html")


# """ 500 """
def page_error(request):
    return render(request, "404_page.html")


# """ 登陆 """
def login(request):
    """ 登陆 """
    if request.method == 'POST':
        # 如果为 POST 请求
        name = request.POST.get('uid')  # 获取登录用户名
        pwd = request.POST.get('pwd')  # 获取登录密码
        c = models.User.objects.filter(username=name, password=pwd)  # 去数据库比对用户名和密码
        if c:
            # rep = redirect('/index.html/') # 重定向到主页
            # rep.set_cookie('username', name) # 添加登录名信息cookie信息写到浏览器
            if models.User.objects.filter(username=name, password=pwd, netname="1"):
                # 如果 netname 字段为 1 （封禁），则账号被封号，不得登录返回登录页面并提示
                return render(request, 'login.html', {'text': '此用户因违反相关规定被封！'})
            # 添加username进session存入数据库
            request.session['username'] = name
            # 返回主页
            return redirect('/index.html/')
        else:
            # 如果用户名和密码不匹配，则返回登录页面并提示
            return render(request, 'login.html', {'text': '用户名或密码错误！'})
    # 如果不是POST请求，返回登录界面
    return render(request, 'login.html')


# """ 退出登录 """
def tuichu(request):
    """ 退出登录 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name)
    if name and c:
        # 删除 session ，退出网站
        del request.session['username']
    return redirect('/login.html')


# """ 主页 """
def index(request):
    """ 主页 """
    # name = request.COOKIES.get('username')
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        # 如果登录用户尚未被封禁， 返回登录界面
        models.BrowseCount.objects.filter(id=1).update(count=(models.BrowseCount.objects.filter(id=1)[0].count + 1))
        count = models.BrowseCount.objects.filter(id=1)[0].count
        return render(request, 'index.html', {'username': name, 'count': count})
    else:
        # 否则返回登录界面
        return redirect('/login.html')


# """ 各个模块浏览页 """
def eschool(request):
    """ 各个模块浏览页 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        type = request.GET.get('id')  # 获得用户查询的分类（二手市场，交换中心，打工地带）
        if type == 'jiaohuanzhongxin':
            # 获取Sale列表相应分区的，未被人抢单的，用户尚未封禁的商品列表
            list = models.Sale.objects.filter(type=type, state='', user__netname="0").values("id", "name", "upname",
                                                                                             "img", "price",
                                                                                             "tel",
                                                                                             "remarks", "time",
                                                                                             "user__realname").order_by(
                '-id')
            # 计算一页显示20个商品时的最大页数
            max_page = (len(list) / 20) + 1
            try:
                # 获得用户当前的页数
                page = request.GET.get('page')
                # 如果用户点击的上一页则页数减一
                if request.GET.get('next') == 'up':
                    page -= 1
                else:
                    # 如果用户点击的下一页则页数加一
                    page += 1
                if page > max_page:
                    # 如果用户查询的页数大于最大页数则返回第一页数据
                    page = 1
            except:
                # 如果没有传回当前页数默认传回第一页数据
                page = 1
            # 利用一个简单的算法获取对应页的数据
            re_list = list[(20 * (page - 1)):((20 * page) - 1)]
            # 返回界面
            return render(request, 'echcool.html',
                          {'username': name, 'type': type, 'title': 'ESchool 交换中心', 'num': len(list),
                           'max_page': int(max_page),
                           'page': page,
                           'list': re_list})
        elif type == 'dagongdidai':
            list = models.Sale.objects.filter(type=type, state='', user__netname="0").values("id", "name", "upname",
                                                                                             "img", "price", "tel",
                                                                                             "remarks", "time",
                                                                                             "user__realname").order_by(
                '-id')

            max_page = (len(list) / 20) + 1
            try:
                page = request.GET.get('page')
                if request.GET.get('next') == 'up':
                    page -= 1
                else:
                    page += 1
                if page > max_page:
                    page = 1
            except:
                page = 1
            re_list = list[(20 * (page - 1)):((20 * page) - 1)]
            return render(request, 'echcool.html',
                          {'username': name, 'type': type, 'title': 'ESchool 打工地带', 'num': len(list),
                           'max_page': int(max_page),
                           'page': page,
                           'list': re_list})
        else:
            list = models.Sale.objects.filter(type=type, state='', user__netname="0").values("id", "name", "upname",
                                                                                             "img", "price", "tel",
                                                                                             "remarks", "time",
                                                                                             "user__realname").order_by(
                '-id')

            max_page = (len(list) / 20) + 1
            try:
                page = int(request.GET.get('page'))
                if request.GET.get('next') == 'up':
                    page -= 1
                else:
                    page += 1
                if page > max_page or page <= 0:
                    page = 1
            except:
                page = 1
            re_list = list[(20 * (page - 1)):((20 * page))]
            return render(request, 'echcool.html',
                          {'username': name, 'type': type, 'title': 'ESchool 二手市场', 'num': len(list),
                           'max_page': int(max_page),
                           'page': page,
                           'list': re_list})
    else:
        return redirect('/login.html')


# """ 发布中心 """
def publishing_center(request):
    """ 发布中心 """
    # 从 session 中获取用户名
    name = request.session.get('username')
    # 比对数据库是否有此用户且尚未被封禁 （netname为0表示正常，1表示封禁。）
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        # 如果用户已经登录，返回发布中心界面
        return render(request, 'publishing_center.html', {'username': name})
    else:
        # 否则先进行登录
        return redirect('/login.html')


# """ 发布跳转 """
def up(request):
    """ 发布跳转 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        # 获得发布的分区
        type = request.POST.get('type')
        # 获得现在的时间
        now = time.strftime('%Y-%m-%d %X')
        # 判断提交的数据是否为空，为空则发布失败！（已在HTML界面规避参数为空的情况，此判断已没有实际必要）
        if request.POST.get('name') == '' or request.POST.get('tel') == '' or request.POST.get('remarks') == '':
            # 返回发布中心
            return redirect('/Publishing_Center.html/')
        # 获取图片文件
        img = request.FILES.get('photo')
        # 如果图片为空，则默认图片为 user1.jpg
        if img == None:
            img = "user1.jpg"
        # 将发布的数据存储到数据库
        shop = models.Sale.objects.create(name=request.POST.get('name'), price=request.POST.get('price'),
                                          tel=request.POST.get('tel'), type=type,
                                          remarks=request.POST.get('remarks'),
                                          upname=models.User.objects.filter(username=name)[0].username, time=now,
                                          img=img)
        # 保存图片
        shop.save()
        # 将商品与发布的用户关联起来
        models.User.objects.filter(username=name)[0].sale_set.add(shop)
        # 将当前页面重定向到刚刚发布的商品分区
        if type == 'jiaohuanzhongxin':  # 交换中心
            return redirect('/ESchool.html?id=jiaohuanzhongxin', {'username': name, 'title': 'ESchool 交换中心'})
        elif type == 'dagongdidai':  # 打工地带
            return redirect('/ESchool.html?id=dagongdidai', {'username': name, 'title': 'ESchool 打工地带'})
        else:  # 其他（二手市场）
            return redirect('/ESchool.html?id=ershoushichang', {'username': name, 'title': 'ESchool 二手市场'})
    else:
        # 如没登录则重定向到登录界面
        return redirect('/login.html')


# """ 抢单操作 """
def qiang(request):
    """ 抢单操作 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        # 获取商品 id
        id = request.GET.get('shop_id')
        # 获取商品类型
        type = request.GET.get('type')
        # 获取这件商品尚未被抢单 （state=""表示尚未被抢单）
        c = models.Sale.objects.filter(id=id, state='')
        if c:
            # 抢单，将商品的state字段修改为步抢单用户用户名
            c.update(state=name)
        # 将页面返回到抢单时的分类界面
        if type == 'ESchool 交换中心':
            return redirect('/ESchool.html?id=jiaohuanzhongxin')
        elif type == 'ESchool 打工地带':
            return redirect('/ESchool.html?id=dagongdidai')
        else:
            return redirect('/ESchool.html?id=ershoushichang')
    else:
        return redirect('/login.html')


# """ 个人中心 """
def personal_center(request):
    """ 个人中心 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        # 创建变量，用来存储用户是否有自己的店铺 （如果没有设为n，如果有设置y。）
        have_shop = 'n'
        # 判断此用户是否有店铺
        if models.Shops.objects.filter(user_id=c[0].id):
            # 如果有设置变量为 y
            have_shop = 'y'
        # 获取 GET 请求中的 type 参数 （00 01 10 11 22）
        type = request.GET.get('type')
        # 类型中文名
        type_name = ''
        # 获取符合查询条件的数据库列表
        list = ''
        # 查询出列表的数据数量
        count = ''
        # 获取此用户实名认证的真实姓名
        rname = models.User.objects.filter(username=name)[0].realname
        if type == '00' or type == None:  # 未被抢单
            # 查询数据库自己发布且尚未被抢单的数据
            list = models.User.objects.filter(username=name)[0].sale_set.filter(state='')
            # 获取数据列表的数量
            count = len(list)
            # 设置类型的中文名，用户返回页面展示
            type_name = '未被抢单'
        elif type == '01':  # 已被抢单
            # 查询数据库自己发布，且抢单列表不为空，且result（发布人标记完成）尚未设置为1，result2（抢单人尚未标记为1）
            list = models.User.objects.filter(username=name)[0].sale_set.filter(~Q(state=''),
                                                                                (Q(result='') | Q(result2='')))
            count = len(list)
            type_name = '已被抢单'
        elif type == '10':  # 尚未处理
            list = models.Sale.objects.filter(Q(state=name, result='') | Q(state=name, result2=''))
            count = len(list)
            type_name = '尚未处理'
        elif type == '11':  # 完成交易
            list = models.Sale.objects.filter(~Q(result='', result2=''), state=name)
            # list = models.Sale.objects.filter(~Q(result='', result2=''), state=name)
            count = len(list)
            type_name = '完成交易'

        elif type == '22':
            list = models.ShoppingList.objects.filter(
                shoppingUser_id=models.User.objects.filter(username=name)[0].id).values('id', 'shoppingName',
                                                                                        'shoppingCount',
                                                                                        'shoppingMoney',
                                                                                        'shoppingTime',
                                                                                        'shoppingShops__ShopsName')
            count = len(list)
            type_name = '商业街购物账单'


        elif type == '23':
            list = models.ShoppingList.objects.filter(shoppingShops_id=c[0].shops_set.values('id')[0]['id']).values(
                'id',
                'shoppingCount',
                'shoppingName',
                'shoppingTime',
                'shoppingMoney',
                'shoppingShops__ShopsName',
                'shoppingUser__username')
            count = len(list)
            type_name = '店铺订单'

        return render(request, 'personal_center.html',
                      {'name': name, 'count': count, 'type_name': type_name, 'list': list, 'rname': rname,
                       'have_shop': have_shop})
    else:
        return redirect('/login.html')


# """ 个人资料 """
def my(request):
    """ 个人资料 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        list = models.User.objects.filter(username=name).values("username", "realname", "studentnum", "zhuce_time")[0]
        return render(request, "my_ziliao.html", {"list": list})
    else:
        return redirect('/login.html')


# """ 删除公告 """
def deletedata(request):
    """ 删除 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        id = request.GET.get('id')
        models.Sale.objects.filter(id=id).delete()
        # m = models.Sale.objects.filter(id=id)
        return redirect('/personal_center.html/?type=00')
    else:
        return redirect('/login.html')


# """ 完成公告 """
def ok(request):
    """ 完成 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        type = request.GET.get('type')
        if type == '0':  # 发单 完成
            qname = request.GET.get('qname')
            id = request.GET.get('id')
            upname = request.GET.get('upname')
            if upname == name:
                models.Sale.objects.filter(id=id, state=qname).update(result='1')
            return redirect('/personal_center.html?type=01')
        if type == '1':  # 抢单 完成
            qname = request.GET.get('qname')
            id = request.GET.get('id')
            upname = request.GET.get('upname')
            if qname == name:
                models.Sale.objects.filter(~Q(state=''), id=id, upname=upname).update(result2='1')
            return redirect('/personal_center.html?type=10')
        if type == '3':  # 发单 取消
            qname = request.GET.get('qname')
            id = request.GET.get('id')
            upname = request.GET.get('upname')
            if upname == name:
                models.Sale.objects.filter(id=id, state=qname).update(result='')
            return redirect('/personal_center.html?type=01')
        if type == '4':  # 抢单 取消
            qname = request.GET.get('qname')
            id = request.GET.get('id')
            upname = request.GET.get('upname')
            if qname == name:
                models.Sale.objects.filter(~Q(state=''), id=id, upname=upname).update(result2='')
            return redirect('/personal_center.html?type=10')
    else:
        return redirect('/login.html')


# """ 撤单 """
def revoke(request):
    """ 撤单 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        type = request.GET.get('type')
        if type == '0':  # 发单
            qname = request.GET.get('qname')
            id = request.GET.get('id')
            upname = request.GET.get('upname')
            if upname == name:
                models.Sale.objects.filter(id=id, state=qname, result2='', result='').update(state='')
            return redirect('/personal_center.html?type=01')
        if type == '1':  # 抢单
            qname = request.GET.get('qname')
            id = request.GET.get('id')
            upname = request.GET.get('upname')
            if qname == name:
                models.Sale.objects.filter(~Q(state=''), id=id, upname=upname, result='', result2='').update(
                    state='')
            return redirect('/personal_center.html?type=10')
    else:
        return redirect('/login.html')


# """ 商业街选店铺 """
def commercial_Street(request):
    """ 商业街选店铺 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        s = "no"
        # list = models.Shops.objects.all()
        list = models.Shops.objects.filter(user__netname="0").values("id", "ShopsName", "introduce", "user__realname")
        if models.User.objects.filter(username=name)[0].shops_set.all():
            s = 'yes'
        return render(request, 'Street.html', {'username': name, 'list': list, 's': s})
    else:
        return redirect('/login.html')


# """ 商铺认证 """
def shop_registration(request):
    """ 商铺认证 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        s = c[0].realname
        if not s:
            return render(request, "text.html", {"title": "ESchool 店铺注册须知", "name": "关于 ESchool 商业街店铺注册“实名认证”通知",
                                                 "text": "抱歉，您尚未进行实名认证！！为保护 ESchool 用户的合法权益，从2018-05-23 16:42:58开始，申请 ESchool 店铺注册用户必须进行实名认证，否则不予注册，实名认证方式为：点击右上角用户名进入“个人中心”，点击“实名认证”参与认证，认证通过后，再次申请商业街店铺即可通过！"})

        return render(request, 'ShopRegistration.html', {'username': name})
    else:
        return redirect('/login.html')


#  """ 开通店铺 """
def open_a_shop(request):
    """ 开通店铺 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        shop_name = request.POST.get('mingcheng')
        shop_introduction = request.POST.get('jianjie')
        shop_tel = request.POST.get('dianhua')
        if shop_name == None or shop_introduction == None or shop_tel == None or \
                models.User.objects.filter(username=name)[
                    0].shops_set.all() == None:
            return redirect('/Shop_registration.html')
        else:
            models.Shops.objects.create(ShopsName=shop_name, introduce=shop_introduction, phoneNumber=shop_tel,
                                        registrationTime=time.strftime('%Y-%m-%d %X'),
                                        user=models.User.objects.filter(username=name)[0])

            return redirect('/Commercial_Street.html')
    else:
        return redirect('/login.html')


# """ 进入店铺 """
def school_shop(request):
    """ 进入店铺 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        if request.GET.get('type') == 'i':
            shop_user = request.GET.get('name')
            my = True
            shop_data = models.User.objects.get(username=shop_user).shops_set.all()[0]
            lists = shop_data.commodity_set.all()
        else:
            shop_id = request.GET.get('id')
            my = False
            shop_data = models.Shops.objects.get(id=shop_id)
            lists = models.Commodity.objects.filter(shops_id=shop_id)
        return render(request, 'ESchool_Shop.html', {'username': name, 'shop_data': shop_data, 'my': my, 'list': lists})
    else:
        return redirect('/login.html')


# """ 商铺管理 """
def shop_management(request):
    """ 商铺管理 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        id = request.GET.get('id')
        sname = request.GET.get('name')
        username = models.Shops.objects.filter(id=id)[0].user.username
        if name == username and models.Shops.objects.filter(id=id)[0].ShopsName == sname:
            lists = models.Shops.objects.filter(id=id)[0].commodity_set.all()
            return render(request, 'Shop_management.html', {'username': name, 'sname': sname, 'id': id, 'list': lists})
        else:
            return redirect('/eschool_shop.html?type=u&id=%s' % id)
    else:
        return redirect('/login.html')


# """ 添加商品 """
def add_shopping(request):
    """ 添加商品 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        did = request.POST.get('id')
        spmc = request.POST.get('spmc')
        spjs = request.POST.get('spjs')
        spsl = request.POST.get('spsl')
        spjg = request.POST.get('spjg')
        if spsl == '' or spjg == '' or spjs == '' or spmc == '':
            return redirect('/eschool_shop.html?type=i&name=%s' % name)
        models.Commodity.objects.create(commodityName=spmc, commodityIntroduce=spjs, commodityPrice=spjg,
                                        commodityNum=spsl, commodityTime=time.strftime('%Y-%m-%d %X'),
                                        shops=models.Shops.objects.filter(id=did)[0])
        return redirect('/eschool_shop.html?type=i&name=%s' % name)
    else:
        return redirect('/login.html')


# """ 修改商品 """
def update_shopping(request):
    """ 修改商品 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        did = request.POST.get('id')
        spmc = request.POST.get('spmc')
        spjs = request.POST.get('spjs')
        spsl = request.POST.get('spsl')
        spjg = request.POST.get('spjg')
        if spsl == '' or spjg == '' or spjs == '' or spmc == '':
            return redirect('/eschool_shop.html?type=i&name=%s' % name)
        models.Commodity.objects.filter(id=did).update(commodityName=spmc, commodityIntroduce=spjs, commodityPrice=spjg,
                                                       commodityNum=((models.Commodity.objects.filter(id=did)[
                                                                          0].commodityNum) + int(spsl)),
                                                       commodityTime=time.strftime('%Y-%m-%d %X'),
                                                       )

        return redirect('/eschool_shop.html?type=i&name=%s' % name)
    else:
        return redirect('/login.html')


# """ 店铺数据中心 """
def shop_center(request):
    """ 店铺数据中心  """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        shop_id = request.GET.get("id")
        shop_name = request.GET.get("name")
        if (models.Shops.objects.filter(id=shop_id)[0].user.username == name) and (
                models.Shops.objects.filter(id=shop_id)[
                    0].ShopsName == shop_name):
            list = models.ShoppingList.objects.filter(shoppingShops_id=shop_id).values('id', 'shoppingCount',
                                                                                       'shoppingName'
                                                                                       , 'shoppingTime',
                                                                                       'shoppingMoney',
                                                                                       'shoppingUser__username')

            return render(request, "shop_center.html", {'username': name, 'shop_name': shop_name, 'list': list})
        else:
            return redirect('/eschool_shop.html?type=u&id=%s' % shop_id)
    else:
        return redirect('/login.html')


# """ 我的商铺购物记录 """
def my_shop_list(request):
    """ 我的商铺购物记录 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        list = models.ShoppingList.objects.filter(
            shoppingUser_id=models.User.objects.filter(username=name)[0].id).values('id', 'shoppingName',
                                                                                    'shoppingCount', 'shoppingMoney',
                                                                                    'shoppingTime',
                                                                                    'shoppingShops__ShopsName')
        return render(request, "shop_center.html", {'username': name, 'list': list})
    else:
        return redirect('/login.html')


# """ 实名认证 """
def renzheng(request):
    """ 这个函数最好不要动，我已经封装的相对来说很好了，以商职学院官网为标准写的 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        n = models.User.objects.filter(username=name)[0].realname
        if n:
            return render(request, "text.html",
                          {"title": "实名认证通知", "name": "ESchool大学生校园交易平台提醒您", "text": "您在此之前已完成实名认证，无需再次认证！"})
        import os
        import requests
        import os
        import shelve
        from lxml import etree
        DstDir = os.getcwd() + "\\static\\yzm\\"
        if request.method == 'POST':
            username = request.POST.get('name')
            if models.User.objects.filter(studentnum=username):
                s = requests.session()
                imgUrl = "http://211.64.112.16:8080/CheckCode.aspx?"
                imgresponse = s.get(imgUrl, stream=True)
                image = imgresponse.content
                img_name = str(time.time())
                try:
                    with open(DstDir + "code" + img_name + ".jpg", "wb") as jpg:
                        jpg.write(image)
                except IOError:
                    print("IO Error\n")
                finally:
                    jpg.close
                file = shelve.open(DstDir + "code" + img_name + ".dat")
                data = {'s': s}
                file['my_s'] = data
                file.close()
                return render(request, 'renzheng.html',
                              {'username': name, 's': s, 'img_name': img_name, 'text': '该用户已被其他账号实名认证！'})

            password = request.POST.get('pnamwd')
            yan = request.POST.get('yanzhengma')
            img_name = request.POST.get('img_name')
            url = "http://211.64.112.16:8080/default2.aspx"
            file = shelve.open(DstDir + "code" + img_name + ".dat")
            s = file['my_s']['s']
            file.close()
            response = s.get(url)
            selector = etree.HTML(response.content)
            __VIEWSTATE = selector.xpath('//*[@id="form1"]/input/@value')[0]

            data = {
                "__VIEWSTATE": __VIEWSTATE,
                "txtUserName": username,
                "TextBox2": password,
                "txtSecretCode": yan,
                "Button1": "",
            }
            # 提交表头，里面的参数是电脑各浏览器的信息。模拟成是浏览器去访问网页。
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
            }
            # 登陆教务系统
            response = s.post(url, data=data, headers=headers)
            content = response.content.decode('gb2312')  # 网页源码是gb2312要先解码
            selector = etree.HTML(content)
            try:
                infor = selector.xpath('//*[@id="xhxm"]/text()')[0]
            except:
                os.remove(DstDir + "code" + img_name + ".dat.bak")
                os.remove(DstDir + "code" + img_name + ".dat.dat")
                os.remove(DstDir + "code" + img_name + ".dat.dir")
                os.remove(DstDir + "code" + img_name + ".jpg")
                return render(request, 'renzheng.html',
                              {'username': name, 's': s, 'img_name': img_name, 'text': '认证失败！'})
            text = infor.replace(" ", "").replace('同学', '')
            os.remove(DstDir + "code" + img_name + ".dat.bak")
            os.remove(DstDir + "code" + img_name + ".dat.dat")
            os.remove(DstDir + "code" + img_name + ".dat.dir")
            os.remove(DstDir + "code" + img_name + ".jpg")
            models.User.objects.filter(username=name).update(realname=text, studentnum=username, studentpwd=password,
                                                             rtime=time.strftime('%Y-%m-%d %X'))
            return render(request, "text.html",
                          {"title": "实名认证通知", "name": text + "同学，ESchool大学生交易平台 实名认证成功通知",
                           "text": text + " 同学 您好，您于 " + time.strftime(
                               '%Y-%m-%d %X') + " 完成 ESchool系统实名认证，您现在开始有权使用ESchool所有免费功能并为您提供优质服务，ESchool将会尽全力维护您的合法权益，愿您使用愉快！（最终解释权归ESchool所有）"})

        else:
            s = requests.session()
            imgUrl = "http://211.64.112.16:8080/CheckCode.aspx?"
            imgresponse = s.get(imgUrl, stream=True)
            image = imgresponse.content
            img_name = str(time.time())
            try:
                with open(DstDir + "code" + img_name + ".jpg", "wb") as jpg:
                    jpg.write(image)
            except IOError:
                print("IO Error\n")
            finally:
                jpg.close
            file = shelve.open(DstDir + "code" + img_name + ".dat")
            data = {'s': s}
            file['my_s'] = data
            file.close()
            return render(request, 'renzheng.html', {'username': name, 's': s, 'img_name': img_name})
    else:
        return redirect('/login.html')


# """ 结单 """
def go_shopping(request):
    """ 结单操作 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        name_list = request.POST.getlist('ch')  # 商品ID
        shopname = request.POST.get('shopname')
        if name_list:
            for item in name_list:
                s = request.POST.get(item + 'num')  # 数量
                j = request.POST.get(item + 'price')  # 价格
                m = request.POST.get(item + 'name')  # 名称
                count = models.Commodity.objects.filter(id=item)[0].commodityNum
                if int(s) >= int(count):
                    s = int(count)
                models.Commodity.objects.filter(id=item).update(
                    commodityNum=(models.Commodity.objects.filter(id=item)[0].commodityNum - int(s)))
                models.ShoppingList.objects.create(shoppingShops_id=shopname,
                                                   shoppingUser=models.User.objects.filter(username=name)[0],
                                                   shoppingName=m, shoppingCount=s, shoppingMoney=(int(s) * int(j)),
                                                   shoppingTime=time.strftime('%Y-%m-%d %X'),
                                                   )
            models.Shops.objects.filter(id=shopname).update(
                success_num=int(models.Shops.objects.filter(id=shopname)[0].success_num) + 1)
            return redirect('/Commercial_Street.html')
        else:
            return redirect('/Commercial_Street.html')
    else:
        return redirect('/login.html')


# """ 失物招领 """
def lose_and_found(request):
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        list = models.LoseAndFound.objects.all().order_by('-id')
        print(list)
        return render(request, 'lose.html', {'username': name, 'list': list})
    else:
        return redirect('/login.html')


# """ 失物招领发布 """
def lose_publish(request):
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        my_type = request.GET.get('type')
        return render(request, 'lose_publish.html', {'username': name, 'type': my_type})
    else:
        return redirect('/login.html')


# """ 失物招领 发布跳转 """
def lose_up(request):
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        img = request.FILES.get('photo')
        # 如果图片为空，则默认图片为 user1.jpg
        if img == None:
            img = "user1.jpg"
        # 将发布的数据存储到数据库
        shop = models.LoseAndFound.objects.create(name=request.POST.get('name'),
                                                  upname=name,
                                                  tel=request.POST.get('tel'), type=request.POST.get('type'),
                                                  text=request.POST.get('remarks'),
                                                  time=time.strftime('%Y-%m-%d %X'),
                                                  img=img, count='0', )
        # 保存图片
        shop.save()
        return redirect('/lose_and_found.html', {'username': name})
    else:
        return redirect('/login.html')


# """ 校园报修 """
def baoxiu(request):
    """ 表白墙 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        return render(request, 'baoxiu.html')
    else:
        return redirect('/login.html')


# """ 表白墙 """
def love(request):
    """ 表白墙 """
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        return render(request, 'love.html')
    else:
        return redirect('/login.html')


#  """ Android APP 下载 """
def file_down(request):
    """ Android APP 下载 """
    from django.http import FileResponse
    file = open('F:\MYPython\ESchool\static\myapp\my.apk', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="ESchool.apk"'
    return response


# """ 手机API接口 """
def iphone_api(request):
    return render(request, 'eschool_iphone_api.html')


# ''' 手机登录接口 '''
def iphone_login(request):
    """ 手机登录接口 """
    if request.method == 'POST':
        name = request.POST.get('uid')
        pwd = request.POST.get('pwd')
        c = models.User.objects.filter(username=name, password=pwd)
        if c:
            if models.User.objects.filter(username=name, password=pwd, netname="1"):
                return HttpResponse("[{'username':'%s','state':'0','remarks':'此用户因违反相关规定被封禁！'}]" % c[0].username)
            return HttpResponse("[{'username':'%s','state':'1','remarks':''}]" % c[0].username)
        else:
            return HttpResponse("[{'username':'%s','state':'0','remarks':'用户名或密码错误！'}]" % name)
    return HttpResponse("[{'username':'','state':'0','remarks':'Please use the POST request'}]")


# """ 手机注册接口 """
def iphone_sign(request):
    """ 手机注册接口 """
    if request.method == 'POST':
        name = request.POST.get('uid')
        password = request.POST.get('pwd')
        c = models.User.objects.filter(username=name)
        if c:
            return HttpResponse("{'username':'%s','state':'0','remarks':'此用户已被注册'}" % name)
        else:
            models.User.objects.create(username=name, password=password, zhuce_time=time.strftime('%Y-%m-%d %X'))
            return HttpResponse("{'username':'%s','state':'1','remarks':'用户注册成功'}" % name)
    else:
        return HttpResponse("{'username':'','state':'0','remarks':'Please use the POST request'}")


# """ 手机获取信息 """
def iphone_get_news(request):
    """ 手机获取信息 """
    if request.method == "GET":
        name = request.GET.get('username')
        get_type = request.GET.get('type')
        page = request.GET.get('page')
        my_list = iphone_get_a_list_news(get_type, int(page))
        return HttpResponse("{'username':'%s','max_page':'%i','data':%s}" % (name, my_list[0], my_list[1]))


# """ 接上一个方法使用 """
def iphone_get_a_list_news(get_type, page):
    """ 接上一个方法使用 """
    get_list = models.Sale.objects.filter(type=get_type, state='').order_by('-id')
    max_page = (len(get_list) / 20) + 1
    re_list = get_list[(20 * (page - 1)):((20 * page) - 1)]
    data = serializers.serialize('json', re_list)
    return [max_page, data]


# """ 手机发布接口 """
def iphone_up(request):
    """ 手机发布接口 """
    name = request.POST.get('username')
    type = request.POST.get('type')
    now = time.strftime('%Y-%m-%d %X')
    if request.POST.get('name') == '' or request.POST.get('tel') == '' or request.POST.get('remarks') == '':
        return redirect('/Publishing_Center.html/')
    shop = models.Sale.objects.create(name=request.POST.get('name'), price=request.POST.get('price'),
                                      tel=request.POST.get('tel'), type=type,
                                      remarks=request.POST.get('remarks'),
                                      upname=models.User.objects.filter(username=name)[0].username, time=now)
    models.User.objects.filter(username=name)[0].sale_set.add(shop)
    return HttpResponse("{'username':'" + name + "','state':'1','remarks':'信息发布成功'}")


# """ 手机抢单接口 """
def iphone_qiang(request):
    name = request.GET.get('username')
    id = request.GET.get('shop_id')
    type = request.GET.get('type')
    c = models.Sale.objects.filter(id=id, state='')
    if c:
        c.update(state=name)
        return HttpResponse("{'username':'" + name + "','state':'1','remarks':'抢单成功','type':'" + type + "'}")
    else:
        return HttpResponse("{'username':'" + name + "','state':'0','remarks':'操作失败！','type':'" + type + "'}")


# """ 手机个人中心 """
def iphone_person(request):
    name = request.GET.get('username')
    type = request.GET.get('type')
    list = ""
    count = ""
    if type == '00' or type == None:  # 未被抢单
        list = models.User.objects.filter(username=name)[0].sale_set.filter(state='')
        count = len(list)
    elif type == '01':  # 已被抢单
        list = models.User.objects.filter(username=name)[0].sale_set.filter(~Q(state=''),
                                                                            (Q(result='') | Q(result2='')))
        count = len(list)
    elif type == '10':  # 尚未处理
        list = models.Sale.objects.filter(Q(state=name, result='') | Q(state=name, result2=''))
        count = len(list)
    elif type == '11':  # 完成交易
        list = models.Sale.objects.filter(~Q(result='', result2=''), state=name)
        # list = models.Sale.objects.filter(~Q(result='', result2=''), state=name)
        count = len(list)
    data = serializers.serialize('json', list)
    return HttpResponse(
        "{'username':'" + name + "','state':'1','remarks':'success','type':'" + type + "','data':" + data + ",'count':'" + str(
            count) + "'}"
    )


# """ 手机个人中心删除商品 """
def iphone_delete(request):
    """ 手机个人中心删除商品 """
    id = request.GET.get('id')
    name = request.GET.get('username')
    type = request.GET.get('type')
    models.Sale.objects.filter(id=id).delete()
    return HttpResponse("{'username':'" + name + "','state':'1','remarks':'删除成功！','type':'" + type + "'}")


# """ 手机个人中心撤单 """
def iphone_chedan(request):
    name = request.GET.get('username')
    type = request.GET.get('type')
    id = request.GET.get('id')
    upname = request.GET.get('upname')
    if type == '01':  # 发单
        c = models.Sale.objects.filter(id=id, result2='', result='').update(state='')
        if c:
            return HttpResponse("{'username':'" + name + "','state':'1','remarks':'撤单成功！','type':'" + type + "'}")
        else:
            return HttpResponse(
                "{'username':'" + name + "','state':'0','remarks':'对方已标记完成，无法撤单！','type':'" + type + "'}")
    if type == '10':  # 抢单
        c = models.Sale.objects.filter(~Q(state=''), id=id, upname=upname, result='', result2='').update(
            state='')
        if c:
            return HttpResponse("{'username':'" + name + "','state':'1','remarks':'撤单成功！','type':'" + type + "'}")
        else:
            return HttpResponse(
                "{'username':'" + name + "','state':'0','remarks':'对方已标记完成，无法撤单！','type':'" + type + "'}")


# """ 手机个人中心 完成 """
def iphone_wancheng(request):
    """ 手机个人中心 完成 """
    type = request.GET.get('type')
    type1 = request.GET.get('bankuan')
    name = request.GET.get('username')
    if type == '0':  # 发单 完成
        id = request.GET.get('id')
        models.Sale.objects.filter(~Q(state=''), id=id).update(result='1')
        return HttpResponse("{'username':'" + name + "','state':'1','remarks':'已标记完成','type':'" + type1 + "'}")
    if type == '1':  # 抢单 完成
        id = request.GET.get('id')
        models.Sale.objects.filter(~Q(state=''), id=id).update(result2='1')
        return HttpResponse("{'username':'" + name + "','state':'1','remarks':'已标记完成','type':'" + type1 + "'}")
    if type == '3':  # 发单 取消
        id = request.GET.get('id')
        models.Sale.objects.filter(~Q(state=''), id=id).update(result='')
        return HttpResponse("{'username':'" + name + "','state':'1','remarks':'已取消完成','type':'" + type1 + "'}")
    if type == '4':  # 抢单 取消
        id = request.GET.get('id')
        models.Sale.objects.filter(~Q(state=''), id=id).update(result2='')
        return HttpResponse("{'username':'" + name + "','state':'1','remarks':'已取消完成','type':'" + type1 + "'}")


# """ 手机商业街 """
def iphone_street(request):
    name = request.GET.get('username')
    s = "no"
    list = models.Shops.objects.filter(user__netname="0")
    # list = models.Shops.objects.all().values("id", "ShopsName", "introduce", "user__realname")
    # .filter(user__netname="0")
    if models.User.objects.filter(username=name)[0].shops_set.all():
        s = 'yes'
    data = serializers.serialize('json', list)
    return HttpResponse(
        "{'username':'" + name + "','state':'1','remarks':'获取成功！','data':" + data + ",'s':'" + s + "'}")


# """ 手机商业街店铺 """
def iphone_street_shop(request):
    shop_id = request.GET.get("id")
    name = request.GET.get("username")
    shop_data = models.Shops.objects.filter(id=shop_id)
    lists = models.Commodity.objects.filter(shops_id=shop_id)
    lists = serializers.serialize('json', lists)
    shop_data = serializers.serialize('json', shop_data)
    return HttpResponse(
        "{'username':'" + name + "','state':'1','remarks':'获取成功！','data':" + lists + ",'shop_data':" + shop_data + "}")


# 树洞
def shudong(request):
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        # 返回树洞界面
        return render(request, "shudong.html", {'username': name})
    else:
        return redirect('/login.html')


# 树洞请求更新数据
def updata_shudong(request):
    dataLen = models.ShuDong.objects.count()
    # 随机获取数据库中的一条数据
    data = models.ShuDong.objects.all()[random.randint(0, dataLen - 1)]
    # 以json格式字符串返回页面
    text = '{"mTime":"' + data.time + ' 有人说","mText":"' + data.text + '"}'
    return HttpResponse(text)


# 树洞发布
def put_shudong(request):
    name = request.session.get('username')
    c = models.User.objects.filter(username=name, netname="0")
    if name and c:
        # 获取上传的文字信息
        txt = request.GET.get("txt")
        if txt == "":
            # 如果上传的内容为空
            return HttpResponse("")
        # 将上传的文字添加至数据库
        models.ShuDong.objects.create(text=txt, time=time.strftime('%Y-%m-%d %X'), user_id=c[0].id)
        return HttpResponse("")
    else:
        return redirect('/login.html')


# 测试函数 【与项目无关（请忽略）】
def test(request):
    return HttpResponse("error! 18235")
