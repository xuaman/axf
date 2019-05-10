$(function () {
    //开始对加和减的操作,发起请求
    $(".add_goods").click(function () {
        var $add = $(this); //得到当前的这个
        var goodsid = $add.attr("goodid");//获得商品的id
        $.get('/axf/addtocart/', {'goodsid': goodsid}, function (data) {
            console.log(data['status']);
            if (data['status'] ===302){
                window.open('/axf/login/', target="_self");
            }else if(data['status'] == 200){
                console.log(data['c_goods_num']);
                $add.prev('span').html(data['c_goods_num']);
            }
        })


    });
$(".sub_goods").click(function () {
        var $add = $(this); //得到当前的这个
        var goodsid = $add.attr("goodid");//获得商品的id

        $.get('/axf/subtocart/', {'goodsid': goodsid}, function (data) {
            console.log(data['status']);
            if (data['status'] ===302){
                window.open('/axf/login/', target="_self");
            }else if(data['status'] == 200){
                console.log(data['c_goods_num']);
                $add.next('span').html(data['c_goods_num']);
            }
        })


    });




















//    这个里面是对两个框的出来和取消显示。
    $all_types_container = $("#all_types_container");//全部分类的
    $sort_rule_container = $("#sort_rule_container");//按照排序的
    $all_type = $("#all_types");
    $sort_rule = $("#order_by");
    $all_types_span = $("#all_types_span");//类型的那个按钮
    $sort_rule_span =$("#sort_rules_span");//排序的那个按钮
    $good_list = $("#good_list");


    $all_type.click(function () {
        $all_types_container.show();
        $sort_rule_container.hide();
        $all_types_span.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");//点击和这个这个变
        $sort_rule_span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");//点击和这个这个变

    });
    $sort_rule.click(function () {
        $all_types_container.hide();
        $sort_rule_container.show();
        $sort_rule_span.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");//点击和这个这个变
        $all_types_span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");//点击和这个这个变

    });
    $good_list.click(function () {
        $all_types_container.hide();
        $sort_rule_container.hide();
        $sort_rule_span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");//点击和这个这个变
        $all_types_span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");//点击和这个这个变

    })


});