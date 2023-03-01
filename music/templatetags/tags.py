from django import template
from ..models import Track,Category
from django.http import request

register = template.Library()

@register.inclusion_tag("remix/footer.html")
def footer():
    return{
        'tracks':Track.objects.active().order_by('-published')[:5],
    }

@register.inclusion_tag("remix/navbar/navbar.html",takes_context=True)
def navbar(context):
    return{
        'categories':Category.objects.active(),
    }

@register.inclusion_tag("remix/slidbar.html",takes_context=True)
def slidbar(context):
    return{
        'last_remixes':Track.objects.remix().order_by('-published')[:15],
        'last_podcasts':Track.objects.podcast().order_by('-published')[:15],
    }
