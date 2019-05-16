// 收藏喜欢传值
function collect_like_session_storage(collect_like_key) {
    // 存入一个值
    sessionStorage.setItem('collect_like_key', collect_like_key);

}



// 从写文章或者是编辑文章的页面跳转过来
// 如果保存为草稿箱，应该是切换到草稿箱
$(document).ready(function () {
    is_publish_or_dfrat = sessionStorage.getItem("publish_draft_key");

    if (is_publish_or_dfrat=="dfrat"){
        // 删除样式
        $(".lwd-trigger-menu-activate").removeClass("lwd-trigger-menu-activate");

        $("#list-container>ul").css("display", "none");
		$("#draft-list").css("display", "block");

		// 给草稿箱的那一栏加上activate
	    $("#user-home-dfrat").attr("class", "lwd-trigger-menu-activate")

    }

    else if (is_publish_or_dfrat=="publish") {
        // 删除样式
        $(".lwd-trigger-menu-activate").removeClass("lwd-trigger-menu-activate");

        // 把所有的ul li隐藏
        $("#list-container>ul").css("display", "none");

        // 把发表文章那一栏显示
		$("#blog-list").css("display", "block");

		// 给发表文章的那一栏加上activate
	    $("#user-home-publish").attr("class", "lwd-trigger-menu-activate");

    }


});




function lwd_trigger_menu_activate(obj, num) {

    // 如果点击了这个后，就把js的session删除
    sessionStorage.setItem('publish_draft_key', "");


	// 删除样式
	$(".lwd-trigger-menu-activate").removeClass("lwd-trigger-menu-activate");

	console.log(num);

	// 把盒子删掉
	if (num == 1) {
		// break;
		$("#list-container>ul").css("display", "none");
		$("#blog-list").css("display", "block");
	}else if (num == 2) {
		$("#list-container>ul").css("display", "none");
		$("#dynamic-list").css("display", "block");
	} else if (num == 3) {
		$("#list-container>ul").css("display", "none");
		$("#comment-list").css("display", "block");
	} else {
		$("#list-container>ul").css("display", "none");
		$("#draft-list").css("display", "block");
	}

	// console.log(activate);
	$(obj).attr("class", "lwd-trigger-menu-activate")

}

// 把首页的selected 设置为 none
$("#starlist li:first-child a").attr("id", "");


// 性别：图标颜色设置
// 	color: #00A7EB;
var i_class =  $(".lwd-title i").attr("class");
if(i_class=="fa fa-mars-stroke"){
	$(".lwd-title").css("color", "#00A7EB");
}
else if(i_class=="fa fa-mercury"){
	$(".lwd-title").css("color", "deeppink");
}
else{
	$(".lwd-title").css("color", "green");
}


// 用户主页的核对关注
function check_follow(article_author) {
    // 文章刚加载进来，需要去检查文章的用户是否是被关注了
    // 用户名是唯一的
    // var article_author = $(".author-info>.name").text();
    // console.log(article_author);
    $.post("/checkfollow/", {
        "article_author": article_author,
    }, function (response) {
        if (response['status'] === "1") {
		   $("#user-home-follow-btn").attr("class", "on user-follow-button");
			$(".fa.fa-plus").attr("class", "fa fa-check");
			$("#user-home-follow-btn>span").html(response['msg']);
        } else if (response['status'] === "0") {

        }
    })
}


// 用户主页的关注
function add_follow(article_author, follow_text) {
    // 点击关注后，首先要判断用户是否是登录的
    $.post("/is_login/", function (response) {
        if (response['status'] === "1") {
            // var follow_text = $("#follow-other-user span").text();
            // var article_author = $(".author-info .name").text();
            $.post("/follow_or_cancel/", {"follow_text": follow_text, "article_author": article_author},
                function (response) {
                    if (response["status"] === "1") {
                        $("#user-home-follow-btn").attr("class", "on user-follow-button");
                        $(".fa.fa-plus").attr("class", "fa fa-check");
                        $("#user-home-follow-btn>span").html(response['msg']);

                    } else if (response['status'] === "0") {
                        $("#user-home-follow-btn").attr("class", "off  user-follow-button");
                        $(".fa.fa-check").attr("class", "fa fa-plus");
                        $("#user-home-follow-btn>span").html(response['msg']);
                    }
                }
            )
        } else if (response['status'] === "0") {
            window.location.href = "/login/";
        }
    });
}









