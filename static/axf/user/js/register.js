$(function () {
    // 分别找到 username email passwd1 passwd2 icon 按照class 把passwd找到 找到外边的壳子
    //这个是进行整体带颜色的变化
    $register_username = $("#register_username");
    $register_email = $("#register_email");
    $register_passwd = $(".register_passwd");
    $register_passwd_span = $(".register_passwd_span");
    $register_icon = $("#register_icon");

    // 找到input的框
    $register_username_input = $("#register_username_input");
    $register_email_input = $("#register_email_input");
    $register_passwd1_input = $("#register_passwd1_input");
    $register_passwd2_input = $("#register_passwd2_input");
    $register_icon_input = $("#register_icon_input");
    //获取值 然后进行判断 发起请求 如果不对的话 或者对的话就进行改变内容,只有email和username进行检车
    $register_username_input.change(function () {
        var username = $register_username_input.val().trim();
        if (username.length) {
            $.getJSON("/axf/checkuser/", {"username": username, "email": 0}, function (data) {
                if (data["status"] === 200) {
                    $register_username.removeClass("has-error").addClass("has-success");
                    $register_username.find("span").removeClass("sr-only").removeClass("glyphicon-remove").addClass("glyphicon-ok");
                }
                else if (data["status"] === 901) {
                    $register_username.removeClass("has-success").addClass("has-error");
                    $register_username.find("span").removeClass("sr-only").removeClass("glyphicon-ok").addClass("glyphicon-remove");
                }
            })
        }
        else {
            $register_username.removeClass("has-success").addClass("has-error");
            $register_username.find("span").removeClass("sr-only").removeClass("glyphicon-ok").addClass("glyphicon-remove");

        }
    });

    $register_email_input.change(function () {
        var email = $register_email_input.val().trim();
        console.log(email)
        if (email.length) {
            $.getJSON("/axf/checkuser/", {"username": 0, "email": email}, function (data) {
                if (data["status"] === 200) {
                    $register_email.removeClass("has-error").addClass("has-success");
                    $register_email.find("span").removeClass("sr-only").removeClass("glyphicon-remove").addClass("glyphicon-ok");
                }
                else if (data["status"] === 901) {
                    $register_email.removeClass("has-success").addClass("has-error");
                    $register_email.find("span").removeClass("sr-only").removeClass("glyphicon-ok").addClass("glyphicon-remove");
                }
            })
        }
        else {
            $register_email.removeClass("has-success").addClass("has-error");
            $register_email.find("span").removeClass("sr-only").removeClass("glyphicon-ok").addClass("glyphicon-remove");

        }
    });
    //密码的验证
    $register_passwd1_input.change(function () {
        var passwd1 = $register_passwd1_input.val().trim();
        var passwd2 = $register_passwd2_input.val().trim();

        if (passwd1.length > 5 && passwd1 === passwd2) {
            $register_passwd.removeClass("has-error").addClass("has-success");
            $register_passwd_span.removeClass("sr-only").removeClass("glyphicon-remove").addClass("glyphicon-ok");
        }
        else {
            $register_passwd.removeClass("has-success").addClass("has-error");
            $register_passwd_span.removeClass("sr-only").removeClass("glyphicon-ok").addClass("glyphicon-remove");

        }
    });
    $register_passwd2_input.change(function () {
        var passwd1 = $register_passwd1_input.val().trim();
        var passwd2 = $register_passwd2_input.val().trim();

        if (passwd2.length > 5 && passwd1 === passwd2) {
            $register_passwd.removeClass("has-error").addClass("has-success");
            $register_passwd_span.removeClass("sr-only").removeClass("glyphicon-remove").addClass("glyphicon-ok");
        }
        else {
            $register_passwd.removeClass("has-success").addClass("has-error");
            $register_passwd_span.removeClass("sr-only").removeClass("glyphicon-ok").addClass("glyphicon-remove");

        }
    });

    $register_icon_input.change(function () {

        $register_icon.removeClass("has-error").removeClass("has-error").addClass("has-success");
        $register_icon.find("span").removeClass("sr-only").removeClass("glyphicon-remove").addClass("glyphicon-ok");

    });
});

function check() {
    $register_username = $("#register_username");
    $register_email = $("#register_email");
    $register_passwd = $(".register_passwd");
    $register_passwd_span = $(".register_passwd_span");
    $register_icon = $("#register_icon");
    if ($register_username.hasClass("has-success")) {
        if ($register_email.hasClass("has-success")) {
            if ($register_passwd.hasClass("has-success")) {
                if ($register_icon.hasClass("has-success")) {
                     var $password_input = $("#register_passwd1_input");

                    var password = $password_input.val().trim();

                    $password_input.val(md5(password));
                    return true
                } else {
                    $register_icon.removeClass("has-error").removeClass("has-success").addClass("has-error");
                    $register_icon.find("span").removeClass("sr-only").removeClass("glyphicon-ok").addClass("glyphicon-remove");
                    return false
                }

            } else {
                $register_passwd.removeClass("has-success").addClass("has-error");
                $register_passwd_span.removeClass("sr-only").removeClass("glyphicon-ok").addClass("glyphicon-remove");
                return false
            }
        }
        else {
            $register_email.removeClass("has-success").addClass("has-error");
            $register_email.find("span").removeClass("sr-only").removeClass("glyphicon-ok").addClass("glyphicon-remove");
            return false
        }
    }
    else {
        $register_username.removeClass("has-success").addClass("has-error");
        $register_username.find("span").removeClass("sr-only").removeClass("glyphicon-ok").addClass("glyphicon-remove");
        return false
    }
}

// sr-only 如果不显示的话就添加 class
// 显示就去掉
// <span class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span>
//