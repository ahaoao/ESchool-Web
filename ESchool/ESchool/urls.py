"""ESchool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views as views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500

handler404 = views.page_not_found

handler500 = views.page_error

urlpatterns = [

                  # ESchool 大学生校园交易平台

                  # 管理员界面
                  path('admin/', admin.site.urls),
                  # 跳转至主页
                  path('', views.ESchool),
                  # 实名认证界面
                  path('renzheng.html/', views.renzheng),
                  # ESchool 条约
                  path('ty.html/', views.ty),
                  # 登录
                  path('login.html/', views.login),
                  # 退出
                  path('tuichu.html/', views.tuichu),
                  # 主页
                  path('index.html/', views.index),
                  # 注册
                  path('sign.html/', views.sign),
                  # 各个模块浏览页
                  path('ESchool.html/', views.eschool),
                  # 发布中心
                  path('Publishing_Center.html/', views.publishing_center),
                  # 发布跳转
                  path('up.html/', views.up),
                  # ESchool 免责声明
                  path('ESchool_Disclaimer.html/', views.disclaimer),
                  # 抢单操作
                  path('qiang.html/', views.qiang),
                  # 个人中心
                  path('personal_center.html/', views.personal_center),
                  # 删除操作
                  path('delete.html/', views.deletedata),
                  # 完成操作
                  path('ok.html/', views.ok),
                  # 撤单操作
                  path('revoke.html/', views.revoke),
                  # 个人资料
                  path('my.html/', views.my),

                  # 树洞
                  path('shudong.html/', views.shudong),
                  # 更新树洞数据
                  path('updata_shudong.html/', views.updata_shudong),
                  # 发布树洞
                  path('put_shudong.html/', views.put_shudong),

                  # ESchool 大学生商铺

                  # 商业街
                  path('Commercial_Street.html/', views.commercial_Street),
                  # 商铺认证
                  path('Shop_registration.html/', views.shop_registration),
                  # 开通店铺
                  path('Open_a_shop.html/', views.open_a_shop),
                  # 进入店铺
                  path('eschool_shop.html/', views.school_shop),
                  # 店铺管理
                  path('shop_management.html/', views.shop_management),
                  # 添加商品
                  path('add_shopping.html/', views.add_shopping),
                  # 修改商品
                  path('updat_shopping.html/', views.update_shopping),
                  # 结单
                  path('go_shopping.html/', views.go_shopping),
                  # 店铺数据中心
                  path('shop_center.html/', views.shop_center),
                  # 我的商铺购物记录
                  path('shop_list.html/', views.my_shop_list),
                  # 失物招领
                  path('lose_and_found.html/', views.lose_and_found),
                  # 失物招领发布
                  path('lose_publish.html/', views.lose_publish),
                  # 失物招领发布跳转
                  path('lose_up.html/', views.lose_up),

                  # 校园报修
                  path('baoxiu.html/', views.baoxiu),

                  # 表白墙
                  path('love.html/', views.love),

                  # 移动端APP下载
                  path('download_app.html', views.file_down),

                  # ESchool 手机端接口
                  path('API.html', views.iphone_api),
                  # 登录
                  path('iphone_api/login.html', views.iphone_login),
                  # 注册
                  path('iphone_api/sign.html', views.iphone_sign),
                  # 获取各个板块信息
                  path('iphone_api/get_news.html', views.iphone_get_news),
                  # 发布信息
                  path('iphone_api/up_news.html', views.iphone_up),
                  # 抢单
                  path('iphone_api/qiang.html', views.iphone_qiang),
                  # 个人中心
                  path('iphone_api/person.html', views.iphone_person),
                  # 删除
                  path('iphone_api/delete.html', views.iphone_delete),
                  # 撤单
                  path('iphone_api/chedan.html', views.iphone_chedan),
                  # 完成
                  path('iphone_api/wancheng.html', views.iphone_wancheng),
                  # 商业街
                  path('iphone_api/street.html', views.iphone_street),
                  # 进入店铺
                  path('iphone_api/street_shop.html', views.iphone_street_shop),

                  # 测试（与项目无关）
                  path('test', views.test),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
