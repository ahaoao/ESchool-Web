from django.db import models

import json


# Create your models here.

# 创建用户数据表
class User(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    netname = models.CharField(max_length=32, default='0', verbose_name='封禁状态')
    realname = models.CharField(max_length=32, default="", verbose_name='真实姓名', null=True, blank=True)
    studentnum = models.CharField(max_length=32, default="", verbose_name='学号', null=True, blank=True)
    studentpwd = models.CharField(max_length=32, default="", verbose_name='学校官网密码', null=True, blank=True)
    rtime = models.CharField(max_length=32, default="", verbose_name='实名认证时间', null=True, blank=True)
    zhuce_time = models.CharField(max_length=32, default="", verbose_name='账号注册时间')

    class Meta:
        db_table = 'user'
        verbose_name = "ESchool注册用户"

    def toJSON(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))


# 存放售卖数据表
class Sale(models.Model):
    name = models.CharField(max_length=32, verbose_name='商品名称')
    upname = models.CharField(max_length=32, verbose_name='发单用户')
    type = models.CharField(max_length=32, default='', verbose_name='分区')
    state = models.CharField(max_length=32, default='', verbose_name='抢单用户')
    img = models.ImageField(upload_to='', default='user1.jpg', verbose_name='图片')
    img_name = models.CharField(max_length=32, default="", verbose_name='图片名称')
    price = models.CharField(max_length=32, verbose_name='价格')
    tel = models.CharField(max_length=32, verbose_name='电话')
    remarks = models.CharField(max_length=128, verbose_name='简介')
    time = models.CharField(max_length=32, verbose_name='发布时间')
    result = models.CharField(max_length=32, default='', verbose_name='发单完成确认')
    result2 = models.CharField(max_length=32, default='', verbose_name='抢单完成确认')
    user = models.ManyToManyField('User', verbose_name='发布用户')

    class Meta:
        db_table = 'sale'
        verbose_name = "发布商品"

    def toJSON(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))


# ESchool 大学生校园交易平台  商业街数据结构
class Shops(models.Model):
    """商铺数据表"""
    ShopsName = models.CharField(max_length=32, verbose_name='商铺名称')  # 商铺名称
    introduce = models.CharField(max_length=128, verbose_name='商铺简介')  # 商铺简介
    phoneNumber = models.CharField(max_length=32, verbose_name='客服电话')  # 手机号码
    registrationTime = models.CharField(max_length=32, verbose_name='注册时间')  # 注册时间
    success_num = models.CharField(max_length=32, default='0', verbose_name='交易次数')  # 交易成功次数
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='注册用户')  # 关联用户（注册用户）

    class Meta:
        verbose_name = "商业街店铺"

    def toJSON(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))


class Commodity(models.Model):
    """商品数据表"""
    commodityName = models.CharField(max_length=32, verbose_name='商品名称')  # 商品名称
    commodityIntroduce = models.CharField(max_length=128, verbose_name='商品介绍')  # 商品介绍
    commodityPrice = models.IntegerField(default=0, verbose_name='商品价格')  # 商品价格
    commodityNum = models.IntegerField(default=0, verbose_name='商品数量')  # 商品数量
    commodityTime = models.CharField(max_length=32, default='', verbose_name='上货时间')  # 上货时间
    shops = models.ForeignKey('Shops', on_delete=models.CASCADE, verbose_name='所属店铺')  # 关联店铺（售卖店铺）

    class Meta:
        verbose_name = "商业街店铺商品"

    def toJSON(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))


class ShoppingList(models.Model):
    """购物清单"""
    shoppingName = models.CharField(max_length=32, verbose_name='商品名称')  # 购买内容
    shoppingCount = models.CharField(max_length=32, verbose_name='购买数量')  # 购买数量
    shoppingTime = models.CharField(max_length=32, verbose_name='购买时间')  # 购买时间
    shoppingMoney = models.CharField(max_length=32, default='', verbose_name='交易金额')  # 交易金额
    shoppingUser = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='购买用户')  # 关联用户（买家）
    shoppingShops = models.ForeignKey('Shops', on_delete=models.CASCADE, verbose_name='所属店铺')  # 关联店家（卖家）

    class Meta:
        verbose_name = "商业街店铺购物清单"

    def toJSON(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))


class ShuDong(models.Model):
    """ 树洞 """
    text = models.CharField(max_length=250, verbose_name='内容')  # 内容
    time = models.CharField(max_length=32, verbose_name='时间')  # 时间
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='发布用户')  # 关联用户（注册用户）

    class Meta:
        verbose_name = "树洞"


class LoseAndFound(models.Model):
    """ 失物招领 """
    name = models.CharField(max_length=32, verbose_name='失物名称')
    upname = models.CharField(max_length=32, verbose_name='发布用户')
    tel = models.CharField(max_length=32, verbose_name='联系方式')
    text = models.CharField(max_length=255, verbose_name='失物备注')
    type = models.CharField(max_length=32, verbose_name='发布类型')
    time = models.CharField(max_length=32, verbose_name='发布时间')
    img = models.ImageField(upload_to='', default='user1.jpg', verbose_name='图片')
    img_name = models.CharField(max_length=32, default="", verbose_name='图片名称')
    count = models.CharField(max_length=32, verbose_name='认领人数')
    user = models.ManyToManyField('User', verbose_name='认领用户')

    class Meta:
        verbose_name = "失物招领"


class BrowseCount(models.Model):
    """ 网站浏览次数 """
    count = models.IntegerField(max_length=64,default=0, verbose_name="网站浏览次数")

    class Meta:
        verbose_name = "网站浏览次数"
