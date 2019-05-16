$(document).ready(function () {

    //banner
    $('#banner').easyFader();

    //nav 三条杠的切换
    $("#mnavh").click(function () {
        $("#starlist").toggle();
        $("#mnavh").toggleClass("open");
    });

    // header
    var new_scroll_position = 0;
    var last_scroll_position;
    var header = document.getElementById("header");

    window.addEventListener('scroll', function (e) {
        last_scroll_position = window.scrollY;

        if (new_scroll_position < last_scroll_position && last_scroll_position > 80) {
            header.classList.remove("slideDown");
            header.classList.add("slideUp");

        } else if (new_scroll_position > last_scroll_position) {
            header.classList.remove("slideUp");
            header.classList.add("slideDown");
        }

        new_scroll_position = last_scroll_position;
    });


    // 侧边栏分类
    $('.fenlei li').click(function () {
        $(this).addClass('flselect').siblings().removeClass('flselect');
        $('.newstw>ul:eq(' + $(this).index() + ')').show().siblings().hide();
    });

    //aside
    // 页面滚动侧边栏的处理
    var Sticky = new hcSticky('aside', {
        stickTo: 'main',
        innerTop: 200,
        followScroll: false,
        queries: {
            480: {
                disable: true,
                stickTo: 'body'
            }
        }
    });

    // 侧边栏滚动处理
    var speed = 2000; //自定义滚动速度
    //回到顶部
    $(".lwd-cd-top").click(function () {
        $("html,body").animate({
            "scrollTop": 0
        }, speed);
    });

    // 回到底部 
    $(".lwd-cd-bottom").click(function () {
        var windowHeight = $("body").css("height"); //整个页面的高度
        $("html, body").animate({
            "scrollTop": windowHeight
        }, speed);
        // window.scrollTo(0, document.documentElement.clientHeight);

    });

});


// 我的主页是去发表文章还是  草稿箱
function publish_dfrat_session_storage(publish_draft_key) {
    sessionStorage.setItem('publish_draft_key', publish_draft_key);

}



