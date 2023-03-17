from django.contrib import admin
from .models import (
    Banner,
    ModelWithComment,
    Sidebar,
    HomePage,

)
from music.admin import (
    active_objects,
    deactive_objects,
)
# Register your models here.


class BannerAdmin(admin.ModelAdmin):
    list_display=['caption','status']
    actions=[active_objects,deactive_objects,]


class ModelWithCommentAdmin(admin.ModelAdmin):
    pass

class SidbarAdmin(admin.ModelAdmin):
    list_display=['title','status']
    actions=[active_objects,deactive_objects,]

class HomePageAdmin(admin.ModelAdmin):
    actions=[active_objects,deactive_objects,]
    list_display=['category','status']

    
admin.site.register(ModelWithComment,ModelWithCommentAdmin)
admin.site.register(Banner,BannerAdmin)
admin.site.register(Sidebar,SidbarAdmin)
admin.site.register(HomePage,HomePageAdmin)