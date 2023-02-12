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
    inlines=[TrackFileAdmin,OriginalLinkTrackAdmin]
    

class CategoryAdmin(admin.ModelAdmin):
    pass

class ArtistAdmin(admin.ModelAdmin):
    pass

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
