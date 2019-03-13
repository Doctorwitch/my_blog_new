
from django.conf.urls import url
from article.views import Article, ArticleDetail

urlpatterns = [
    url(r'^(\d+)$', ArticleDetail.as_view(), name='文章详情'),
    url(r'^$', Article.as_view(), name='文章页'),
]


