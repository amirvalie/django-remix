from django import template
from django.http import request
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from comment.forms import CommentForm
from ..models import (
    Comment,
)
from site_control.models import (ModelWithComment,)

register=template.Library()

@register.inclusion_tag('remix/comment.html')
def comment(obj):
    return{
        'object':obj,
        'comments':obj.comments.active(),
        'form':CommentForm
    }

@register.filter
def comments_count(obj):
    return obj.comments.active().count()

@register.simple_tag()
def model_with_comment_exist(obj):
    content_type=ContentType.objects.get_for_model(obj.__class__)
    return(
        ModelWithComment.objects.filter(content_type=content_type).exists()
    )

@register.simple_tag
def comment_target(obj):
    return reverse('comment:post_comment',args=(ContentType.objects.get_for_model(obj).id,obj.id))
