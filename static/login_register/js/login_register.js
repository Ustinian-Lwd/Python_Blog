$(document).ready(function () {
    // 获取首页传过来的参数  判断是否是login还是register
    is_login_or_register = sessionStorage.getItem("login_register_key");
    console.log(is_login_or_register);
    if (is_login_or_register == "login") {
        // 先把标题改成如下
        $('title').html('Lwd’s Blog | 登录');

        document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_login";
        document.querySelector('.cont_form_login').style.display = "block";
        document.querySelector('.cont_form_sign_up').style.opacity = "0";

        setTimeout(function () {
            document.querySelector('.cont_form_login').style.opacity = "1";
        }, 400);

        setTimeout(function () {
            document.querySelector('.cont_form_sign_up').style.display = "none";
        }, 200);


    } else if (is_login_or_register == "register") {
        // 先把标题改成如下
        $('title').html('Lwd’s Blog | 注册');

        document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_sign_up";
        document.querySelector('.cont_form_sign_up').style.display = "block";
        document.querySelector('.cont_form_login').style.opacity = "0";

        setTimeout(function () {
            document.querySelector('.cont_form_sign_up').style.opacity = "1";
        }, 100);

        setTimeout(function () {
            document.querySelector('.cont_form_login').style.display = "none";
        }, 400);

    }

});

function cambiar_login() {
    document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_login";
    document.querySelector('.cont_form_login').style.display = "block";
    document.querySelector('.cont_form_sign_up').style.opacity = "0";
    // 返回首页按钮消失
    document.querySelector('.login-register-back-home').style.display = "none";

    setTimeout(function () {
        document.querySelector('.cont_form_login').style.opacity = "1";
    }, 400);

    setTimeout(function () {
        document.querySelector('.cont_form_sign_up').style.display = "none";
    }, 200);
    // 先把标题改成如下
    $('title').html('Lwd’s Blog | 登录');
}

function cambiar_sign_up(at) {
    document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_sign_up";
    document.querySelector('.cont_form_sign_up').style.display = "block";
    document.querySelector('.cont_form_login').style.opacity = "0";
    // 返回首页按钮消失
    document.querySelector('.login-register-back-home').style.display = "none"

    setTimeout(function () {
        document.querySelector('.cont_form_sign_up').style.opacity = "1";
    }, 100);

    setTimeout(function () {
        document.querySelector('.cont_form_login').style.display = "none";
    }, 400);
    // 先把标题改成如下
    $('title').html('Lwd’s Blog | 注册');
}

function ocultar_login_sign_up() {
    // 先把标题改成如下
    $('title').html('Lwd’s Blog | 登录&注册');

    document.querySelector('.cont_forms').className = "cont_forms";
    document.querySelector('.cont_form_sign_up').style.opacity = "0";
    document.querySelector('.cont_form_login').style.opacity = "0";

    setTimeout(function () {
        document.querySelector('.cont_form_sign_up').style.display = "none";
        document.querySelector('.cont_form_login').style.display = "none";
        document.querySelector('.login-register-back-home').style.display = "block";
    }, 500);

}

function login_register_back_home() {
    window.location.href = "/"
}


// #####################  注册相关js  #####################
// 判断手机后是否能够注册，符合正则
// 如果符合正则，再把这些个值传给后台

// 失去焦点
// 用户名输入完成，发起ajax请求，验证该用户名是否能用
// 手机号码校验
var reg = /^1[34578]\d{9}$/;
$('#phone_number_sign_up').blur(function () {
    // 匹配正则
    // console.log(11111);
    // console.log($(this).val());
    var flag = reg.test($(this).val());
    console.log(flag);
    // 如果匹配
    if (flag) {
        console.log("匹配");
        $("#lwd-h2-sign-up").html("Lwd's Blog | Sign up");
        $('#sign_up_en').removeAttr("disabled").css("cursor", "pointer");

        $.post('/checkaccount/', {'phone_number': $(this).val()}, function (response) {
            console.log(response);
            if (response['status'] === '-1') { // 用户存在
                $("#lwd-h2-sign-up").html("账户已存在");
                // 把button给禁止了
                $('#sign_up_en').attr('disabled', 'disabled').css('cursor', 'none');

            } else {
                $('#lwd-h2-sign-up').html("Lwd's Blog | Sign up");
                $('#sign_up_en').removeAttr("disabled").css("cursor", "pointer");
            }
        });

    }
    // 如果不匹配
    else {
        console.log("不匹配");
        if ($(this).val()) {
            $("#lwd-h2-sign-up").html("手机号格式不匹配");
            // 把button给禁止了
            $('#sign_up_en').attr('disabled', 'disabled').css('cursor', 'none');

        } else {
            $("#lwd-h2-sign-up").html("请输入手机号码");
            // 把button给禁止了
            $('#sign_up_en').attr('disabled', 'disabled').css('cursor', 'none');
        }

    }
});

// 同样地，验证用户名是否能用
$('#user_name_sign_up').blur(function () {
    if ($(this).val()) {
        $.get('/checkname/', {'user_name': $(this).val()}, function (response) {
            console.log(response);
            if (response['status'] === '-1') { // 用户名被占用
                $('#lwd-h2-sign-up').html(response['msg']);
            } else {
                $('#lwd-h2-sign-up').html("Lwd's Blog | Sign up");
            }
        });
    } else {
        $("#lwd-h2-sign-up").html("别闹了，注册信息不完整");
    }
});


// 验证密码
$('#user_pwd_sign_up').blur(function () {
    var password = $(this).val();
    if (password) {
        if (password.length < 6 || password.length > 12) {
            $("#lwd-h2-sign-up").html("密码在6-12位之间");
        } else {
            $("#lwd-h2-sign-up").html("Lwd's Blog | Sign up")
        }
    } else {
        $("#lwd-h2-sign-up").html("别闹了，请输入密码");
    }
});

// 两次密码是否是一样的
$('#user_pwd_again_sign_up').blur(function () {
    var mypassword = $(this).val();
    if (mypassword) {
        if (mypassword !== $('#user_pwd_sign_up').val()) {
            $("#lwd-h2-sign-up").html("两次密码不一致");
        } else {
            $("#lwd-h2-sign-up").html("Lwd's Blog | Sign up");
        }
    } else {
        $("#lwd-h2-sign-up").html("Lwd's Blog | Sign up");
    }
});


// 点击button的时候再次发起ajax请求
$("#sign_up_en").on("click", function () {
    // 获取输入框的值
    // 账号
    phone_number = $("#phone_number_sign_up").val();
    // 用户名
    user_name = $("#user_name_sign_up").val();
    // 密码
    user_pwd = $("#user_pwd_sign_up").val();
    // 再一次密码
    user_pwd_again = $("#user_pwd_again_sign_up").val();
    // 是否为空
    flag = phone_number || user_name || user_pwd || user_pwd_again;
    if (flag) {
        if (user_pwd !== user_pwd_again) {
            $('#lwd-h2-sign-up').html("都说了密码不一致，你还点");
        }
        // 如果符合各种要求
        else {
            $.post("/register_post/", {
                'phone_number': phone_number,
                'user_name': user_name,
                'user_pwd': user_pwd
            }, function (response) {
                console.log(response);
                if (response["status"] === "1") {
                    window.location.href = "/";
                }
            });
        }
    } else {
        $('#lwd-h2-sign-up').html("注册信息不完整");
    }
});



// #####################  登录相关js  #####################
$("#sign_in_en").on("click", function () {
    phone_number = $("#phone_number_sign_in").val();
    user_pwd = $("#user_pwd_sign_in").val();
    $.post("/login_post/", {
        "phone_number": phone_number,
        "user_pwd": user_pwd
    }, function (response) {
        console.log(response);
            // 登录成功
            if (response["status"] === "1") {
                window.location.href = "/";
            }
            // 用户名不存在
            else if(response["status"] === "0"){
                $('#lwd-h2-sign-in').html("账号不存在，请先注册");
            }
            // 密码错误
            else if(response["status"] === "-1"){
                $('#lwd-h2-sign-in').html("密码错误");
            }
    })
});








