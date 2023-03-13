from django import template
from django.http import request
from ..models import (
    Track,
)
from category.models import (
    ArtistCategory,
    TrackCategory,
)
from site_control.models import (
    Sidebar,
    HomePage,
)

register = template.Library()

@register.inclusion_tag("remix/footer.html")
def footer():
    return{
        'tracks':Track.objects.active().order_by('-published')[:5],
    }

@register.inclusion_tag("remix/navbar/navbar.html",takes_context=True)
def navbar(context):
    return{
        'track_categories':TrackCategory.objects.active(),
        'artist_categories':ArtistCategory.objects.active(),
    }

@register.inclusion_tag("remix/sidbar.html",takes_context=True)
def sidbar(context):
    return{
        'static_sidbars':HomePage.objects.filter(status=True)[:2],
        'dynamic_sidbars':Sidebar.objects.filter(status=True)[:4],
    }

@register.simple_tag
def call_method(category_obj,filter):
    method=getattr(category_obj, 'find_tracks')
    return method(filter)

