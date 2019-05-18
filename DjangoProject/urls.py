
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^$', include('memes.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^memes/', include('memes.urls'))
]
