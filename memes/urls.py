from django.conf.urls import url
from memes.views import(
    IndexView,
    MakeMemesView,
    ViewProfileView,
    EditProfileView,
    UserRegistrationView,
    ChangePasswordView,
    CommentView,
    AddLikeView,
    DeleteLikeView
)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^make_memes/', MakeMemesView.as_view(), name='make_memes'),
    url(r'^profile/view', ViewProfileView.as_view(), name='view_profile'),
    url(r'^profile/edit/(?P<pk>\d+)/$', EditProfileView.as_view(), name='edit_profile'),
    url(r'^profile/register/', UserRegistrationView.as_view(), name='user_registration'),
    url(r'^password/(?P<pk>\d+)/$', ChangePasswordView.as_view(), name='change_password'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^like/add/$', AddLikeView.as_view(), name='like_add'),
    url(r'^like/delete/(?P<pk>\d+)/$', DeleteLikeView.as_view(), name='like_delete')
]