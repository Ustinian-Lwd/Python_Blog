from haystack import indexes
from Lwd.models import ArticleInfo, UserInfo


class ArticleInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ArticleInfo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class UserInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return UserInfo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

