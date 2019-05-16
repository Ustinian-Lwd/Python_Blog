function publish_dfrat_session_storage(publish_draft_key){
        sessionStorage.setItem('publish_draft_key', publish_draft_key);

}


function setShowLength() {
    var input_len = $("#write-article-title").val().length;
    // console.log(input_len);
    if (input_len <= 60) {
        $("#article-title-len").html((input_len > 10 ? input_len : "0" + input_len) + "/" + "60");
    }
}


// 返回首页点击事件
function back_home() {
    window.location.href = "/";
}


// 实时监控屏幕的大小
window.onresize = function () {
    var scroll_width = document.body.scrollWidth;
    console.log(scroll_width);
    var body = document.getElementsByTagName("body")[0];
    if (scroll_width < 639) {
        $('#myModal-alert').modal('show');
        body.style.pointerEvents = "none";
    } else {
        $('#myModal-alert').modal('hide');
        body.style.pointerEvents = "auto";
    }

};


// 匹配正则
function abstractFn(res) {
    if (!res) {
        return '';
    } else {
        var str = res.replace(/(\*\*|__)(.*?)(\*\*|__)/g, ' $2 ')          //全局匹配内粗体
            .replace(/\!\[[\s\S]*?\]\([\s\S]*?\)/g, ' ')  //全局匹配图片
            .replace(/\[[\s\S]*?\]\([\s\S]*?\)/g, ' ')  //全局匹配连接
            .replace(/<\/?.+?\/?>/g, '')   //全局匹配内html标签
            .replace(/(\*)(.*?)(\*)/g, '$1 ')  //全局匹配内联代码块
            .replace(/`{1,2}[^`](.*?)`{1,2}/g, '$1 ') //全局匹配内联代码块
            .replace(/```([\s\S]*?)```[\s]*/g, '$1 ')   //全局匹配代码块
            .replace(/\~\~(.*?)\~\~/g, '$1 ')   //全局匹配删除线
            .replace(/[\s]*([-\*\+]+)(.*)/g, '$1 $2 ')   //全局匹配无序列表
            .replace(/[\s]*[0-9]+\.(.*)/g, '$1')   //全局匹配有序列表
            .replace(/(#+)(.*)/g, '')                                    //全局匹配标题
            .replace(/(>+)(.*)/g, '$2')                                    //全局匹配摘要
            .replace(/\r\n/g, "")                                        //全局匹配换行
            .replace(/\n/g, "   ")                                          //全局匹配换行
            .replace(/\s/g, "  ");                                          //全局匹配空字符;
        return str
    }
}


window.onload = function () {

    // 点击发表文章的事件
    $("#write-article-publish").on("click", function () {
        // 文章标题
        var article_title = $("#write-article-title").val();
        // 文章内容-md
        var article_content_md = testEditor.getMarkdown();
        flag = article_title && article_content_md;
        if (flag) {
            $("#lwd-ModalLabel").html("发表文章").css("color", "black");
        } else {
            $("#lwd-ModalLabel").html("文章标题或内容不为空").css("color", "red");
        }
    });

};


function write_article(is_publish) {
    // 文章标题
    var article_title = $("#write-article-title").val();
    // 文章内容-md
    var article_content_md = testEditor.getMarkdown();
    console.log(abstractFn(article_content_md));
    // 文章分类
    var article_class = $("#article-class").val();
    console.log(article_class);
    // 文章标签
    var article_tag = document.getElementById("jquery-tagbox-text").value;
    console.log(article_tag, "----");

    // 获取文章的第一个图片
    var img_pattern = /\!\[[\s\S]*?\]\([\s\S]*?\)/g;
    console.log(img_pattern.test(article_content_md));
    if (article_content_md.match(img_pattern)) {
        article_pre_img = article_content_md.match(img_pattern)[0];
        console.log(article_pre_img, "预览图片");
    } else {
        article_pre_img = "blog_default_img.png";
        console.log(article_pre_img, "预览图片");
    }
    if (article_title=="" || article_content_md=="") {
        $("#lwd-ModalLabel").html("文章标题或内容不为空").css("color", "red");
    }
    else{
         $("#lwd-ModalLabel").html("发表文章").css("color", "black");
        if (article_class == "-1") {
    $("#lwd-ModalLabel").html("请选择文章类别或标签").css("color", "red");
}
        else {
    $("#lwd-ModalLabel").html("发布文章").css("color", "black");
    $.post("/write_post/", {
        // 文章标题
        "article_title": article_title,
        // 文章预览图片
        "article_pre_img": article_pre_img,
        // 文章内容-html
        "article_content_md": article_content_md,
        // 文章内容-text
        "article_content_text": abstractFn(article_content_md),
        // 文章分类
        "article_class": article_class,
        // 文章标签
        "article_tag": article_tag,
        // 是否发表还是草稿箱
        "is_publish": is_publish,

    }, function (response) {
        // console.log(response);
        if (response['status'] === "1") {
            // console.log(response["msg"]);
            $("#lwd-ModalLabel").html(response['msg']).css("color", "red");

            setTimeout(function () {
                console.log(1);
                window.location.href = "/a_id/" + response['a_id'];
            }, 3000);

        }
        else if (response['status'] === "2"){
            $("#lwd-ModalLabel").html(response['msg']).css("color", "red");

            setTimeout(function () {
                console.log(1);
                window.location.href = "/u_id/" + response['u_id'] + "/";
            }, 3000);
        }

        else if (response["status"] === "0") {
            $("#lwd-ModalLabel").html("发送文章失败，请重新发送").css("color", "red");

        }
    })
}
    }
}







