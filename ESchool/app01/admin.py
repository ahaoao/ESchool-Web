from django.contrib import admin

# Register your models here.
from django.contrib import admin
from app01.models import *

# class MyAdminSite(admin.AdminSite):
#     site_header = 'ESchool大学生校园交易平台 运维资源管理系统'  # 此处设置页面显示标题
#     site_title = 'ESchool大学生校园交易平台'  # 此处设置页面头部标题
#
#
# admin_site = MyAdminSite(name='management')

admin.site.site_header = 'ESchool 运维资源管理系统'
admin.site.site_title = 'ESchool 运维资源管理系统'


# Blog模型的管理器
@admin.register(User)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'password', 'netname', 'realname', 'studentnum', 'studentpwd', 'rtime', 'zhuce_time')
    # 筛选器
    # list_filter = ('realname',)  # 过滤器
    search_fields = ('id', 'username', 'realname', 'studentnum')  # 搜索字段
    # date_hierarchy = 'zhuce_time'  # 详细时间分层筛选　
    list_editable = ['netname']


@admin.register(Sale)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'upname', 'type', 'state', 'img', 'img_name', 'price', 'tel', 'remarks', 'time', 'result',
        'result2')
    # 筛选器
    # list_filter = ('type','result','result2',)  # 过滤器
    search_fields = ('id', 'name', 'upname', 'state', 'type', 'state', 'price', 'tel', 'remarks')  # 搜索字段


@admin.register(Shops)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'ShopsName', 'introduce', 'phoneNumber', 'registrationTime', 'success_num', 'user',)
    # 筛选器
    # list_filter = ('realname',)  # 过滤器
    search_fields = ('id', 'ShopsName', 'introduce', 'phoneNumber')  # 搜索字段
    # date_hierarchy = 'zhuce_time'  # 详细时间分层筛选　


@admin.register(Commodity)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'commodityName', 'commodityIntroduce', 'commodityPrice', 'commodityNum', 'commodityTime', 'shops')
    # 筛选器
    # list_filter = ('realname',)  # 过滤器
    search_fields = (
        'id', 'commodityName', 'commodityIntroduce', 'commodityPrice', 'commodityNum', 'commodityTime')  # 搜索字段
    # date_hierarchy = 'zhuce_time'  # 详细时间分层筛选　


@admin.register(ShoppingList)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'shoppingName', 'shoppingCount', 'shoppingTime', 'shoppingMoney', 'shoppingUser', 'shoppingShops')
    # 筛选器
    # list_filter = ('realname',)  # 过滤器
    search_fields = ('id', 'shoppingName', 'shoppingCount', 'shoppingTime', 'shoppingMoney',)  # 搜索字段
    # date_hierarchy = 'zhuce_time'  # 详细时间分层筛选　


@admin.register(ShuDong)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'text', 'time', 'user')


@admin.register(LoseAndFound)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'upname', 'tel', 'text', 'type', 'time', 'count')


@admin.register(BrowseCount)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'count')
