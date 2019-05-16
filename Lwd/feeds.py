

from django.contrib.syndication.views import Feed

from .models import ArticleInfo


class AllPostsRssFeed(Feed):
    # 显示在聚合阅读器上的标题
    title = "Lwd's Blog"

    # 通过聚合阅读器跳转到网站的地址
    link = "/"

    # 显示在聚合阅读器上的描述信息
    description = "Lwd's Blog | 李易阳"

    # 需要显示的内容条目
    def items(self):
        return ArticleInfo.objects.all()

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.a_tag, item.a_title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.a_content_md

    # def item_link(self, item):
    #     return item.get_absolute_url()



