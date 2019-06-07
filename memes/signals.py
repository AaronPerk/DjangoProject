from django.core.signals import request_started, request_finished
from django.dispatch import receiver


@receiver(request_started)
def request_started_callback(sender, **kwargs):
    print('Request Received')


@receiver(request_finished)
def request_finished_callback(sender, **kwargs):
    print('Response Served')
