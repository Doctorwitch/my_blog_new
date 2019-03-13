
from django.conf.urls import url
from mood.views import Mood

urlpatterns = [
    url(r'^$', Mood.as_view(), name='心情')
]

