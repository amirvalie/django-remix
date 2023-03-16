from django.contrib import admin
from .models import (
    ArtistCategory,
    TrackCategory,
)
from music.admin import active_objects,deactive_objects

# Register your models here.
glob_fieldsets=(
    (None,{
        'fields':(
            'title',
            'slug',
            'parent',
            'status',
        )
    }),
)
class ArtistCategoryAdmin(admin.ModelAdmin):
    list_display=['title','parent','status',]
    search_fields=['title']
    actions=[active_objects,deactive_objects,]
    fieldsets=glob_fieldsets

class TrackCategoryAdmin(admin.ModelAdmin):
    list_display=['title','parent','status',]
    search_fields=['title']
    actions=[active_objects,deactive_objects,]
    fieldsets=glob_fieldsets


admin.site.register(ArtistCategory,ArtistCategoryAdmin)
admin.site.register(TrackCategory,TrackCategoryAdmin)

