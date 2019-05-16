from django.contrib import admin
from comments.models import Comment


# 评论管理
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'com_content', 'com_created_time', 'com_article', 'com_user']
    list_filter = ['com_article']
    # 搜索字段
    search_fields = ['com_content']
    # 分页(多少条为一页)
    list_per_page = 10


# 注册
admin.site.register(Comment, CommentAdmin)