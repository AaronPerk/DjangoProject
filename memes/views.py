
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Memes, Comment
from .forms import MemeForm, EditProfileForm, UserRegistrationForm, CommentForm
import re

class IndexView(TemplateView):

    template_name = 'memes/index.html'

    def get(self, request, *args, **kwargs):
        queryset_list = Memes.objects.all().order_by('-id')

        paginator = Paginator(queryset_list, 10)  # Show 10 memes per page

        page = request.GET.get('page')

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            #If page is not an integer deliver first page
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator(paginator.num_pages)
            #Deliver last page


        context = super(IndexView, self).get_context_data(**kwargs)
        context['memes'] = queryset

        comment_form = CommentForm()
        context['form'] = comment_form

        return render(request, self.template_name, context)


class MakeMemesView(TemplateView):
    template_name = 'memes/makeMemes.html'

    def get(self, request, *args, **kwargs):

        form = MemeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = MemeForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect('/')


class UserRegistrationView(TemplateView):
    template_name = 'memes/user_registration.html'

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect('/')


@method_decorator(login_required, name='dispatch')
class ViewProfileView(TemplateView):
    template_name = 'memes/view_profile.html'


@method_decorator(login_required, name='dispatch')
class EditProfileView(TemplateView):
    template_name = 'memes/edit_profile.html'

    def get(self, request, *args, **kwargs):

        form = EditProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():

            form.save()
            return HttpResponseRedirect('/memes/profile/view')


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(TemplateView):
    template_name = 'memes/change_password.html'

    def get(self, request, *args, **kwargs):

        form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():

            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/memes/password')


class CommentView(CreateView):
    http_method_names = ['post']
    form_class = CommentForm
    success_url = '/'

    def form_valid(self, form):
        form.cleaned_data['user'] = self.request.user
        form.cleaned_data['meme'] = Memes.objects.get(pk=self.request.POST.get('meme_id', -1))
        form.save()
        return HttpResponseRedirect(self.success_url)