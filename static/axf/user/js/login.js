function parse_data() {


    var $password_input = $("#password_input");

    var password = $password_input.val().trim();

    $password_input.val(md5(password));

    return true
}
$(function () {
      $("#toregister").click(function () {
        // 添加地址
        window.open('/axf/register/', target = "_self");
    });
})