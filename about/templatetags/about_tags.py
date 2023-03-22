from django import template 
from ..models import AboutMe
from ..forms import ContactForm

register=template.Library()

@register.inclusion_tag('remix/about/follow_social.html')
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
