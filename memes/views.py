
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from models import Memes
from .forms import MemeForm
import re


class IndexView(TemplateView):
    template_name = 'memes/index.html'

    def get(self, request, *args, **kwargs):
        context = {
            'meme_urls': []
        }

        memes = list(Memes.objects.all())
        memes.reverse()
        for meme in memes[:10]:
            context['meme_urls'].append(get_api_url(meme))

        return render(request, self.template_name, context)


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
