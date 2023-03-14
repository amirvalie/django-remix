from django import template 
from ..models import AboutMe

register=template.Library()

@register.inclusion_tag('remix/follow_social.html')
def follow_socials():
    try:
        links=AboutMe.objects.last().social_networks.filter(
        social_network_name__in=['instagram','telegram']
        )
    except:
        links=None
    return {
        'links':links
    }

