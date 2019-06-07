from django.core.signals import request_started, request_finished
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(request_started)
def request_started_callback(sender, **kwargs):
    print('Request Received')


@receiver(request_finished)
def request_finished_callback(sender, **kwargs):
    print('Response Served')


@receiver(post_save, sender=User)
def create_user_profile(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])
