from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from artist.models import (SocialNetwork,)
from .models import (
    AboutMe,
    Contact,
)
# Register your models here.

class SocialNetworkAdmin(GenericTabularInline):
    model=SocialNetwork
    extra=1

class AboutMeAdmin(admin.ModelAdmin):
    inlines=[SocialNetworkAdmin,]

class ContactAdmin(admin.ModelAdmin):
    pass


admin.site.register(AboutMe,AboutMeAdmin)
admin.site.register(Contact,ContactAdmin)