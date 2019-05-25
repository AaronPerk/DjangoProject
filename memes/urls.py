from django.conf.urls import url
from memes.views import(
    IndexView,
    MakeMemesView,
    ViewProfileView,
    EditProfileView,
    UserRegistrationView,
    ChangePasswordView,
    CommentView
)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^make_memes/', MakeMemesView.as_view(), name='make_memes'),
    url(r'^profile/view', ViewProfileView.as_view(), name='view_profile'),
    url(r'^profile/edit', EditProfileView.as_view(), name='edit_profile'),
    url(r'^profile/register', UserRegistrationView.as_view(), name='user_registration'),
    url(r'^password/$', ChangePasswordView.as_view(), name='change_password'),
    url(r'^comment/$', CommentView.as_view(), name='comment')
]