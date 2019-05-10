import uuid

from alipay import AliPay
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodTypes, Goods, Users, Cart, OrderGoods, \
    Order, Shopaddress
from App.tasks import send_email_activate
from App.views_constant import ALL_TYPE, ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN, \
    USER_OK, USER_EXISTS, USER_ERROR, PASSWD_ERROR, ORDER_STATUS_NOT_PAY, ORDER_STATUS_NOT_RECEIVE, \
    ORDER_STATUS_NOT_SEND
from App.views_helper import get_total_price
from axf.settings import MEDIA_KEY_PREFIX, ALIPAY_APPID, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY


def home(request):
    main_wheels = MainWheel.objects.all()

    main_navs = MainNav.objects.all()

    main_mustbuys = MainMustBuy.objects.all()

    main_shops = MainShop.objects.all()

    main_shop_first = main_shops[0:1]#第一个上边的
    main_shop_second = main_shops[1:3]#然后是两个的
    main_shop_third = main_shops[3:7] #这个是四个的
    main_shop_fourth = main_shops[7:11] #最后的牛奶什么的五种情况
   #这个传的应该还是query_set类型
    main_show_lists = MainShow.objects.all()


    print(main_shop_first)
    data = {
        "title": "首页",
        "main_wheels": main_wheels,
        'main_navs': main_navs,
        'main_mustbuys': main_mustbuys,

        'main_shop_first': main_shop_first,
        'main_shop_second': main_shop_second,
        'main_shop_third': main_shop_third,
        'main_shop_fourth': main_shop_fourth,

        'main_show_lists':main_show_lists,
    }
    return render(request,"axf/home.html",data)


def market(request):
    return redirect(reverse('axf:market_select', kwargs={
        "typeid": 104749,
        "childcid": 0,
        'order_rule': 0
    }))

def market_select(request, typeid, childcid,order_rule):
    foodtypes = FoodTypes.objects.all()


    goods_lists = Goods.objects.all().filter(categoryid=typeid)

    if childcid == ALL_TYPE:
        pass
    else:
        goods_lists = goods_lists.filter(childcid=childcid)

    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == ORDER_PRICE_UP:
        goods_lists = goods_lists.order_by("price")
    elif order_rule == ORDER_PRICE_DOWN:
        goods_lists = goods_lists.order_by("-price")
    elif order_rule == ORDER_SALE_UP:
        goods_lists = goods_lists.order_by("productnum")
    elif order_rule == ORDER_SALE_DOWN:
        goods_lists = goods_lists.order_by("-productnum")

    foodtype = foodtypes.get(typeid=typeid)


    foodtypechildnames = foodtype.childtypenames

    foodtypechildname_list = foodtypechildnames.split("#")

    foodtype_childname_list = []

    for foodtypechildname in foodtypechildname_list:
        foodtype_childname_list.append(foodtypechildname.split(":"))

    order_rule_list = [
        ['综合排序', ORDER_TOTAL],
        ['价格升序', ORDER_PRICE_UP],
        ['价格降序', ORDER_PRICE_DOWN],
        ['销量升序', ORDER_SALE_UP],
        ['销量降序', ORDER_SALE_DOWN],
    ]


    data ={
        "title": "闪购",
        "foodtypes": foodtypes,
        "goods_lists": goods_lists,
        "typeid": int(typeid),
        'foodtype_childname_list': foodtype_childname_list,
        'childcid': childcid,
        'order_rule_list': order_rule_list,
        'order_rule_view': order_rule
    }
    return render(request,"axf/market.html",context=data)


def cart(request):
    user = request.user
    carts = Cart.objects.filter(c_user_id=user)
    is_all_select = not carts.filter(c_is_select=False).exists()
    data = {
        "title": "购物车",
        "carts": carts,
        'is_all_select': is_all_select,
        'total_price': get_total_price(),
        'has_address': False,
    }

    # 这个是判断是否存在收货地址
    address = Shopaddress.objects.filter(s_user=user)

    if address:
        address = address.get(s_isdefault=True)
        print(address)
        data["has_address"] = True
        data["address"] = address




    return render(request,"axf/cart.html",context=data)


def mine(request):
    user_id = request.session.get('user_id')

    data = {
        'title': '我的',
        'is_login': False
    }

    if user_id:
        user = Users.objects.get(pk=user_id)
        data['is_login'] = True
        data['username'] = user.u_name
        data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url
        data['order_not_pay'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        data['order_not_receive'] = Order.objects.filter(o_user=user).filter(
        o_status__in=[ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND]).count()

    return render(request, 'axf/mine.html', context=data)


def register(request):
    if request.method == "GET":
        data={
            "title":"用户注册"
        }
        return render(request,"user/register.html",context=data)
    elif request.method == "POST":
        user = Users()
        user.u_name=request.POST.get("username")
        user.u_email=request.POST.get("email")
        passwd=request.POST.get("passwd")
        passwd = make_password(passwd)
        user.u_passwd=passwd
        user.u_icon=request.FILES.get("icon")
        user.save()
        u_token = uuid.uuid4().hex

        cache.set(u_token, user.id, timeout=60 * 60 * 24)

        send_email_activate.delay(user.u_name, user.u_email, u_token)

        return redirect(reverse("axf:login"))

def activate(request):
    u_token = request.GET.get('u_token')

    user_id = cache.get(u_token)

    if user_id:
        cache.delete(u_token)

        user = Users.objects.get(pk=user_id)

        user.u_active = True

        user.save()

        return redirect(reverse('axf:login'))

    return render(request, 'user/activate_fail.html')





def checkuser(request):

    data = {
        "status": USER_OK,
    }
    username = request.GET.get("username")
    email = request.GET.get("email")
    if username!= "0":
        users = Users.objects.filter(u_name=username)
        if users.exists():
            data["status"]=USER_EXISTS
        else:
            pass
    elif email != "0":
        email = Users.objects.filter(u_email=email)
        if email.exists():
            data["status"]=USER_EXISTS
        else:
            pass

    return JsonResponse(data=data)


def login(request):
    if request.method == "GET":

        data={
            "title":"用户登录",
        }
        message_error=False
        try:
            message_error = request.session["message_error"]
        except:
            pass
        if message_error:
            request.session.flush()
            data["message_error"]=message_error

        return render(request, "user/login.html", context=data)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("passwd")
        user = Users.objects.filter(u_name=username)
        if user:
            user = user.first()
            if check_password(password ,user.u_passwd) :
                if user.u_active:
                    request.session['user_id'] = user.id
                    # 在session里存入用户登录 然后跳转登录就ok了
                    return redirect(reverse("axf:mine"))
                else:
                    request.session["message_error"] = "账号没激活"

                    return redirect(reverse("axf:login"))
            else:
                request.session["message_error"] = "账号或密码错误"

                return redirect(reverse("axf:login"))
        else:
            request.session["message_error"] = "账号或密码错误"
            return redirect(reverse("axf:login"))


def logout(request):
    request.session.flush()
    return redirect(reverse("axf:mine"))


def addtocart(request):


    #尝试得到session 存在登录
        user_id = request.session.get('user_id')

        goodsid = request.GET.get('goodsid')
        carts = Cart.objects.filter(c_user_id=user_id).filter(c_goods_id=goodsid)
        print(carts)
        if carts.exists():
            cart_obj = carts.first()
            cart_obj.c_goods_num = cart_obj.c_goods_num + 1
        else:
            cart_obj = Cart()
            cart_obj.c_goods_id = goodsid
            cart_obj.c_user_id = user_id
            print(cart_obj.c_user_id)
            print(cart_obj.c_goods_id)
        cart_obj.save()
        data = {
            'status': 200,
            'msg': 'success',
            'c_goods_num': cart_obj.c_goods_num,
        }


        return JsonResponse(data=data)


def subtocart(request):
    data = {
        'status': 200,
    }
    user_id = request.session.get('user_id')

    goodsid = request.GET.get('goodsid')
    carts = Cart.objects.filter(c_user_id=user_id).filter(c_goods_id=goodsid)
    print(carts)
    if carts.exists():
        cart_obj = carts.first()
        if cart_obj.c_goods_num > 1:
            cart_obj.c_goods_num = cart_obj.c_goods_num - 1
            cart_obj.save()
            data["c_goods_num"]=cart_obj.c_goods_num
        elif cart_obj.c_goods_num == 1:
            cart_obj.delete()
            data["c_goods_num"] = 0
    else:
        pass



    return JsonResponse(data=data)


def change_cart_state(request):

    cart_id = request.GET.get('cartid')
    print(cart_id)

    cart_obj = Cart.objects.get(pk=cart_id)

    cart_obj.c_is_select = not cart_obj.c_is_select

    cart_obj.save()

    is_all_select = not Cart.objects.filter(c_user=request.user).filter(c_is_select=False).exists()

    data = {
        'status': 200,
        'msg': 'change ok',
        'c_is_select': cart_obj.c_is_select,
        'is_all_select': is_all_select,
        'total_price': get_total_price()
    }

    return JsonResponse(data=data)

def all_select(request):
    cart_list = request.GET.get('cart_list')

    cart_list = cart_list.split("#")

    carts = Cart.objects.filter(id__in=cart_list)

    for cart_obj in carts:
        cart_obj.c_is_select = not cart_obj.c_is_select
        cart_obj.save()

    data = {
        'status': 200,
        'msg': 'ok',
        'total_price': get_total_price()
    }

    return JsonResponse(data=data)


def make_order(request):
    carts = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)

    order = Order()

    order.o_user = request.user

    order.o_price = get_total_price()

    order.save()

    for cart_obj in carts:
        ordergoods = OrderGoods()
        ordergoods.o_order = order
        ordergoods.o_goods_num = cart_obj.c_goods_num
        ordergoods.o_goods = cart_obj.c_goods
        ordergoods.save()
        cart_obj.delete()

    data = {
        "status": 200,
        "msg": 'ok',
        'order_id': order.id
    }

    return JsonResponse(data)


def sub_shopping(request):
    cartid = request.GET.get("cartid")

    cart_obj = Cart.objects.get(pk=cartid)

    data = {
        'status': 200,
        'msg': 'ok',
    }

    if cart_obj.c_goods_num > 1:
        cart_obj.c_goods_num = cart_obj.c_goods_num - 1
        cart_obj.save()
        data['c_goods_num'] = cart_obj.c_goods_num
    else:
        cart_obj.delete()
        data['c_goods_num'] = 0

    data['total_price'] = get_total_price()

    return JsonResponse(data=data)
def add_shopping(request):
    cartid = request.GET.get("cartid")

    cart_obj = Cart.objects.get(pk=cartid)

    data = {
        'status': 200,
        'msg': 'ok',
    }

    cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    cart_obj.save()
    data['c_goods_num'] = Cart.objects.get(pk=cartid).c_goods_num

    data['total_price'] = get_total_price()

    return JsonResponse(data=data)



def order_detail(request):
    order_id = request.GET.get('orderid')

    # 构建支付的科幻  AlipayClient
    alipay_client = AliPay(
        appid=ALIPAY_APPID,
        app_notify_url=None,  # 默认回调url
        app_private_key_string=APP_PRIVATE_KEY,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False  # 默认False
    )
    # 使用Alipay进行支付请求的发起

    subject = "axf购物订单"
    money = Order.objects.get(pk=order_id).o_price
    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay_client.api_alipay_trade_wap_pay(
        out_trade_no=order_id+uuid.uuid4().hex,
        total_amount=money,
        subject=subject,
        return_url="http://xuaman.top/axf/payed/",
        notify_url="http://xuaman.top/axf/payed/"  # 可选, 不填则使用默认notify url
    )


    url = "https://openapi.alipaydev.com/gateway.do?" + order_string

    order = Order.objects.get(pk=order_id)

    data = {
        'title': "订单详情",
        'order': order,
        'url':url,
    }
    return render(request, 'order/order_detail.html', context=data)


def order_list_not_pay(request):

    print(request.user)

    orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NOT_PAY)

    data = {
        'title': '订单列表',
        'orders': orders,
    }
    return render(request, 'order/order_list_not_pay.html', context=data)





def alipay(request):
    order_list = request.GET.get("out_trade_no")
    order_id = order_list[:-32]

    order = Order.objects.get(pk=order_id)

    order.o_status = ORDER_STATUS_NOT_SEND

    order.save()

    return redirect(reverse("axf:mine"))

def addresslist(request):
    if request.method == "GET":
        addresslist = Shopaddress.objects.filter(s_user=request.user)
        data ={
            "addresslist":addresslist,

        }
        return render(request, "address/addresslist.html", context=data)





def addaddress(request):

    if request.method == "GET":
        return render(request, "address/addaddress.html")
    elif request.method == "POST":
        user = request.user
        add_name = request.POST.get("name")
        add_phone = request.POST.get("phone")
        add_address = request.POST.get("address")
        shop_user = Shopaddress.objects.filter(s_user=user)
        if shop_user:
            new_shopaddress = Shopaddress()
            new_shopaddress.s_user = user
            new_shopaddress.s_name = add_name
            new_shopaddress.s_phone = add_phone
            new_shopaddress.s_address = add_address
            new_shopaddress.save()
        else:
            new_shopaddress = Shopaddress()
            new_shopaddress.s_user = user
            new_shopaddress.s_name = add_name
            new_shopaddress.s_phone = add_phone
            new_shopaddress.s_address = add_address
            new_shopaddress.s_isdefault = True
            new_shopaddress.save()
    return redirect(reverse("axf:cart"))


