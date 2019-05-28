
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Memes, Comment, Like
from .forms import (
    MemeForm,
    UserRegistrationForm,
    CommentForm,
    LikeForm
)


class IndexView(ListView):
    template_name = 'memes/index.html'
    model = Memes
    queryset = Memes.objects.all().order_by('-id')
    paginate_by = 10
    context_object_name = "memes"

    def get_context_data(self, **kwargs):
        paginator = Paginator(self.queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            memes = paginator.page(page)
        except PageNotAnInteger:
            #If page is not an integer deliver first page
            memes = paginator.page(1)
        except EmptyPage:
            memes = paginator(paginator.num_pages)
            #Deliver last page

        context = super(IndexView, self).get_context_data(**kwargs)
        context['memes'] = memes
        context['comment_form'] = CommentForm()
        context['like_form'] = LikeForm()
        return context


class MakeMemesView(CreateView):
    template_name = 'memes/makeMemes.html'
    success_url = '/'
    form_class = MemeForm

    def form_valid(self, form):
        if form.cleaned_data['top_caption']:
            form.cleaned_data['top_caption'] = Memes.fix_caption(form.cleaned_data['top_caption'])
        else:
            form.cleaned_data['top_caption'] = '_'

        if form.cleaned_data['bottom_caption']:
            form.cleaned_data['bottom_caption'] = Memes.fix_caption(form.cleaned_data['bottom_caption'])
        else:
            form.cleaned_data['bottom_caption'] = '_'

        form.save()
        return HttpResponseRedirect(self.success_url)


class UserRegistrationView(CreateView):
    template_name = 'memes/user_registration.html'
    model = User
    form_class = UserRegistrationForm
    success_url = '/accounts/login'

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

    def form_invalid(self, form):
        return HttpResponseRedirect('/memes/profile/register/')


@method_decorator(login_required, name='dispatch')
class ViewProfileView(TemplateView):
    template_name = 'memes/view_profile.html'


@method_decorator(login_required, name='dispatch')
class EditProfileView(UpdateView):
    template_name = 'memes/edit_profile.html'
    success_url = '/memes/profile/view'
    model = User
    fields = (
        'username',
        'first_name',
        'last_name',
        'email'
    )


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(PasswordChangeView):
    template_name = 'memes/change_password.html'
    success_url = '/'
    model = User

    def form_invalid(self, form):
        return HttpResponseRedirect('/memes/password/{}/'.format(form.user.pk))


@method_decorator(login_required, name='dispatch')
class CommentView(CreateView):
    http_method_names = ['post']
    form_class = CommentForm
    success_url = '/'

    def form_valid(self, form):
        Comment.objects.create(
            content=form.cleaned_data['content'],
            meme=Memes.objects.get(pk=self.request.POST.get('meme_id', -1)),
            user=self.request.user
        )
        return HttpResponseRedirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class AddLikeView(CreateView):
    http_method_names = ['post']
    model = Like
    form_class = LikeForm
    success_url = '/'
    exclude = [
        'meme',
        'user'
    ]

    def form_valid(self, form):
        Like.objects.create(
            meme=Memes.objects.get(pk=self.request.POST.get('meme_id', -1)),
            user=self.request.user
        )
        return HttpResponseRedirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class DeleteLikeView(DeleteView):
    http_method_names = ['post']
    model = Like
    success_url = '/'

