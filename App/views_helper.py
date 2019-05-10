from django.core.mail import send_mail
from django.template import loader

from App.models import Cart
from axf.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT








def get_total_price():

    carts = Cart.objects.filter(c_is_select=True)

    total = 0

    for cart in carts:
        total += cart.c_goods_num * cart.c_goods.price

    return "{:.2f}".format(total)
