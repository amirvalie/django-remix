from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from .models import (
    Reply,
    Comment,
)
from music.admin import(
    deactive_objects,
    active_objects,
)

class ReplyInline(admin.StackedInline):
    model=Reply
    extra=0

class CommentAdmin(admin.ModelAdmin):
    inlines=(ReplyInline,)
    actions=(deactive_objects,active_objects,)
    
admin.site.register(Comment,CommentAdmin)


