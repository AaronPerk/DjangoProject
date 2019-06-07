# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class MemesConfig(AppConfig):
    name = 'memes'

    def ready(self):
        from .signals import (
            request_started_callback,
            request_finished_callback
        )
