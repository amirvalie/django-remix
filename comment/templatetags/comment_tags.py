from django import template
from django.http import request
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.db.models import Count
from ..models import (
    Comment,
)
from site_control.models import (ModelWithComment,)

register=template.Library()

@register.inclusion_tag('remix/comment/comment.html', takes_context=True)
def comment(context,obj):
    try:
        success_massage=context['request'].session.pop('success_massage')
    except:
        success_massage=None

    return{
        'object':obj,
        'comments':obj.comments.active(),
        'success_massage':success_massage,
    }

@register.filter
def comments_count(obj):
    return obj.comments.active().count() + obj.comments.aggregate(count=Count('replies'))['count']

@register.simple_tag()
def model_with_comment_exist(obj):
    try:
        content_type=ContentType.objects.get_for_model(obj)
        return ModelWithComment.objects.filter(content_type=content_type).exists()
    except:
        return False
    
@register.simple_tag
def comment_target(obj):
    return reverse('comment:post_comment',args=(
        ContentType.objects.get_for_model(obj).id,
        obj.id,
    ))
