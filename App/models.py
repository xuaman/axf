from django.db import models

# Create your models here.
from App.views_constant import ORDER_STATUS_NOT_PAY


class Main(models.Model):
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField(default=1)
    class Meta:
        abstract=True

class MainWheel(Main):
    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):
    class Meta:
        db_table = 'axf_nav'


class MainMustBuy(Main):
    """
       axf_mustbuy(img,name,trackid)
       """
    class Meta:
        db_table = 'axf_mustbuy'


class MainShop(Main):
    """
    axf_shop(img,name,trackid
    """
    class Meta:
        db_table = 'axf_shop'


class MainShow(Main):
    categoryid = models.IntegerField(default=1)
    brandname = models.CharField(max_length=128)
    img1 = models.CharField(max_length=255)
    childcid1 = models.IntegerField(default=1)
    productid1 = models.IntegerField(default=1)
    longname1 = models.CharField(max_length=255)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=0)
    img2 = models.CharField(max_length=255)
    childcid2 = models.IntegerField(default=1)
    productid2 = models.IntegerField(default=1)
    longname2 = models.CharField(max_length=255)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=0)
    img3 = models.CharField(max_length=255)
    childcid3 = models.IntegerField(default=1)
    productid3 = models.IntegerField(default=1)
    longname3 = models.CharField(max_length=255)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = 'axf_mainshow'

class FoodTypes(models.Model):
    typeid = models.IntegerField(default=0)
    typename = models.CharField(max_length=128)
    childtypenames = models.CharField(max_length=128)
    typesort = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    productid = models.IntegerField(default=0)
    productimg = models.CharField(max_length=255)
    productname = models.CharField(max_length=255)
    productlongname = models.CharField(max_length=255)
    isxf = models.BooleanField(default=False)
    pmdesc = models.BooleanField(default=False)
    specifics = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=0)
    categoryid = models.IntegerField(default=0)
    childcid = models.IntegerField(default=0)
    childcidname = models.CharField(max_length=128)
    dealerid = models.IntegerField(default=0)
    storenums = models.IntegerField(default=0)
    productnum = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_goods'

class Users(models.Model):
    u_name = models.CharField(max_length=128,unique=True)
    u_passwd = models.CharField(max_length=128)
    u_email = models.EmailField(max_length=128,unique=True)
    u_icon = models.ImageField(upload_to="icons/%Y/%m/%d")
    u_active = models.BooleanField(default=False)
    u_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'axf_users'
class Cart(models.Model):
    c_user = models.ForeignKey(Users)
    c_goods = models.ForeignKey(Goods)

    c_goods_num = models.IntegerField(default=1)
    c_is_select = models.BooleanField(default=True)
    class Meta:
        db_table = "axf_cart"


class Order(models.Model):
    o_user = models.ForeignKey(Users)
    o_price = models.FloatField(default=0)
    o_time = models.DateTimeField(auto_now=True)
    o_status = models.IntegerField(default=ORDER_STATUS_NOT_PAY)

    class Meta:
        db_table = 'axf_order'


class OrderGoods(models.Model):
    o_order = models.ForeignKey(Order)
    o_goods = models.ForeignKey(Goods)
    o_goods_num = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_ordergoods'

class Shopaddress(models.Model):
    s_user = models.ForeignKey(Users)
    s_name = models.CharField(max_length=32)
    s_phone = models.CharField(max_length=11)
    s_address = models.CharField(max_length=255)
    s_isdefault = models.BooleanField(default=False)


    class Meta:
        db_table = "axf_shopaddress"