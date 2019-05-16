from django.conf.urls import url
from comments import views

app_name = 'comments'
urlpatterns = [
    # 添加评论
    url(r'^comment/a_id/(\w+)/$', views.article_comment, name='article_comment'),

    # 删除评论
    url(r'^delete_comment/(?P<pk>[0-9]+)/$', views.delete_comment, name='delete_comment'),

]
