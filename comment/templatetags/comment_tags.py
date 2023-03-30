from django import template
from django.http import request
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.db.models import Count
from ..forms import CommentForm
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
    context['request'].session['content_type_id']=ContentType.objects.get_for_model(obj).id
    context['request'].session['object_id']=obj.id
    return{
        'object':obj,
        'comments':obj.comments.active().order_by('-created'),
        'success_massage':success_massage,
        'form':CommentForm()
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
    