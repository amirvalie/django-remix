from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from artist.models import (SocialNetwork,)
from .models import (
    AboutMe,
    Contact,
    AboutWebsite,
)
# Register your models here.

class SocialNetworkAdmin(GenericTabularInline):
    model=SocialNetwork
    extra=1

class AboutMeAdmin(admin.ModelAdmin):
    inlines=[SocialNetworkAdmin,]
    list_display=['name']

class ContactAdmin(admin.ModelAdmin):
    list_display=['title','username','email']

class AboutWebsiteAdmin(admin.ModelAdmin):
    pass

admin.site.register(AboutMe,AboutMeAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(AboutWebsite,AboutWebsiteAdmin)