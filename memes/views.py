
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Memes
from .forms import MemeForm, EditProfileForm, UserRegistrationForm
import re


class IndexView(TemplateView):

    template_name = 'memes/index.html'

<<<<<<< HEAD
    def get_context_data(self, request, *args, **kwargs):
        queryset_list = []
        memes = list(Memes.objects.all())
        memes.reverse()
        for meme in memes:
            queryset_list.append(get_api_url(meme))

        paginator = Paginator(queryset_list, 10)  # Show 5 memes per page

        page = request.GET.get('page')

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            #If page is not an integer deliver first page
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator(paginator.num_pages)

        context = {
                'meme_urls': queryset
            }

        return context


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
