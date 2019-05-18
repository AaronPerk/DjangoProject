from django import forms
from .services import get_meme_options

class MemeForm(forms.Form):

    meme_names = get_meme_options()

    meme_name = forms.CharField(label='Meme Name', widget=forms.Select(
        choices=meme_names
        ))
    top_caption = forms.CharField(label='Top Caption', max_length=32, widget=forms.TextInput())
    bottom_caption = forms.CharField(label='Bottom Caption', max_length=32, widget=forms.TextInput())