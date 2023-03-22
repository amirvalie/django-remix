from django.contrib import admin
from music.admin import active_objects,deactive_objects
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import (
    Artist,
    SocialNetwork,
)

# Register your models here.
class SocialNetworkAdmin(GenericTabularInline):
    model=SocialNetwork
    extra=1

class ArtistAdmin(admin.ModelAdmin):
    list_display=['picture_tag','name','status']
    inlines=[SocialNetworkAdmin,]
    actions=[active_objects,deactive_objects,]
    fieldsets=(
        (None,{
            'fields':(
                'name',
                'slug',
                'category',
                'decription',
                'cover',
                'status',
            )
        }
        ),
    )


admin.site.register(Artist,ArtistAdmin)
