
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    url(r'^$', include('memes.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', LoginView.as_view(redirect_authenticated_user=True)),
    url(r'^accounts/logout/$', LogoutView.as_view()),
    url(r'^memes/', include('memes.urls'))
]
