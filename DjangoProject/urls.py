
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LoginView

urlpatterns = [
    url(r'^$', include('memes.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', LoginView.as_view(redirect_authenticated_user=True)),
    url(r'^memes/', include('memes.urls'))
]
