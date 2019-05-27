from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .services import get_meme_options
from .models import Memes, Comment, Like

class MemeForm(forms.ModelForm):

    class Meta:
        model = Memes
        fields = [
            'meme_name',
            'top_caption',
            'bottom_caption'
        ]

    meme_name = forms.CharField(label='Meme Name', widget=forms.Select(
        choices=get_meme_options()
        ))


class CommentForm(forms.ModelForm):

    content = forms.CharField(
        label='',
        max_length=128,
        widget=forms.TextInput(attrs={'placeholder': 'Comment...'})
    )

    def save(self, commit=True):
        Comment.objects.create(
            content=self.cleaned_data['content'],
            meme=self.cleaned_data['meme'],
            user=self.cleaned_data['user']
        )

    class Meta:
        model = Comment
        exclude = (
            'user',
            'meme',
            'created_at'
        )


class LikeForm(forms.ModelForm):

    class Meta:
        model = Like
        exclude = (
            'user',
            'meme'
        )

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