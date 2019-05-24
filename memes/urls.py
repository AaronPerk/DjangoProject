from django.conf.urls import url
from memes.views import IndexView, MakeMemesView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^make_memes/', MakeMemesView.as_view(), name='make_memes'),
]