
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from models import Memes
from .forms import MemeForm, EditProfileForm, UserRegistrationForm
import re


class IndexView(TemplateView):
    template_name = 'memes/index.html'

    def get_context_data(self, **kwargs):

        memes = list(Memes.objects.all())
        memes.reverse()

        context = super(IndexView, self).get_context_data(**kwargs)
        context['meme_urls'] = []

        for meme in memes[:10]:
            context['meme_urls'].append(get_api_url(meme))

        return context

class MakeMemesView(TemplateView):
    template_name = 'memes/makeMemes.html'

    def get(self, request, *args, **kwargs):

        form = MemeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = MemeForm(request.POST)

        if form.is_valid():

            if form.cleaned_data['top_caption']:
                form.cleaned_data['top_caption'] = fix_caption(form.cleaned_data['top_caption'])
            else:
                form.cleaned_data['top_caption'] = '_'

            if form.cleaned_data['bottom_caption']:
                form.cleaned_data['bottom_caption'] = fix_caption(form.cleaned_data['bottom_caption'])
            else:
                form.cleaned_data['bottom_caption'] = '_'

            Memes.objects.create(
                meme_name=form.cleaned_data['meme_name'],
                top_caption=form.cleaned_data['top_caption'],
                bottom_caption=form.cleaned_data['bottom_caption']
            )
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


def get_api_url(meme):
    c1 = '_' if not meme.top_caption else meme.top_caption
    c2 = '_' if not meme.bottom_caption else meme.bottom_caption
    return (
        'https://memegen.link/{}/{}/{}.jpg'.format(
            meme.meme_name,
            c1,
            c2
        )
    )


def fix_caption(caption):
    d = {
        ' ': '_',
        '_': '__',
        '-': '--',
        '?': '~q',
        '%': '~p',
        '#': '~h',
        '/': '~s',
        '"': r"''"
    }

    pattern = '|'.join(re.escape(k) for k in d)
    return re.sub(pattern, lambda m: d.get(m.group(0).upper()), caption, flags=re.IGNORECASE)
