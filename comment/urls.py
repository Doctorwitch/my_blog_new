
from django.conf.urls import url
from comment.views import Board, CommentTree

urlpatterns = [
    url(r'^board$', Board.as_view(), name='board'),
    url(r'^comment_tree$', CommentTree.as_view(), name='comment_tree')
]

