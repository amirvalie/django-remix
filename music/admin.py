from django.contrib import admin
from .models import (
    Category,
    Artist,
    IpAddress,
    Track,
    TrackFile,
    Banner,
    OriginalLinkTrack,
    SocialNetwork,
    ComingSoon,
)

class TrackFileAdmin(admin.TabularInline):
    model=TrackFile
    extra=1
class OriginalLinkTrackAdmin(admin.TabularInline):
    model=OriginalLinkTrack
    extra=1
class TrackAdmin(admin.ModelAdmin):
    list_display=['title','category','best_song','status','jpublish',]
    inlines=[TrackFileAdmin,OriginalLinkTrackAdmin]
    
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','parent','status',]
    search_fields=['title']

class ArtistAdmin(admin.ModelAdmin):
    list_display=['picture_tag','name']
class BannerAdmin(admin.ModelAdmin):
    pass

class SocialNetworkAdmin(admin.ModelAdmin):
    pass

class ComingSoonAdmin(admin.ModelAdmin):
    pass

admin.site.register(Track,TrackAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Artist,ArtistAdmin)
admin.site.register(Banner,BannerAdmin)
admin.site.register(SocialNetwork,SocialNetworkAdmin)
admin.site.register(ComingSoon,ComingSoonAdmin)
