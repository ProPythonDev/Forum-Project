__author__ = 'liuhui'

from haystack import indexes
from blog.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    content = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    tags = indexes.CharField(model_attr='tags')
    category = indexes.DateTimeField(model_attr='category')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
