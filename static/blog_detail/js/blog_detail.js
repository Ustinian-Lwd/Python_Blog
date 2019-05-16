// {#  广告位的轮播图js  #}
var swiper = new Swiper('.swiper-container', {
    // 开启环路
    loop: true,
    // 自动播放
    autoplay: {
        // 时间间隔
        delay: 3500,
        // 用户操作swiper之后，是否禁止autoplay
        disableOnInteraction: false,
    },

    // 切换方式
    effect: 'cube',
    // cube效果
    cubeEffect: {
        slideShadows: true,
        shadow: true,
        shadowOffset: 15,
        shadowScale: 0.80
    },

    // 分页器
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
});


function check_follow(article_author) {
    // 文章刚加载进来，需要去检查文章的用户是否是被关注了
    // 用户名是唯一的
    // var article_author = $(".author-info>.name").text();
    console.log(article_author);
    $.post("/checkfollow/", {
        "article_author": article_author,
    }, function (response) {
        if (response['status'] === "1") {
            $("#follow-other-user").attr("class", "btn btn-default following");
            $(".fa.fa-plus").attr("class", "fa fa-check");
            $("#follow-other-user>span").html(response['msg']);
        } else if (response['status'] === "0") {

        }
    })
}


// 点击关注的操作
function add_follow(follow_text) {
    // 点击关注后，首先要判断用户是否是登录的
    $.post("/is_login/", function (response) {
        if (response['status'] === "1") {
            // var follow_text = $("#follow-other-user span").text();
            var article_author = $(".author-info .name").text();
            $.post("/follow_or_cancel/", {"follow_text": follow_text, "article_author": article_author},
                function (response) {
                    if (response["status"] === "1") {
                        $("#follow-other-user").attr("class", "btn btn-default following");
                        $(".fa.fa-plus").attr("class", "fa fa-check");
                        $("#follow-other-user>span").html(response['msg']);

                    } else if (response['status'] === "0") {
                        $("#follow-other-user").attr("class", "btn btn-success follow");
                        $(".fa.fa-check").attr("class", "fa fa-plus");
                        $("#follow-other-user>span").html(response['msg']);
                    }
                }
            )
        } else if (response['status'] === "0") {
            window.location.href = "/login/";
        }
    });
}


// 点击喜欢的处理
// current_elem 当前元素
// 文章的id
function add_like(current_elem, article_id) {
    // 喜欢 或者是 取消喜欢
    // console.log(article_id, "应该可以传过来吧");
    var like_or_cancel = $("#lwd-blog-detail-like .diggit a").text();
    console.log(like_or_cancel);
    $.post("/like_handler/", {
            "article_id": article_id,
            "like_or_cancel": like_or_cancel,
        },
        function (response) {
            if (response['status'] === "0") {
                window.location.href = "/login/";
            } else if (response['status'] === "1") {
                $("#lwd-blog-detail-like .diggit a").html(response['msg'])
                $("#lwd-blog-detail-like .diggit b").html(response['a_like_num'])
            } else if (response['status'] === '-1') {
                $("#lwd-blog-detail-like .diggit a").html(response['msg'])
                $("#lwd-blog-detail-like .diggit b").html(response['a_like_num'])
            }
        })
}


// 点击收藏的操作
function add_collect(current_elem, article_id) {
    // 收藏 或者是 取消收藏
    var collect_or_cancel = $("#lwd-blog-detail-collect .diggit a").text();
    $.post("/collect_handler/", {
            "article_id": article_id,
            "collect_or_cancel": collect_or_cancel,
        },
        function (response) {
            if (response['status'] === "0") {
                window.location.href = "/login/";
            } else if (response['status'] === "1") {
                $("#lwd-blog-detail-collect .diggit a").html(response['msg']);
                $("#lwd-blog-detail-collect .diggit b").html(response['a_collect_num'])
            } else if (response['status'] === '-1') {
                $("#lwd-blog-detail-collect .diggit a").html(response['msg']);
                $("#lwd-blog-detail-collect .diggit b").html(response['a_collect_num'])
            }
        })
}


// 核对当页面加载出来时候，是否收藏，喜欢
function check_like(article_id) {
    // 发送post请求
    $.post("/is_like/", {"article_id": article_id}, function (response) {
        if (response['status'] === "1") {
            $("#lwd-blog-detail-like .diggit a").html(response['msg']);
            $("#lwd-blog-detail-like .diggit b").html(response['a_like_num'])
        } else if (response['status'] === '-1') {
            $("#lwd-blog-detail-like .diggit a").html(response['msg']);
            $("#lwd-blog-detail-like .diggit b").html(response['a_like_num'])
        } else if (response['status'] === '0') {
            $("#lwd-blog-detail-like .diggit a").html(response['msg']);
            $("#lwd-blog-detail-like .diggit b").html(response['a_like_num'])
        }
    })
}

function check_collect(article_id) {
    // 发送post请求
    $.post("/is_collect/", {"article_id": article_id}, function (response) {
        if (response['status'] === "1") {
            $("#lwd-blog-detail-collect .diggit a").html(response['msg']);
            $("#lwd-blog-detail-collect .diggit b").html(response['a_collect_num'])
        } else if (response['status'] === "-1") {
            $("#lwd-blog-detail-collect .diggit a").html(response['msg']);
            $("#lwd-blog-detail-collect .diggit b").html(response['a_collect_num'])
        } else if (response['status'] === '0') {
            $("#lwd-blog-detail-collect .diggit a").html(response['msg']);
            $("#lwd-blog-detail-collect .diggit b").html(response['a_collect_num'])
        }

    })
}


$("#starlist li:first-child a").attr("id", "");

// 文本框获得焦点
var lwd_comment_textarea = $(".lwd-comment-textarea");
lwd_comment_textarea.on("focus", function () {
    lwd_comment_textarea.css('border', "1px solid #66afe9");
    lwd_comment_textarea.css('box-shadow', "1px 1px 1px #66afe9");
});

// 失去焦点
lwd_comment_textarea.on("blur", function () {
    lwd_comment_textarea.css('border', "1px solid #a9a9a9");
    lwd_comment_textarea.css('box-shadow', "none");
});

// 如果评论框是空的
// 禁止提交
$("#publish-comment").on("mousemove", function () {
    var text = $(".lwd-comment-textarea").val();
    if (text) {
        $("#publish-comment").attr("type", "submit")
    } else {
        $("#publish-comment").attr("type", "button")
    }
});




