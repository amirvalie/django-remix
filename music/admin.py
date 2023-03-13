from django.contrib import admin
from .models import (
    IpAddress,
    Track,
    TrackFile,
    OriginalLinkTrack,
)
def active_objects(modeladmin,request,queryset):
    queryset.update(
        status=True,
    )
active_objects.short_description='منتشر کردن'

def deactive_objects(modeladmin,request,queryset):
    print(queryset)
    queryset.update(
        status=False,
    )
deactive_objects.short_description='غیرفعال کردن'

class TrackFileAdmin(admin.TabularInline):
    model=TrackFile
    extra=1
class OriginalLinkTrackAdmin(admin.TabularInline):
    model=OriginalLinkTrack
    extra=1


class TrackAdmin(admin.ModelAdmin):
    list_display=['title','best_song','status','jpublish',]
    inlines=[TrackFileAdmin,OriginalLinkTrackAdmin]
    actions=[active_objects,deactive_objects,]
    



admin.site.register(Track,TrackAdmin)