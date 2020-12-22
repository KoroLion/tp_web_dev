from django import template
from moments_feed.models import Like

register = template.Library()


@register.simple_tag
def is_liked_by(moment, user):
    return int(Like.objects.filter(moment=moment, author=user).count() != 0)
