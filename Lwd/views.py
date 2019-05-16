import re
import hashlib
import time
import urllib.request
import uuid
from django.contrib.auth import logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
import os
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from Lwd.models import UserInfo, ArticleInfo, LikeInfo, CollectInfo, FollowInfo, IndexBannerImg, AdBannerImg, \
    ArticleCategory, ArticleTag
from Python_Blog import settings
from PIL import Image
from comments.models import Comment


# 测试
def hello(request):
    return HttpResponse("Hello, My Blog.")


# 分页处理
def page_handler(request, obj, per_page_num):
    # 分页处理
    # 每页10条
    paginator = Paginator(obj, per_page_num)
    # 获取页面参数
    page_num = request.GET.get('page', 1)

    try:
        article_page = paginator.page(page_num)
    except PageNotAnInteger:
        article_page = paginator.page(1)
    except EmptyPage:
        article_page = paginator.page(paginator.num_pages)

    return article_page


# 首页
def index(request):
    responseData = {}
    # 获取token
    token = request.session.get('token')
    responseData['token'] = token
    # 是否存在这样的用户
    user_token = UserInfo.objects.filter(u_token=token, u_is_delete=False)

    # 判断这样的用户
    if len(user_token) > 0:
        user_token = user_token[0]
        responseData['user_token'] = user_token

    # 首页-文章列表 渲染
    article_index_list = ArticleInfo.objects.filter(a_is_publish=True).order_by("-a_update_time")
    responseData['article_page'] = page_handler(request, article_index_list, 10)

    return render(request, 'index.html', context=responseData)


# 注册get请求
def register_get(request):
    return render(request, 'login_register.html')


# 注册post请求
def register_post(request):
    # 接受传过来的参数
    req_u_account = request.POST.get("phone_number")
    req_u_name = request.POST.get("user_name")
    req_u_pwd = request.POST.get("user_pwd")

    """
    # 用户表中账号和用户昵称是unique的
    # 在用户表中设置了一个is_delete字段
    # 这个字段是当我们删除用户的时候，可以采取逻辑删除
    # 当用户注册的时候
    # 要分三种情况：
    # 1 被删除的用户或者其他用户注册，用的账号是原来的；
    # 2 被删除的用户或者其他用户注册，用的昵称是原来的；
    # 3 被删除的用户或者其他用户注册，既用了原来的账号，又用了原来的昵称；
    """
    user_ = UserInfo.objects.filter(u_account=req_u_account) or UserInfo.objects.filter(
        u_name=req_u_name) or UserInfo.objects.filter(u_account=req_u_account, u_name=req_u_name)

    # 存在
    if user_:
        user_[0].u_account = req_u_account
        user_[0].u_name = req_u_name
        user_[0].u_password = generate_password(req_u_pwd)
        user_[0].u_is_delete = False
        # token
        user_[0].u_token = str(uuid.uuid5(uuid.uuid4(), 'register'))
        user_[0].save()
        # 状态保持
        request.session['token'] = user_[0].u_token
    # 不存在
    else:
        user = UserInfo()
        user.u_id = str(uuid.uuid5(uuid.uuid4(), 'register')).replace("-", "")
        user.u_account = req_u_account
        user.u_name = req_u_name
        user.u_password = generate_password(req_u_pwd)
        # token
        user.u_token = str(uuid.uuid5(uuid.uuid4(), 'register'))
        # 保存到数据库
        user.save()
        # 状态保持
        request.session['token'] = user.u_token

    return JsonResponse({'msg': '账号注册成功!', 'status': '1'})


# 加密密码
def generate_password(password):
    sha = hashlib.sha512()
    sha.update(password.encode('utf-8'))
    return sha.hexdigest()


# 检查账号是否存在
def checkaccount(request):
    phone_number = request.POST.get('phone_number')
    # 先判断这个用户是不是逻辑删除
    user = UserInfo.objects.filter(u_account=phone_number)
    if user:
        user_is_delete = user[0].u_is_delete
        print(user_is_delete, '111111')
        if user_is_delete:
            return JsonResponse({'msg': '账号可用!', 'status': '1'})
        else:
            return JsonResponse({'msg': '账号已注册!', 'status': '-1'})
    else:
        return JsonResponse({'msg': '账号可用!', 'status': '1'})


# 检查用户名是否被占用
def checkname(request):
    user_name = request.GET.get('user_name')
    user = UserInfo.objects.filter(u_name=user_name)
    if user:
        flag = user.u_is_delete
        if flag:
            return JsonResponse({'msg': '昵称可用!', 'status': '-1'})
        else:
            return JsonResponse({'msg': '昵称已占用!', 'status': '-1'})
    else:
        return JsonResponse({'msg': '昵称可用!', 'status': '1'})


# 登录-get
def login_get(request):
    return render(request, 'login_register.html')


# 登录-post
def login_post(request):
    account = request.POST.get('phone_number')
    password = request.POST.get('user_pwd')

    try:
        user = UserInfo.objects.get(u_account=account, u_is_delete=False)
        if user.u_password != generate_password(password):  # 密码错误
            return JsonResponse({"msg": "密码错误", "status": "-1"})
        else:  # 登录成功
            # 更新token
            user.u_token = str(uuid.uuid5(uuid.uuid4(), 'login'))
            user.save()
            # 状态保持
            request.session['token'] = user.u_token
            return JsonResponse({"msg": "登录", "status": "1"})
    except:
        return JsonResponse({"msg": "用户名错误", "status": "0"})


# 退出登录
def quit(request):
    # request.session.flush()
    logout(request)
    return redirect('lwd:index')


# 写文章-get请求
def write_article_get(request):
    # 文章的分类
    article_category_list = ArticleCategory.objects.all()

    return render(request, "write_article.html", locals())


# 写文章-post请求
def write_article_post(request):
    try:
        article = ArticleInfo()
        # 文章id
        a_id = str(uuid.uuid5(uuid.uuid4(), 'write')).replace("-", "")
        article.a_id = a_id
        # 标题
        article.a_title = request.POST.get("article_title")
        # 作者
        # 只有在登录的情况下才能书写文章
        token = request.session.get('token')
        article.a_author = UserInfo.objects.get(u_token=token).u_name

        # 预览图片
        pre_img_str = request.POST.get("article_pre_img")
        print(pre_img_str, "传过来的图片")
        # 正则匹配
        if pre_img_str == "blog_default_img.png":
            article.a_pre_img = pre_img_str
        else:
            try:
                pre_img_obj = re.compile(r'[(]/media/(.*?)[)]')
                pre_img = pre_img_obj.findall(pre_img_str)[0].split(" ")[0]
                pre_img_path = os.path.join(settings.MEDIA_ROOT, pre_img)
                print(pre_img_path, "看一下这个pre_img_path是个什么鬼")
                img = Image.open(pre_img_path)
                width, height = img.size
                if width <= height:
                    article.a_pre_img = "blog_default_img.png"
                else:
                    article.a_pre_img = pre_img
            except:
                pre_img_obj = re.compile(r'[(](.*?)[)]')

                # 请求url
                pre_img_url = pre_img_obj.findall(pre_img_str)[0]
                # print(pre_img_url, "爬虫url")

                # 请求头
                headers = {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
                }
                # 创建请求
                request_obj = urllib.request.Request(pre_img_url, headers=headers)
                response_obj = urllib.request.urlopen(request_obj)

                # 保存路径
                path = settings.MEDIA_URL + 'blog_img/' + str(uuid.uuid5(uuid.uuid4(),'upload_img_path')).replace("-", "") + '/'

                # 绝对路径-目录
                abs_path = (settings.BASE_DIR + path).replace("\\", '/')
                if not os.path.exists(abs_path):
                    os.makedirs(abs_path)

                # 拼装本地保存图片的完整文件名
                filename = str(uuid.uuid5(uuid.uuid4(), 'upload_img')) + '_' + '.jpg'

                # 绝对路径-文件
                abs_file_path = abs_path + filename

                # 写入文件
                with open(abs_file_path, 'wb+') as fp:
                    fp.write(response_obj.read())

                img2 = Image.open(abs_file_path)
                width, height = img2.size
                if width >= height:
                    article.a_pre_img = path.split("/media/")[-1] + filename
                else:
                    article.a_pre_img = "blog_default_img.png"

        # 内容-html
        article.a_content_md = request.POST.get("article_content_md")
        # 文章字数
        article.a_word_num = str(len(request.POST.get("article_content_md")))

        # 内容-纯text
        # 其实就是内容的概述
        article.a_content_text = request.POST.get("article_content_text")[0:200] + "..."

        # 分类
        article_class_id = eval(request.POST.get("article_class"))
        article.a_category = ArticleCategory.objects.get(id=article_class_id)

        """
        # 创建时间
        # 修改时间
        # 喜欢数量
        # 评论数量
        # 以上内容在发表文章时，默认
        """

        # 是否正式发表
        is_publish = request.POST.get("is_publish")
        if int(is_publish):
            article.a_is_publish = True
            # 声明关系
            article.a_user = UserInfo.objects.get(u_token=token)
            # print(article.a_user)

            # 写入数据库
            article.save()

            # 标签
            tag_list = request.POST.get("article_tag").split(',')
            print(tag_list)

            tag_exist_all = ArticleTag.objects.all()
            temp_list = []
            for tag_exist in tag_exist_all:
                temp_list.append(tag_exist.tag_name)

            # 首先写入标签中
            for tag in tag_list:
                if tag in temp_list:
                    pass
                else:
                    if tag == "":
                        pass
                    else:
                        tag_save = ArticleTag()
                        tag_save.tag_name = tag
                        tag_save.save()

            # 文章-标签的声明关系
            tag_all = ArticleTag.objects.all()
            # 多对多
            for tag in tag_list:
                if tag == "":
                    pass
                else:
                    for tag_ in tag_all:
                        if tag == tag_.tag_name:
                            article.a_tag.add(tag_)
            article.save()

            return JsonResponse({"msg": "发表文章成功，3秒后跳转文章详情页面", "status": "1", "a_id": article.a_id})

        else:
            article.a_is_publish = False
            # 声明关系
            article.a_user = UserInfo.objects.get(u_token=token)
            # print(article.a_user)

            # 写入数据库
            article.save()

            return JsonResponse({"msg": "已保存到草稿箱,3秒后跳转到用户主页", "status": "2", "u_id": article.a_user.u_id})

    except:
        return JsonResponse({"msg": "发表文章失败", "status": "0"})


# 用户等级图片判断
def lwd_user_level(user_level):
    if 1 <= user_level <= 20:
        user_level_img = "user_level/putong.png"
        user_level_alt = "普通用户"
        return (user_level_img, user_level_alt)

    elif 21 <= user_level <= 30:
        user_level_img = "user_level/qingtong.png"
        user_level_alt = "青铜用户"
        return (user_level_img, user_level_alt)

    elif 31 <= user_level <= 40:
        user_level_img = "user_level/baiyin.png"
        user_level_alt = "白银用户"
        return (user_level_img, user_level_alt)

    elif 41 <= user_level < 50:
        user_level_img = "user_level/huangjin.png"
        user_level_alt = "黄金用户"
        return (user_level_img, user_level_alt)

    elif 51 <= user_level <= 60:
        user_level_img = "user_level/bojin.png"
        user_level_alt = "铂金用户"
        return (user_level_img, user_level_alt)

    elif 61 <= user_level <= 70:
        user_level_img = "user_level/zuanshi.png"
        user_level_alt = "钻石用户"
        return (user_level_img, user_level_alt)
    else:
        user_level_img = "user_level/zhizun.png"
        user_level_alt = "至尊用户"
        return (user_level_img, user_level_alt)


# 点击标题进入文章详情
# 文章详情-
def blog_detail(request, a_id):
    # 数据交互
    responseData = {}

    # 广告位轮播图
    ad_banners = AdBannerImg.objects.all()[:5]
    responseData['ad_banners'] = ad_banners

    # 查找到文章
    article = ArticleInfo.objects.get(a_id=a_id)
    responseData['article'] = article
    article.increase_views()

    # 上一篇文章，下一篇文章

    # 评论
    comment_list = article.comment_set.all()
    responseData['comment_list'] = comment_list

    # 文章作者
    author = article.a_user
    responseData['author'] = author

    # 各自等级用户的图标
    responseData['user_level_img'], responseData['user_level_alt'] = lwd_user_level(int(author.u_level))

    responseData['is_have_follow_btn'] = True
    responseData['is_have_edit_btn'] = False

    # 接下来是判断用户是否登录
    token = request.session.get("token")
    # 说明登录
    if token:
        user_token = UserInfo.objects.get(u_token=token)
        responseData['token'] = token
        # responseData['user_login_img'] = user_login.u_img
        responseData['user_token'] = user_token

        # 判断是否需要 关注按钮、编辑文章按钮
        if user_token.u_id == author.u_id:
            responseData['is_have_follow_btn'] = False
            responseData['is_have_edit_btn'] = True

        return render(request, "blog_detail.html", context=responseData)
    else:
        return render(request, "blog_detail.html", context=responseData)


# 判断用户是否登录
def is_login(request):
    # token
    token = request.session.get("token")
    if token:
        return JsonResponse({"msg": "登录状态", "status": "1"})
    else:
        return JsonResponse({"msg": "未登录状态", "status": "0"})


# 核对用户是否被关注
def check_is_follow(request):
    token = request.session.get("token")
    if token:
        # 登录的用户
        user_login = UserInfo.objects.get(u_token=token)

        # 文章作者
        article_author = request.POST.get("article_author")

        data = {}
        for author in user_login.u_follow.split(";"):
            if author == article_author:
                data = {
                    "msg": "已关注",
                    "status": "1"
                }
                break
            else:
                data = {
                    "msg": "关注",
                    "status": "0"
                }
        # print(data, "看一下data")
        return JsonResponse(data)


# 文章详情界面的关注
# 用户取消关注或者用户关注
def follow_or_cancel(request):
    # 登录的用户
    token = request.session.get("token")
    user_login = UserInfo.objects.get(u_token=token)

    # 关注的文本
    follow_text = request.POST.get("follow_text")
    follow_text = re.findall(r'[\u4E00-\u9FA5]+', follow_text)[0]
    article_author = request.POST.get("article_author")
    user_author = UserInfo.objects.get(u_name=article_author)
    if follow_text == "关注":
        # 用户表的关注
        user_login.u_follow += article_author + ";"
        user_login.save()

        # 关注表的关注
        follow = FollowInfo()
        follow.f_id = str(uuid.uuid5(uuid.uuid4(), 'follow')).replace("-", "")
        follow.f_user1 = user_login
        follow.f_user2_name = user_author.u_name
        follow.save()

        return JsonResponse({
            "msg": "已关注",
            "status": "1"
        })

    elif follow_text == "已关注":
        # 关注表的关注
        follow_ = FollowInfo.objects.filter(f_user1=user_login, f_user2_name=user_author.u_name)

        if follow_:
            follow_.delete()
            # follow_.save()

        # 用户表中的关注
        data = {}
        for author in user_login.u_follow.split(";"):
            if author == article_author:
                # 删除
                author = author + ";"
                # print(user_login.u_follow, "begin")
                user_login.u_follow = user_login.u_follow.replace(author, "")
                user_login.save()
                data = {
                    "msg": "关注",
                    "status": "0"
                }

                break
        return JsonResponse(data)


# 喜欢
# 涉及到的表是LikeInfo, ArticleInfo
def like_handler(request):
    token = request.session.get("token")
    # 首先得判断用户是否登录
    if token:
        # print("-----------")
        like_or_cancel = request.POST.get("like_or_cancel")
        article_id = request.POST.get("article_id")
        like = LikeInfo()
        if like_or_cancel == "喜欢":
            like.l_id = str(uuid.uuid5(uuid.uuid4(), 'like')).replace("-", "")
            # 用户
            user_login = UserInfo.objects.get(u_token=token)
            like.l_user = user_login
            # 文章
            article = ArticleInfo.objects.get(a_id=article_id)
            like.l_article = article
            # like表保存
            like.save()
            # 文章表喜欢数量+1
            article.a_like_num += 1
            article.save()
            return JsonResponse({"msg": "取消喜欢", "status": "1", "a_like_num": article.a_like_num})
        elif like_or_cancel == "取消喜欢":
            u = UserInfo.objects.get(u_token=token)
            a = ArticleInfo.objects.get(a_id=article_id)
            # 删除记录
            LikeInfo.objects.filter(l_article=a).filter(l_user=u).delete()
            # like.save()
            # 文章喜欢-1
            a.a_like_num = a.a_like_num - 1
            a.save()
            return JsonResponse({"msg": "喜欢", "status": "-1", "a_like_num": a.a_like_num})
    else:
        return JsonResponse({"msg": "用户未登录", "status": "0"})


# 每次blog详情加载进来，
# 首先得去查询用户是否是处在喜欢或者有没有收藏
# 核对喜欢
def is_like(request):
    token = request.session.get("token")
    user_info = UserInfo.objects.get(u_token=token)
    article_id = request.POST.get("article_id")
    article = ArticleInfo.objects.get(a_id=article_id)
    # print(article.a_id, "1111111111111111")
    if token:
        like = LikeInfo.objects.filter(l_user=user_info).filter(l_article=article)
        # 核对喜欢
        if like:
            return JsonResponse({"msg": "取消喜欢", "status": "1", "a_like_num": article.a_like_num})
        else:
            return JsonResponse({"msg": "喜欢", "status": "-1", "a_like_num": article.a_like_num})
    else:
        return JsonResponse({"msg": "喜欢", "status": "0", "a_like_num": article.a_like_num})


# 收藏
def collect_handler(request):
    token = request.session.get("token")
    # 首先得判断用户是否登录
    if token:
        collect_or_cancel = request.POST.get("collect_or_cancel")
        article_id = request.POST.get("article_id")
        # 实例化收藏模型
        collect = CollectInfo()
        if collect_or_cancel == "收藏":
            collect.col_id = str(uuid.uuid5(uuid.uuid4(), 'collect')).replace("-", "")
            # 用户
            user_login = UserInfo.objects.get(u_token=token)
            collect.col_user = user_login
            # 文章
            article = ArticleInfo.objects.get(a_id=article_id)
            collect.col_article = article
            # collect表保存
            collect.save()
            # 文章表喜欢数量+1
            article.a_collect_num += 1
            article.save()
            return JsonResponse({"msg": "取消收藏", "status": "1", "a_collect_num": article.a_collect_num})
        elif collect_or_cancel == "取消收藏":
            u = UserInfo.objects.get(u_token=token)
            a = ArticleInfo.objects.get(a_id=article_id)
            # 删除记录
            CollectInfo.objects.filter(col_article=a).filter(col_user=u).delete()
            # collect.save()
            # 文章喜欢-1
            a.a_collect_num -= 1
            a.save()
            return JsonResponse({"msg": "收藏", "status": "-1", "a_collect_num": a.a_collect_num})
    else:
        return JsonResponse({"msg": "用户未登录", "status": "0"})


# 核对收藏
def is_collect(request):
    token = request.session.get("token")
    user_info = UserInfo.objects.get(u_token=token)
    article_id = request.POST.get("article_id")
    article = ArticleInfo.objects.get(a_id=article_id)
    if token:
        collect = CollectInfo.objects.filter(col_article=article).filter(col_user=user_info)
        # 核对收藏
        if collect:
            return JsonResponse({"msg": "取消收藏", "status": "1", "a_collect_num": article.a_collect_num})
        else:
            return JsonResponse({"msg": "收藏", "status": "-1", "a_collect_num": article.a_collect_num})
    else:
        return JsonResponse({"msg": "喜欢", "status": "0", "a_collect_num": article.a_collect_num})


# 编辑-修改文章-get请求
def edit_article_get(request, article_id):
    responseData = {}
    article = ArticleInfo.objects.get(a_id=article_id)
    responseData['article'] = article

    # 文章的分类
    categories_list = ArticleCategory.objects.all()
    responseData['categories_list'] = categories_list

    return render(request, 'edit_article.html', context=responseData)


# 编辑-修改文章-post请求
def edit_article_post(request):
    # 获取
    article_id = request.POST.get("article_id")
    try:
        # 通过文章id去查询
        article = ArticleInfo.objects.get(a_id=article_id)
        # 标题
        article.a_title = request.POST.get("article_title")
        """
        这里是一个巧妙的处理，只有作者本人这个位置才可能出现编辑文章
        """
        token = request.session.get('token')
        article.a_author = UserInfo.objects.get(u_token=token).u_name

        # 预览图片
        pre_img_str = request.POST.get("article_pre_img")
        # 正则匹配
        if pre_img_str == "blog_default_img.png":
            article.a_pre_img = pre_img_str
        else:
            try:
                pre_img_obj = re.compile(r'[(]/media/(.*?)[)]')
                pre_img = pre_img_obj.findall(pre_img_str)[0].split(" ")[0]
                pre_img_path = os.path.join(settings.MEDIA_ROOT, pre_img)
                print("------hahahahhah-----")
                img = Image.open(pre_img_path)

                width, height = img.size
                if width <= height:
                    article.a_pre_img = "blog_default_img.png"
                else:
                    article.a_pre_img = pre_img

            except:
                pre_img_obj = re.compile(r'[(](.*?)[)]')
                # 请求url
                pre_img_url = pre_img_obj.findall(pre_img_str)[0]
                # print(pre_img_url, "爬虫url")

                # 请求头
                headers = {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
                }
                # 创建请求
                request_obj = urllib.request.Request(pre_img_url, headers=headers)
                response_obj = urllib.request.urlopen(request_obj)

                # 保存路径
                path = settings.MEDIA_URL + 'blog_img/' + str(uuid.uuid5(uuid.uuid4(), 'upload_img_path')).replace("-", "") + '/'

                # 绝对路径-目录
                abs_path = (settings.BASE_DIR + path).replace("\\", '/')
                if not os.path.exists(abs_path):
                    os.makedirs(abs_path)

                # 拼装本地保存图片的完整文件名
                filename = str(uuid.uuid5(uuid.uuid4(), 'upload_img')) + '_' + '.jpg'

                # 绝对路径-文件
                abs_file_path = abs_path + filename

                # 写入文件
                with open(abs_file_path, 'wb+') as fp:
                    fp.write(response_obj.read())

                img2 = Image.open(abs_file_path)
                width, height = img2.size

                if width >= height:
                    article.a_pre_img = path.split("/media/")[-1] + filename
                else:
                    article.a_pre_img = "blog_default_img.png"

        # 内容-md
        article.a_content_md = request.POST.get("article_content_md")
        # 文章字数
        article.a_word_num = str(len(request.POST.get("article_content_md")))

        # 内容-纯text
        len_ = len(request.POST.get("article_content_md"))
        if len_ <= 200:
            article.a_content_text = request.POST.get("article_content_text")[0:len_] + "..."
        else:
            article.a_content_text = request.POST.get("article_content_text")[0:200] + "..."

        # 分类
        article_class_id = eval(request.POST.get("article_class"))
        print(type(article_class_id), article_class_id)
        article.a_category = ArticleCategory.objects.get(id=article_class_id)

        # 发表
        is_publish = int(request.POST.get("is_publish"))
        if is_publish:
            article.a_is_publish = True
            # 声明关系
            article.a_user = UserInfo.objects.get(u_token=token)

            # 写入数据库
            article.save()

            # 标签
            tag_list = request.POST.get("article_tag").split(',')
            print(tag_list)

            tag_exist_all = ArticleTag.objects.all()
            temp_list = []
            for tag_exist in tag_exist_all:
                temp_list.append(tag_exist.tag_name)

            # 首先写入标签中
            for tag in tag_list:
                if tag in temp_list:
                    pass
                else:
                    if tag == "":
                        pass
                    else:
                        tag_save = ArticleTag()
                        tag_save.tag_name = tag
                        tag_save.save()

            # 文章-标签的声明关系
            tag_all = ArticleTag.objects.all()
            # 多对多
            for tag in tag_list:
                if tag == "":
                    pass
                else:
                    for tag_ in tag_all:
                        if tag == tag_.tag_name:
                            article.a_tag.add(tag_)

            article.save()

            return JsonResponse({"msg": "修改文章成功，3秒后跳转到文章详情页面", "status": "1"})

        else:
            article.a_is_publish = False
            # 声明关系
            article.a_user = UserInfo.objects.get(u_token=token)

            # 写入数据库
            article.save()

            return JsonResponse({"msg": "已保存到草稿箱，3秒后跳转到用户主页", "status": "2", "u_id": article.a_user.u_id})

    except:
        return JsonResponse({"msg": "修改文章失败", "status": "0"})


# 我的主页
def user_home(request, u_id):
    responseData = {}
    # 获取token
    # 登录的用户
    token = request.session.get("token")
    responseData['token'] = token
    user_token = UserInfo.objects.get(u_token=token)
    responseData['user_token'] = user_token

    # 通过id去查找此人
    user = UserInfo.objects.get(u_id=u_id)
    responseData['user'] = user
    articles = user.articleinfo_set.filter(a_is_publish=True).order_by('-a_create_time')
    responseData['articles'] = articles

    # 判断登录的人和这个主页的作者是不是一个人
    if user_token.u_id == user.u_id:
        responseData['is_same_people'] = True
    else:
        responseData['is_same_people'] = False

    # 性别展示
    responseData['u_sex'] = int(user.u_sex)

    # 关注的人数
    responseData['follow_num'] = len(user.u_follow.split(";")) - 1

    # 粉丝数量
    name_temp = user.u_name
    responseData['fans_num'] = UserInfo.objects.filter(u_follow__contains=name_temp).count() or "0"

    # 文章的篇数
    responseData['article_num'] = articles.count()

    # 文章总字数
    article_word_num = 0
    for article in articles:
        article_word_num += int(article.a_word_num)
    responseData["article_word_num"] = article_word_num

    # 收获的喜欢数量
    responseData['like_num'] = user.likeinfo_set.filter(l_user=user.u_id).count() or "0"

    # L币
    responseData['u_lb'] = user.u_lb

    # 草稿箱
    # 文章未发表
    articles_no_publish = user.articleinfo_set.filter(a_is_publish=False).order_by('-a_create_time')

    responseData['articles_no_publish'] = articles_no_publish

    # 与我相关的 评论
    comments_list = []
    for article in articles:
        commets = Comment.objects.filter(com_article=article)
        for comment in commets:
            comments_list.append(comment)

    responseData['comments_list'] = comments_list
    comments_list_len = len(comments_list)
    responseData['comments_list_len'] = comments_list_len

    return render(request, 'user_home.html', context=responseData)


# 我的主页--收藏与喜欢
# 点击进入之后，文章的渲染
def collect_like(request, u_id):
    responseData = {}
    # 被查看的用户--或作者
    user = UserInfo.objects.get(u_id=u_id)
    responseData['user'] = user
    # 这个文章是用来统计
    articles = user.articleinfo_set.filter(a_is_publish=True).order_by('-a_create_time')
    responseData['articles'] = articles

    # 登录的用户
    token = request.session.get("token")
    if token:
        user_token = UserInfo.objects.get(u_token=token)
        responseData['token'] = token
        responseData['user_token'] = user_token

        # 判断两个是否是同一人
        if user_token.u_id == user.u_id:
            responseData['is_same_people'] = True
        else:
            responseData['is_same_people'] = False

        # 性别展示
        responseData['u_sex'] = int(user.u_sex)

        # 关注的人数
        responseData['follow_num'] = len(user.u_follow.split(";")) - 1

        # 粉丝数量
        name_temp = user.u_name
        responseData['fans_num'] = UserInfo.objects.filter(u_follow__contains=name_temp).count() or "0"

        # 文章的篇数
        responseData['article_num'] = articles.count()

        # 文章总字数
        article_word_num = 0
        for article in articles:
            article_word_num += int(article.a_word_num)
        responseData["article_word_num"] = article_word_num

        # 收获的喜欢数量
        responseData['like_num'] = user.likeinfo_set.filter(l_user=user.u_id).count() or "0"

        # L币
        responseData['u_lb'] = user.u_lb

    # 收藏的文章
    user_collect_ = CollectInfo.objects.filter(col_user=user)
    user_collect_articles = []
    for user_collect__ in user_collect_:
        user_collect_articles.append(user_collect__.col_article)
    responseData['user_collect_articles'] = user_collect_articles

    # 喜欢的文章
    user_like_ = LikeInfo.objects.filter(l_user=user)
    user_like_articles = []
    for user_like__ in user_like_:
        user_like_articles.append(user_like__.l_article)
    responseData['user_like_articles'] = user_like_articles

    return render(request, 'user_collect_like.html', context=responseData)


# 删除文章--逻辑删除
def delete_article_logic(request, u_id, a_id):
    # 用户
    token = request.session.get("token")
    user_token = UserInfo.objects.get(u_token=token)

    user_article = ArticleInfo.objects.filter(a_user=user_token, a_id=a_id)

    # 该文章存在
    if user_article:
        # 删除 逻辑
        user_article[0].a_is_publish = False
        user_article[0].save()

    return HttpResponseRedirect(reverse('lwd:user_home', args={u_id}))


# 删除文章-完全删除-将草稿箱删除
def delete_article_complete(request, u_id, a_id):
    # 用户
    token = request.session.get("token")
    user_token = UserInfo.objects.get(u_token=token)

    user_article = ArticleInfo.objects.filter(a_user=user_token, a_id=a_id)

    # 该文章存在
    if user_article:
        user_article.delete()

    return HttpResponseRedirect(reverse('lwd:user_home', args={u_id}))


# 关于本人
def about_me(request):
    responseData = {}
    token = request.session.get('token')
    responseData['token'] = token
    if token:
        user_token = UserInfo.objects.get(u_token=token)
        responseData['user_token'] = user_token

    # 广告位轮播图
    ad_banners = AdBannerImg.objects.all()[:5]
    responseData['ad_banners'] = ad_banners

    return render(request, 'about_me.html', context=responseData)


# 用户设置
def user_setting_get(request, u_id):
    responseData = {}

    # token
    token = request.session.get("token")
    responseData['token'] = token

    if token:
        user_token = UserInfo.objects.get(u_token=token)
        responseData['user_token'] = user_token

    return render(request, 'user_setting.html', context=responseData)


# ############### user Basic 设置 ####################
# 用户头像修改
def update_avatar(request):
    # 获取数据
    file_name = request.FILES.get('update_avatar')
    print(file_name, '头像啊呀')
    token = request.session.get("token")
    user_token = UserInfo.objects.get(u_token=token)

    # 写入文件
    img_path = str(settings.BASE_DIR) + "/media/user_img" + "/" + str(user_token.u_name) + "/"
    if not os.path.exists(img_path):
        os.mkdir(img_path)

    img_file_path = os.path.join(img_path, file_name.name)
    with open(img_file_path, 'wb') as fp:
        for chunk in file_name.chunks():
            fp.write(chunk)

        # 修改头像
        user_token.u_img = "/user_img/" + str(user_token.u_name) + "/" + file_name.name
        user_token.save()

    return HttpResponse({"success": "success"})


# 其他基础设置
def basic_setting_other(request):
    # token
    token = request.session.get('token')
    user_token = UserInfo.objects.get(u_token=token)

    print(request.POST.get('user_name'))
    user_token.u_name = request.POST.get("user_name")
    user_token.u_is_simple = request.POST.get("u_is_simple")

    # 更新token
    user_token.u_token = str(uuid.uuid5(uuid.uuid4(), 'basic_setting'))
    user_token.save()

    # 状态保持
    request.session['token'] = user_token.u_token

    return JsonResponse({"msg": "修改成功", "status": "1"})


# 个人资料设置
def personal_setting(request):
    # token
    user_token = UserInfo.objects.get(u_token=request.session.get('token'))

    user_token.u_sex = request.POST.get('sex')
    user_token.u_intro = request.POST.get('intro')
    user_token.u_website = request.POST.get('website')
    user_token.save()

    return JsonResponse({'msg': "修改成功", 'status': "1"})


# 修改密码
def update_pwd(request):
    # token
    user_token = UserInfo.objects.get(u_token=request.session.get('token'))

    user_token.u_password = generate_password(request.POST.get('pwd'))
    user_token.save()
    return JsonResponse({'msg': "修改成功", 'status': "1"})


# 删除账号
def delete_account(request):
    # token
    token = request.session.get('token')
    # 逻辑删除账号
    user_token = UserInfo.objects.get(u_token=token)

    # user_token.delete()

    user_token.u_is_delete = True
    # 更新token
    user_token.u_token = ""
    user_token.save()

    request.session['token'] = user_token.u_token

    return JsonResponse({'msg': "删除成功", "status": '1'})


# 文章分类列表
def article_category(request, pk):
    responseData = {}
    # 获取token
    token = request.session.get('token')
    responseData['token'] = token

    # 用户
    user_token = UserInfo.objects.filter(u_token=token, u_is_delete=False)
    if len(user_token) > 0:
        user_token = user_token[0]
        responseData['user_token'] = user_token

    # 导入相应的分类
    cate = get_object_or_404(ArticleCategory, pk=pk)

    # 该分类的文章
    article_list = ArticleInfo.objects.filter(a_category=cate).order_by('-a_create_time')
    article_page = page_handler(request, article_list, 10)
    responseData['article_page'] = article_page

    # 显示标题
    responseData['a_category_0'] = cate.category_name

    return render(request, 'article_category.html', context=responseData)


# 归档文章
def archives(request, year, month):

    article_list = ArticleInfo.objects.filter(a_create_time__year=year, a_create_time__month=month).order_by('-a_create_time')

    # 分页处理
    article_page = page_handler(request, article_list, 5)


    token = request.session.get('token')
    if token:
        user_token = UserInfo.objects.get(u_token=token)
        return render(request, 'archives.html', context={'user_token': user_token, 'token': token, 'article_page': article_page})

    return render(request, 'archives.html', context={'article_page': article_page})


# 标签云
def article_tag(request, pk):
    responseData = {}
    # 获取token
    token = request.session.get('token')
    responseData['token'] = token

    # 用户
    user_token = UserInfo.objects.filter(u_token=token, u_is_delete=False)
    if len(user_token) > 0:
        user_token = user_token[0]
        responseData['user_token'] = user_token

    # 导入相应的分类
    tag = get_object_or_404(ArticleTag, pk=pk)

    # 该标签的文章
    article_list = ArticleInfo.objects.filter(a_tag=tag).order_by('-a_create_time')
    article_page = page_handler(request, article_list, 10)
    responseData['article_page'] = article_page

    # 显示标题
    tag_title = ArticleTag.objects.filter(pk=pk)
    responseData['a_tag_0'] = tag_title[0].tag_name

    return render(request, 'article_tag.html', context=responseData)


# 上传图片
@csrf_exempt
def upload_img(request):
    upload_file = request.FILES['editormd-image-file']
    print(upload_file, "上传文件名")
    if request.method == 'POST':
        success, message = 0, "上传失败"

        # 本地创建保存图片的文件夹
        path = settings.MEDIA_URL + 'blog_img/' + \
               str(uuid.uuid5(uuid.uuid4(), 'upload_img_path'))\
                   .replace("-", "") + '/'

        # 绝对路径-目录
        abs_path = (settings.BASE_DIR + path).replace("\\", '/')
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)

        # 拼装本地保存图片的完整文件名
        filename = str(uuid.uuid5(uuid.uuid4(), 'upload_img')) + '_' + str(upload_file.name)

        # 绝对路径-文件
        abs_file_path = abs_path + filename

        # 写入文件
        with open(abs_file_path, 'wb+') as f:
            for chunk in upload_file.chunks():
                f.write(chunk)

        success, message = 1, "上传成功"

        # 图片回显url
        url = path + filename

        # 返回格式
        data = {"success": success, "message": message, "url": url}
        return JsonResponse(data=data)
    else:
        data = {
            "success": 0,
            "message": "没有找到文件，或者文件不存在"
        }
        return JsonResponse(data=data)
