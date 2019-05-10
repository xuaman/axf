$(function () {

    $("#alipay").click(function () {

        console.log("支付");

        var orderid = $(this).attr("orderid");
        console.log(orderid);
        window.open(orderid, target = "_self");

    })

})