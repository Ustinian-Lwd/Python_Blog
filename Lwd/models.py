from django.db import models


# 用户模型类 user_info
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible


# 用户表
@python_2_unicode_compatible
class UserInfo(models.Model):
    # 用户id
    u_id = models.CharField(primary_key=True, unique=True, null=False, max_length=255)
    # 账号：手机号，唯一
    u_account = models.CharField(max_length=255, unique=True, null=False)
    # 用户名 唯一
    u_name = models.CharField(max_length=200, unique=True, null=False)
    # 密码
    u_password = models.CharField(max_length=200)
    # 头像
    u_img = models.CharField(max_length=255, default="user_default_img.png")
    # 性别
    # 0 男
    # 1 女
    # 2 未知
    u_sex = models.CharField(max_length=20, default=2)
    # 邮箱 绑定邮箱
    u_email = models.CharField(max_length=200)
    # 个人网站
    u_website = models.CharField(max_length=200)
    # 网站的语言是否为简体
    # 1 中文
    # 0 繁体
    u_is_simple = models.BooleanField(default=1)
    # 个人简介
    u_intro = models.TextField(default="这个人很懒，什么都没写")
    # 逻辑删除
    u_is_delete = models.BooleanField(default=0)
    # 用户积分
    u_point = models.CharField(max_length=200, default=0)
    # 用户等级
    u_level = models.CharField(max_length=50, default=1)
    # 积分和等级的关系
    # 一级等于100积分
    # 发表文章+10积分
    # 浏览一篇文章，+1积分
    # 等等后期完善
    # 1-20级 普通用户
    # 20-30 青铜
    # 31-40 白银
    # 41-50 黄金
    # 51-60 铂金
    # 61-70 钻石
    # 71-99 至尊

    # 用户L币
    u_lb = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # token
    u_token = models.CharField(max_length=200)
    # 用户关注
    u_follow = models.TextField(default="", null=True)

    def __str__(self):
        return self.u_name

    class Meta:
        db_table = "user_info"


# 文章的分类
@python_2_unicode_compatible
class ArticleCategory(models.Model):
    # 文章分类
    # 后端开发，HTML基础，Vue，Node等
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'article_category'


# 文章的标签
@python_2_unicode_compatible
class ArticleTag(models.Model):
    # 文章标签
    # 文章标签  可以有多个
    # 属于学习，书序人工智能
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name

    class Meta:
        db_table = 'article_tag'


# 文章模型类 article_info
# 用户和文章是一对多的关系
# 即一个人可以发表多篇文章
@python_2_unicode_compatible
class ArticleInfo(models.Model):
    # 文章id
    a_id = models.CharField(max_length=255, primary_key=True)
    # 文章标题
    a_title = models.CharField(max_length=255)
    # 文章作者
    # 说明这里的文章作者是在发表文章的时候，用户token的那个人
    a_author = models.CharField(max_length=200)
    # 文章内容-md
    a_content_md = models.TextField()
    # 文章内容-纯文本
    a_content_text = models.TextField()
    # 文章预览图片
    a_pre_img = models.CharField(max_length=200, default="blog_default_img.png")

    # 文章字数
    a_word_num = models.CharField(max_length=200, default="0")
    # 文章创建时间
    a_create_time = models.DateTimeField(auto_now_add=True)
    # 文章修改时间
    a_update_time = models.DateTimeField(auto_now=True)
    # 文章喜欢数量
    a_like_num = models.IntegerField(default=0)
    # 收藏数量
    a_collect_num = models.IntegerField(default=0)
    # 文章评论数量
    a_comment_num = models.IntegerField(default=0)
    # 文章是否是草稿还是正式发表
    # 草稿 0
    # 发表 1
    a_is_publish = models.BooleanField()

    # 阅览量
    a_views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.a_title

    # ... 其它已有的模型方法
    def increase_views(self):
        self.a_views += 1
        self.save(update_fields=['a_views'])

    # 声明关系
    # 和用户之间的关系
    # 其实这和当时写文章时，那个作者是一致的，一个用户可以发表多篇文章为了更好的获取用户的资料
    a_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    # 文章分类的关系
    a_category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE)
    a_tag = models.ManyToManyField(ArticleTag, blank=True)

    # 文章标签的关系

    class Meta:
        db_table = "article_info"

    def get_absolute_url(self):
        return reverse('lwd:blog_detail', args={self.pk})


# 关注表
class FollowInfo(models.Model):
    # 关注表的id
    f_id = models.CharField(max_length=255, primary_key=True)

    # 外键
    # 其中一个用户
    f_user1 = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    # 关注另外一个用户
    f_user2_name = models.CharField(max_length=255, default="")

    class Meta:
        db_table = 'follow_info'


# 喜欢like模型
# 一篇文章可以被很多人喜欢
# 或者是可以对应很多记录
class LikeInfo(models.Model):
    # 喜欢表的id
    l_id = models.CharField(max_length=255, primary_key=True)

    # 外键
    # 两个外键
    # 文章id
    l_article = models.ForeignKey(ArticleInfo, on_delete=models.CASCADE)

    # 用户id
    l_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'like_info'


# 收藏模型
class CollectInfo(models.Model):
    # 喜欢表的id
    col_id = models.CharField(max_length=255, primary_key=True)

    # 外键
    # 两个外键
    # 文章id
    col_article = models.ForeignKey(ArticleInfo, on_delete=models.CASCADE)

    # 用户id
    col_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'collect_info'


# 轮播图模型
# 轮播图基类
class BannerImg(models.Model):
    # id自动生成

    # 图片的名字注入img的alt title
    b_img_name = models.CharField(max_length=255)

    # 轮播图描述
    b_info_content = models.CharField(max_length=255)

    # 轮播图创建的时间
    b_create_time = models.DateTimeField(auto_now_add=True)

    # 抽象化父类
    class Meta:
        abstract = True


# 首页轮播图
class IndexBannerImg(BannerImg):

    # 轮播图name如图片的alt，title之类的
    ib_img_upload = models.ImageField(upload_to="banner/index_banner/%Y/%m", max_length=255)

    # 种类是属于哪一种轮播图
    ib_kind = models.CharField(max_length=255, default="index")

    class Meta:
        db_table = 'index_banner'


# vip广告位轮播图
class AdBannerImg(BannerImg):

    # 轮播图name如图片的alt，title之类的
    ab_img_upload = models.ImageField(upload_to="banner/ad_banner/%Y/%m", max_length=255)

    # 轮播图的种类
    ab_kind = models.CharField(max_length=255, default="vip_ad")

    # 广告跳转的链接
    ab_link = models.CharField(max_length=255)

    class Meta:
        db_table = "ad_banner"
