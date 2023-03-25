from django.contrib import admin
from .models import (
    IpAddress,
    Track,
    TrackFile,
    OriginalLinkTrack,
)


def active_objects(modeladmin,request,queryset):
    for obj in queryset:
        obj.status=True
        obj.save()
    
active_objects.short_description='منتشر کردن'

def deactive_objects(modeladmin,request,queryset):
    for obj in queryset:
        obj.status=False
        obj.save()

deactive_objects.short_description='غیرفعال کردن'


class TrackFileAdmin(admin.TabularInline):
    model=TrackFile
    extra=0

class OriginalLinkTrackAdmin(admin.TabularInline):
    model=OriginalLinkTrack
    extra=0

class TrackAdmin(admin.ModelAdmin):
    list_display=['title','status',]
    inlines=[TrackFileAdmin,OriginalLinkTrackAdmin]
    actions=[active_objects,deactive_objects,]
    search_fields=['title','description','artists__name']
    readonly_fields=('preview_url',)
    fieldsets=(
        (None,{
            'fields': (
                'title',
                'finglish_title',
                'slug',
                'category',
                'description',
                'lyrics',
                'cover',
                'artists',
                'published',
                'preview_url',
                'status',
            )
        }),
    )

admin.site.register(Track,TrackAdmin)