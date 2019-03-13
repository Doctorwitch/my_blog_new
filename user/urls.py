from django.conf.urls import url
from user.views import Register, Index, About, Login, Active, Logout

urlpatterns = [
    url(r'^register$', Register.as_view(), name='register'),
    url(r'^active/(?P<token>.*)$', Active.as_view(), name='active'),
    url(r'^login$', Login.as_view(), name='login'),
    url(r'^logout', Logout.as_view(), name='logout'),
    url(r'^about$', About.as_view(), name='about'),
    url(r'^index$', Index.as_view(), name='index'),
    url(r'^$', Index.as_view(), name='index'),
]
