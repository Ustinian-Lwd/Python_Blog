// 收藏喜欢传值
function collect_like_session_storage(collect_like_key) {
    // 存入一个值
    sessionStorage.setItem('collect_like_key', collect_like_key);

}



$(document).ready(function () {
    // 获取首页传过来的参数  判断是否是collect还是login
    is_collect_or_like = sessionStorage.getItem("collect_like_key");
    console.log(is_collect_or_like);


    if (is_collect_or_like=="collect"){
        // 删除样式
	    $(".lwd-trigger-menu-activate").removeClass("lwd-trigger-menu-activate");

        $("#collect-like-list-container>ul").css("display", "none");
		$("#collect-blog-list").css("display", "block");
		$(".trigger-menu>li:first-child").attr("class", "lwd-trigger-menu-activate");
    }
    else if (is_collect_or_like=='like') {
        // 删除样式
	    $(".lwd-trigger-menu-activate").removeClass("lwd-trigger-menu-activate");

        $("#collect-like-list-container>ul").css("display", "none");
		$("#like-blog-list").css("display", "block");
		$(".trigger-menu>li:last-child").attr("class", "lwd-trigger-menu-activate");
    }



});












function lwd_trigger_menu_activate(obj, num) {
	// 删除样式
	$(".lwd-trigger-menu-activate").removeClass("lwd-trigger-menu-activate");

	console.log(num);

	// 把盒子删掉
	if (num == 1) {
		// break;
		$("#collect-like-list-container>ul").css("display", "none");
		$("#collect-blog-list").css("display", "block");
	} else if (num == 2) {
		$("#collect-like-list-container>ul").css("display", "none");
		$("#like-blog-list").css("display", "block");

	}
	$(obj).attr("class", "lwd-trigger-menu-activate");


}


function lwd_collect_like(is_collect_like) {
	// 判断是否那个点击事件
	console.log(is_collect_like);

	// 删除样式
	$(".lwd-trigger-menu-activate").removeClass("lwd-trigger-menu-activate");

	if (is_collect_like == "collect") {
		$("#collect-like-list-container>ul").css("display", "none");
		$("#collect-blog-list").css("display", "block");
		$(".trigger-menu>li:first-child").attr("class", "lwd-trigger-menu-activate");
	} else if (is_collect_like == "like") {
		$("#collect-like-list-container>ul").css("display", "none");
		$("#like-blog-list").css("display", "block");
		$(".trigger-menu>li:last-child").attr("class", "lwd-trigger-menu-activate");
	}


}


// 用户收藏页的核对关注
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


// 用户收藏页面的关注
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


// 把首页的selected 设置为 none
$("#starlist li:first-child a").attr("id", "");


