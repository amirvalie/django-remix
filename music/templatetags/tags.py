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
from about.models import (
    AboutMe,
    AboutWebsite
)


register = template.Library()

def social_network():
    try:
        socia_networks_link=AboutMe.objects.last().social_networks.all()
    except:
        socia_networks_link=None
    return socia_networks_link

@register.inclusion_tag("remix/footer.html")
def footer():
    return{
        'tracks':Track.objects.active().order_by('-published')[:5],
        'socia_networks_link':social_network,
        'website':AboutWebsite.objects.last(),
    }

@register.inclusion_tag("remix/top-menue.html")
def top_menue():
    return{
        'socia_networks_link':social_network,
    }

@register.inclusion_tag("remix/navbar/navbar.html",takes_context=True)
def navbar(context):
    return{
        'track_categories':TrackCategory.objects.active(),
        'artist_categories':ArtistCategory.objects.active(),
        'website':AboutWebsite.objects.last(),
        'about_me':AboutMe.objects.last()
    }

@register.inclusion_tag("remix/sidbar.html",takes_context=True)
def sidbar(context):
    return{
        'static_sidbars':HomePage.objects.filter(status=True)[:2],
        'dynamic_sidbars':Sidebar.objects.filter(status=True)[:4],
    }

@register.simple_tag
def call_method(category_obj,filter):
    try:
        method=getattr(category_obj, 'find_tracks')
        return method(filter)
    except AttributeError:
        return None

