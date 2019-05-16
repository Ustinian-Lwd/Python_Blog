"""Python_Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from Lwd.feeds import AllPostsRssFeed
from Python_Blog import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^xadmin/', xadmin.site.urls),

    # 首页主要功能
    url(r'', include('Lwd.urls', namespace='lwd')),
    # 评论功能
    url(r'^comments/', include('comments.urls')),
    # 全文检索
    url(r'^search/', include('haystack.urls')),
    # rss订阅
    url(r'^all/rss/$', AllPostsRssFeed(), name='rss'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 新加入
