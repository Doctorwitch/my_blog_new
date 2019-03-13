
from django.conf.urls import url
from comment.views import Board

urlpatterns = [
    url(r'^board$', Board.as_view(), name='board'),
]

