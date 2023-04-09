from django import template
from django.http import request
from django.db.models import Q
from ..models import Track
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
from extentions.utils import jalali_converter

register = template.Library()

@register.inclusion_tag("remix/footer.html",takes_context=True)
def footer(context):

    return{
        'tracks':Track.objects.active().order_by('-published')[:5],
        'website':context.get('website'),
        'about_me':context.get('about_me'),
    }

@register.filter
def convert_to_jalali(time):
    return jalali_converter(time)

@register.inclusion_tag("remix/top-menue.html",takes_context=True)
def top_menue(context):
    return {
        'about_me':context.get('about_me')
    }

@register.inclusion_tag("remix/navbar/navbar.html",takes_context=True)
def navbar(context):
    return{
        'track_categories':TrackCategory.objects.active(),
        'artist_categories':ArtistCategory.objects.active(),
        'website':context.get('website'),
        'about_me':context.get('about_me')
    }

@register.inclusion_tag("remix/site_control/sidbar.html",takes_context=True)
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


@register.simple_tag
def return_class_name(obj):
    return obj.__class__.__name__

@register.simple_tag
def subcategories(obj):
    categories=TrackCategory.objects.active().filter(
        Q(child=obj.category)|
        Q(parent=obj.category)
    ).exclude()
    return categories
