// 我的主页是去发表文章还是  草稿箱
function publish_dfrat_session_storage(publish_draft_key) {
    sessionStorage.setItem('publish_draft_key', publish_draft_key);

}

// 收藏喜欢传值
function collect_like_session_storage(collect_like_key) {
    // 存入一个值
    sessionStorage.setItem('collect_like_key', collect_like_key);

}


// 点击 侧边栏 (用户设置) 事件

// 基本设置侧边栏
$(".setting-aside>ul li:first-child").on("click", function () {
    // 取消影响
    $(".setting-active").attr("class", "");
    // 把所有的div隐藏
    $("div[class='col-xs-16 col-xs-offset-8 main']").css("display", "none");

    //
    $(".setting-aside>ul li:first-child").attr("class", "setting-active");
    $("#basic-setting").css("display", "block");
});

// 个人设置侧边栏
$(".setting-aside>ul li:nth-child(2)").on("click", function () {
    // 取消影响
    $(".setting-active").attr("class", "");
    // 把所有的div隐藏
    $("div[class='col-xs-16 col-xs-offset-8 main']").css("display", "none");

    //
    $(".setting-aside>ul li:nth-child(2)").attr("class", "setting-active");
    $("#profile-setting").css("display", "block");
});


// 账号管理设置侧边栏
$(".setting-aside>ul li:nth-child(3)").on("click", function () {
    // 取消影响
    $(".setting-active").attr("class", "");
    // 把所有的div隐藏
    $("div[class='col-xs-16 col-xs-offset-8 main']").css("display", "none");

    //
    $(".setting-aside>ul li:nth-child(3)").attr("class", "setting-active");
    $("#account-setting").css("display", "block");
});


// 黑名单设置侧边栏
$(".setting-aside>ul li:nth-child(4)").on("click", function () {
    // 取消影响
    $(".setting-active").attr("class", "");
    // 把所有的div隐藏
    $("div[class='col-xs-16 col-xs-offset-8 main']").css("display", "none");

    //
    $(".setting-aside>ul li:nth-child(4)").attr("class", "setting-active");
    $("#black-name").css("display", "block");
});


// 黑名单设置侧边栏
$(".setting-aside>ul li:last-child").on("click", function () {
    // 取消影响
    $(".setting-active").attr("class", "");
    // 把所有的div隐藏
    $("div[class='col-xs-16 col-xs-offset-8 main']").css("display", "none");

    //
    $(".setting-aside>ul li:last-child").attr("class", "setting-active");
    $("#reward-setting").css("display", "block");
});



// 把首页的selected 设置为 none
$("#starlist li:first-child a").attr("id", "");


// 基础设置--btn-save
function update_basic_setting(u_name, u_id, u_is_simple) {
    console.log(u_name, '-');
    $.get('/checkname/', {
        "user_name": u_name
    }, function (response) {
        if (response['status'] === '-1') { // 用户名被占用
            // $('#basic-setting-modal').modal('show');
            $("#modal-body-error").html(response['msg']).css("color", "red");
        } else {
            // $('#basic-setting-modal').modal('hide');
            // $("#modal-body-error").html("");
            $.post('/basic_setting/', {"user_name": u_name, "u_is_simple": u_is_simple}, function (response) {
                if (response['status'] === "1") {
                    $("#modal-body-error").html("保存成功，3秒后跳转...").css("color", "red");
                    setTimeout(function () {
                        console.log(1);
                        window.location.href = "/setting/u_id/" + u_id + '/';
                    }, 3000);


                }
            })


        }
    })


}


// 点击个人资料保存--save-btn
function update_personal_setting(sex, intro, website, u_id) {
    $.post('/personal_setting/', {"sex":sex, 'intro':intro, 'website':website}, function (response) {
        if (response['status']==="1"){
            console.log("******");
            $("#modal-body-error-1").html("保存成功，3秒后跳转...").css("color", "red");
            setTimeout(function () {
                console.log(1);
                window.location.href = "/setting/u_id/" + u_id + '/';
            }, 3000);
        }
    })
}

// 修改密码
function update_pwd(pwd, u_id){
    $.post('/update_pwd/', {'pwd': pwd}, function (response) {
        if (response['status']=='1') {
            $("#modal-body-error-2").html("保存成功，3秒后跳转...").css("color", "red");
            setTimeout(function () {
                console.log(1);
                window.location.href = "/setting/u_id/" + u_id + '/';
            }, 3000);
        }
    })

}


// 点击  删除账户
$(".delete-account-content .show-button").on("click", function () {
    $(".delete-account-content>.show-button").css("display", "none");
    $(".delete-account-content .content").css("display", "block");

});



// 点击 保留账号
$(".delete-account-content .content a[class='btn btn-hollow']").on("click", function () {

    console.log(111);
    $(".delete-account-content .content").css("display", "none");
    $(".delete-account-content .show-button").css("display", "block");
});

// 点击删除  那就是ajax发起请求，去删除用户信息了


