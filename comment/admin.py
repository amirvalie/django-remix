from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from .models import (
    Reply,
    Comment,
    ModelWithComment,
)

class ReplyInline(admin.StackedInline):
    model=Reply
    extra=0

class CommentAdmin(admin.ModelAdmin):
    inlines=(ReplyInline,)

class ModelWithCommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comment,CommentAdmin)
admin.site.register(ModelWithComment,ModelWithCommentAdmin)




