from haystack import indexes
from article.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        # 修改此处，为你自己的model
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
