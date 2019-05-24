from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .services import get_meme_options

class MemeForm(forms.Form):

    meme_names = get_meme_options()

    meme_name = forms.CharField(label='Meme Name', widget=forms.Select(
        choices=meme_names
        ))
    top_caption = forms.CharField(label='Top Caption', max_length=32, widget=forms.TextInput())
    bottom_caption = forms.CharField(label='Bottom Caption', max_length=32, widget=forms.TextInput())


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True);

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        )
