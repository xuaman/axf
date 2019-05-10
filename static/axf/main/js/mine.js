$(function () {
    // 找到对应的登录和注册 然后进行跳转页面
    $("#regis").click(function () {
        // 注册
        window.open('/axf/register/', target = "_self");
    });
    $("#not_login").click(function () {
        window.open('/axf/login/', target = "_self");
    });
     $("#not_pay").click(function () {
        window.open('/axf/orderlistnotpay/', target="_self");

    })

     $("#address").click(function () {
        window.open('/axf/addresslist/', target="_self");

    })


});