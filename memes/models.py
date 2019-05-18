import re
from django.db import models

# Create your models here.
class Memes(models.Model):
    meme_name = models.CharField(max_length=64)
    top_caption = models.CharField(max_length=32)
    bottom_caption = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Memes"