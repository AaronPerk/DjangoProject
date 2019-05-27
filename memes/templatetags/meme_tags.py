from django import template

register = template.Library()

@register.filter()
def get_like_from_user_and_meme(value, arg):
    try:
        return value.like_set.get(meme=value, user=arg).pk
    except :
        return None