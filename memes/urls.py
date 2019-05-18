from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^make_memes/', views.make_memes, name='make_memes'),
]