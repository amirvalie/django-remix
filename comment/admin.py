from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from .models import (
    Reply,
    Comment,
)

class ReplyInline(admin.StackedInline):
    model=Reply
    extra=0

class CommentAdmin(admin.ModelAdmin):
    inlines=(ReplyInline,)


admin.site.register(Comment,CommentAdmin)


