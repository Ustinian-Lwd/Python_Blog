from django.contrib import admin
from django.contrib import admin
from .models import ArticleInfo, UserInfo, FollowInfo, IndexBannerImg, AdBannerImg, CollectInfo, LikeInfo, \
    ArticleCategory, ArticleTag


# 文章表admin
class ArticleInfoAdmin(admin.ModelAdmin):
    # 列表页的属性
    # 显示字段(需要显示什么字段，就写上什么字段即可)
    list_display = ['pk', 'a_title', 'a_author', 'a_content_text', "a_word_num", "a_create_time", "a_update_time", 'a_like_num', 'a_collect_num', 'a_comment_num', 'a_is_publish', 'a_views', 'a_user']
    # 过滤器(过滤字段)
    list_filter = ['a_title']
    # 搜索字段
    search_fields = ['a_title']
    # 分页(多少条为一页)
    list_per_page = 10


# 用户admin
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'u_account', 'u_name', 'u_password', 'u_sex', 'u_intro', 'u_level', 'u_lb', 'u_follow']
    # 过滤器(过滤字段)
    list_filter = ['u_name']
    # 搜索字段
    search_fields = ['u_name']
    # 分页(多少条为一页)
    list_per_page = 10


# 轮播图
# 首页
class IndexBannerIngAdmin(admin.ModelAdmin):
    list_display = ['pk', 'b_img_name', 'b_info_content', 'b_create_time', 'ib_img_upload', 'ib_kind']
    list_filter = ['b_img_name']
    # 搜索字段
    search_fields = ['b_img_name']
    # 分页(多少条为一页)
    list_per_page = 10


# 广告位
class AdBannerImgAdmin(admin.ModelAdmin):
    list_display = ['pk', 'b_img_name', 'b_info_content', 'b_create_time', 'ab_img_upload', 'ab_kind']
    list_filter = ['b_img_name']
    # 搜索字段
    search_fields = ['b_img_name']
    # 分页(多少条为一页)
    list_per_page = 10


# 关注表
class FollowAdmin(admin.ModelAdmin):
    list_display = ['pk', 'f_user1', 'f_user2_name']
    list_filter = ['f_user1']
    # 搜索字段
    search_fields = ['f_user1']
    # 分页(多少条为一页)
    list_per_page = 10


# 喜欢表
class LikeAdmin(admin.ModelAdmin):
    list_display = ['l_id', 'l_article', 'l_user']
    list_filter = ['l_article']
    # 搜索字段
    search_fields = ['l_article']
    # 分页(多少条为一页)
    list_per_page = 10


# 收藏表
class CollectAdmin(admin.ModelAdmin):
    list_display = ['pk', 'col_article', 'col_user']
    list_filter = ['col_article']
    # 搜索字段
    search_fields = ['col_article']
    # 分页(多少条为一页)
    list_per_page = 10


# 分类
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'category_name']
    list_filter = ['category_name']
    # 搜索字段
    search_fields = ['category_name']
    # 分页(多少条为一页)
    list_per_page = 10

# 标签
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ['pk', 'tag_name']
    list_filter = ['tag_name']
    # 搜索字段
    search_fields = ['tag_name']
    # 分页(多少条为一页)
    list_per_page = 10


# 文章表
admin.site.register(ArticleInfo, ArticleInfoAdmin)
# 用户表
admin.site.register(UserInfo, UserInfoAdmin)
# 关注表
admin.site.register(FollowInfo, FollowAdmin)
# 收藏表
admin.site.register(CollectInfo, CollectAdmin)
# 喜欢表
admin.site.register(LikeInfo, LikeAdmin)
# 分类表
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
# 标签表
admin.site.register(ArticleTag, ArticleTagAdmin)
# 轮播图
# 首页
admin.site.register(IndexBannerImg, IndexBannerIngAdmin)
# 广告位
admin.site.register(AdBannerImg, AdBannerImgAdmin)
