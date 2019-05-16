#!/Software/Python37
# -*- coding:utf-8 -*-
# 文件: urls
# 作者: lwd
# 时间: 2019/4/20 13:08
# IDE: PyCharm
from django.conf.urls import url

from Lwd import views

app_name = 'lwd'
urlpatterns = [
    # 测试
    url(r'^hello/$', views.hello),

    # 首页
    url(r'^$', views.index, name="index"),
    # url(r'^index/$', views.index, name='index'),

    # 注册
    url(r'^register/$', views.register_get, name="register"),
    url(r'^register_post/$', views.register_post, name="register_post"),
    # 检查账号是否存在
    url(r'^checkaccount/$', views.checkaccount, name="checkaccount"),
    # 检查用户名是否再存
    url(r'^checkname/$', views.checkname, name="checkname"),

    # 登录
    url(r'^login/$', views.login_get, name="login"),
    url(r'^login_post/$', views.login_post, name='login_post'),
    # 退出登录
    url(r'^quit/$', views.quit, name="quit"),
    # 判断用户是否登录
    url(r'^is_login/$', views.is_login, name="is_login"),

    # 写文章
    url(r'^write/$', views.write_article_get, name="write"),
    url(r'^write_post', views.write_article_post, name='write_post'),
    # 上传图片
    url(r'^upload_img/$', views.upload_img, name="upload_img"),

    # 文章详情
    url(r'^a_id/(\w+)/$', views.blog_detail, name="blog_detail"),

    # 核对是否被关注
    url(r'^checkfollow/$', views.check_is_follow, name="checkfollow"),
    # 关注取消
    url(r'^follow_or_cancel/$', views.follow_or_cancel, name="follow_or_cancel"),

    # 喜欢
    url(r'^like_handler/$', views.like_handler, name="like_handler"),
    # 收藏
    url(r'^collect_handler/$', views.collect_handler, name="collect_handler"),
    # 核对是否被喜欢
    url(r'^is_like/$', views.is_like, name='is_like'),
    # 核对是否被收藏
    url(r'^is_collect/$', views.is_collect, name="is_collect"),

    # 我的主页
    url(r'^u_id/(\w+)', views.user_home, name="user_home"),
    # 收藏与喜欢的文章
    url(r'^collect_like/u_id/(\w+)/$', views.collect_like, name="collect_like"),
    # 用户设置
    url(r'^setting/u_id/(\w+)', views.user_setting_get, name='user_setting'),
    # 头像修改
    url(r'^update_avatar/$', views.update_avatar, name="update_avatar"),
    # 基础设置-其他-如用户名、绑定邮箱、语言设置
    url(r'^basic_setting/$', views.basic_setting_other, name="basic_setting"),
    # 个人资料设置
    url(r'^personal_setting/$', views.personal_setting, name='personal_setting'),
    # 账号管理
    # 修改密码
    url(r'^update_pwd/$', views.update_pwd, name="update_pwd"),
    # 删除账号
    url(r'^delete_account/$', views.delete_account, name='delete_account'),

    # 编辑文章
    url(r'^edit/(\w+)/$', views.edit_article_get, name='edit'),
    url(r'^edit_post/', views.edit_article_post, name='edit_post'),
    # 删除文章-逻辑删除
    url(r'^delete_logic/(\w+)/(\w+)/$', views.delete_article_logic, name="delete_article_logic"),
    # 删除草稿-彻底删除
    url(r'^delete_com/(\w+)/(\w+)/$', views.delete_article_complete, name='delete_article_com'),

    # 关于本站
    url(r'^about_me/$', views.about_me, name="about_me"),


    # 搜索页
    # url(r'^search/$', views.lwd_search, name='lwd_search')

    # 文章分类列表
    url(r'^article_category/(?P<pk>[0-9]+)/$', views.article_category, name='article_category'),

    # 归档功能
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),

    # 标签云
    url(r'^article_tag/(?P<pk>[0-9]+)/$', views.article_tag, name='article_tag'),









]



