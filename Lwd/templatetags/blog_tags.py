from django import template
from django.db.models import Count

from Lwd.models import ArticleInfo, ArticleCategory, AdBannerImg, IndexBannerImg, ArticleTag

# 模板标签自定义对象
register = template.Library()


# 最新文章
@register.simple_tag
def get_recent_article(num=5):
    return ArticleInfo.objects.filter(a_is_publish=True).order_by('-a_create_time')[:num]


# 推荐文章
@register.simple_tag
def get_recommend_article(num=5):
    return ArticleInfo.objects.filter(a_is_publish=True).order_by('-a_like_num')[:num]


# 热评排行
@register.simple_tag
def get_hot_comment_article(num=5):
    return ArticleInfo.objects.filter(a_is_publish=True).order_by('-a_comment_num')[:num]


# 收藏排行
@register.simple_tag
def get_collect_article(num=5):
    return ArticleInfo.objects.filter(a_is_publish=True).order_by('-a_collect_num')[:num]


# 归档功能
@register.simple_tag
def archives():
    return ArticleInfo.objects.dates('a_create_time', 'month', order='DESC').filter(a_is_publish=True)


# 总分类
@register.simple_tag
def get_categories():
    return ArticleCategory.objects.annotate(num_articles=Count("articleinfo")).filter(num_articles__gt=0)


# 用户的分类
@register.simple_tag
def get_user_categories(user):
    return ArticleCategory.objects.filter(articleinfo__a_user=user, articleinfo__a_is_publish=True).annotate(num_articles=Count("articleinfo")).filter(num_articles__gt=0)


# 得到Python分类的名字
@register.simple_tag
def get_python_category():
    return ArticleCategory.objects.all()[:5]


# 得到Share分类的名字
@register.simple_tag
def get_share_category():
    return ArticleCategory.objects.all()[6:14]


# 得到Other分类的名字
@register.simple_tag
def get_other_category():
    return ArticleCategory.objects.all()[15:]


# 标签云
@register.simple_tag
def get_tags():
    return ArticleTag.objects.annotate(num_articles=Count('articleinfo')).filter(num_articles__gt=0)


# 广告轮播图
@register.simple_tag
def get_ad_banner():
    return AdBannerImg.objects.all().order_by("-b_create_time")[:5]


# 首页轮播图
@register.simple_tag
def get_index_banner():
    return IndexBannerImg.objects.all().order_by("-b_create_time")[:5]




