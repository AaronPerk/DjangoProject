import re
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Memes(models.Model):
    meme_name = models.CharField(max_length=64)
    top_caption = models.CharField(max_length=32)
    bottom_caption = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Memes"

    def get_api_url(self):
        c1 = '_' if not self.top_caption else self.top_caption
        c2 = '_' if not self.bottom_caption else self.bottom_caption
        return (
            'https://memegen.link/{}/{}/{}.jpg'.format(
                self.meme_name,
                c1,
                c2
            )
        )

    @staticmethod
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


class Comment(models.Model):
    content = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now())
    meme = models.ForeignKey(Memes)
    user = models.ForeignKey(User)


class Like(models.Model):
    meme = models.ForeignKey(Memes)
    user = models.ForeignKey(User)
