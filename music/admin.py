from django.contrib import admin
from .models import (
    ArtistCategory,
    TrackCategory,
    Artist,
    IpAddress,
    Track,
    TrackFile,
    Banner,
    OriginalLinkTrack,
    SocialNetwork,
    ComingSoon,
    Sidebar,
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
class ArtistCategoryAdmin(admin.ModelAdmin):
    list_display=['title','parent','status',]
    search_fields=['title']
    actions=[active_objects,deactive_objects,]
class TrackCategoryAdmin(admin.ModelAdmin):
    list_display=['title','parent','status',]
    search_fields=['title']
    actions=[active_objects,deactive_objects,]
class ArtistAdmin(admin.ModelAdmin):
    list_display=['picture_tag','name']
    actions=[active_objects,deactive_objects,]
class BannerAdmin(admin.ModelAdmin):
    actions=[active_objects,deactive_objects,]
class SidbarAdmin(admin.ModelAdmin):
    actions=[active_objects,deactive_objects,]

class SocialNetworkAdmin(admin.ModelAdmin):
    pass

class ComingSoonAdmin(admin.ModelAdmin):
    actions=['active_objects','deactive_objects',]


admin.site.register(ArtistCategory,ArtistCategoryAdmin)
admin.site.register(TrackCategory,TrackCategoryAdmin)
admin.site.register(Track,TrackAdmin)
admin.site.register(Artist,ArtistAdmin)
admin.site.register(Banner,BannerAdmin)
admin.site.register(SocialNetwork,SocialNetworkAdmin)
admin.site.register(ComingSoon,ComingSoonAdmin)
admin.site.register(Sidebar,SidbarAdmin)
