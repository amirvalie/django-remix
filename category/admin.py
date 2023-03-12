from django.contrib import admin
from .models import (
    ArtistCategory,
    TrackCategory,
    Sidebar,

)
from music.admin import active_objects,deactive_objects

# Register your models here.

class ArtistCategoryAdmin(admin.ModelAdmin):
    list_display=['title','parent','status',]
    search_fields=['title']
    actions=[active_objects,deactive_objects,]

class TrackCategoryAdmin(admin.ModelAdmin):
    list_display=['title','parent','status',]
    search_fields=['title']
    actions=[active_objects,deactive_objects,]


class SidbarAdmin(admin.ModelAdmin):
    actions=[active_objects,deactive_objects,]


admin.site.register(ArtistCategory,ArtistCategoryAdmin)
admin.site.register(TrackCategory,TrackCategoryAdmin)
admin.site.register(Sidebar,SidbarAdmin)
