from django.conf.urls import url

from App import views

urlpatterns =[
    url(r"^home/",views.home,name="home"),
    url(r"^market/",views.market,name="market"),
    url(r"^market_select/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)",views.market_select,name="market_select"),
    url(r"^cart/",views.cart,name="cart"),
    url(r"^mine/",views.mine,name="mine"),

    url(r"^register/",views.register,name="register"),
    url(r"^login/",views.login,name="login"),
    url(r"^logout/",views.logout,name="logout"),
    url(r"^checkuser/",views.checkuser,name="checkuser"),

    url(r'^activate/', views.activate, name='activate'),

    url(r"^subtocart/", views.subtocart, name="subtocart"),
    url(r"^addtocart/",views.addtocart,name="addtocart"),

    url(r'^subshopping/', views.sub_shopping, name='sub_shopping'),
    url(r"^addshopping/",views.add_shopping,name="add_shopping"),

    url(r'^changecartstate/', views.change_cart_state, name='change_cart_state'),
    url(r'^allselect/', views.all_select, name='all_select'),

    url(r'^makeorder/', views.make_order, name='make_order'),
    url(r'^orderdetail/', views.order_detail, name='order_detail'),

    url(r'^orderlistnotpay/', views.order_list_not_pay, name='order_list_not_pay'),


    url(r"^payed/", views.alipay,name="payed"),


    url(r"^addresslist/", views.addresslist,name="addresslist"),
    url(r"^addaddress/", views.addaddress,name="addaddress"),


]