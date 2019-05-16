from django.db import models
from django.utils.six import python_2_unicode_compatible


# python_2_unicode_compatible 装饰器用于兼容 Python2
@python_2_unicode_compatible
class Comment(models.Model):
    # id默认生成
    # 自动增长

    # 评论内容
    com_content = models.TextField()
    # 评论时间
    com_created_time = models.DateTimeField(auto_now_add=True)

    # 声明关系
    # 跟文章的关系
    com_article = models.ForeignKey('Lwd.ArticleInfo', on_delete=models.CASCADE)
    # 跟用户的关系
    com_user = models.ForeignKey('Lwd.UserInfo', on_delete=models.CASCADE)

    class Meta:
        db_table = "comment_info"

    def __str__(self):
        return self.com_content[:20]
