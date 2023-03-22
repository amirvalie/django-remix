from django.shortcuts import render,reverse,get_object_or_404,redirect
from django.contrib.contenttypes.models import ContentType
from django.views import View
from django.urls import reverse_lazy
from .forms import CommentForm
from django.views.generic.edit import (
    BaseCreateView
)

class PostComment(View):
    def post(self,request,*args,**kwargs):
        form=CommentForm(request.POST)
        if form.is_valid:
            content_type=get_object_or_404(
                ContentType,
                id=kwargs.get('content_type_id')
            )
            model_class=content_type.model_class()
            get_object=get_object_or_404(model_class,id=kwargs.get('object_id'))
            obj=form.save(commit=False)
            obj.content_type=content_type
            obj.object_id=kwargs.get('object_id')
            obj.save()
            request.session['success_massage']='ارسال پیام موفقیت آمیز بود'
            return redirect(get_object.get_absolute_url())
        else:
            return redirect('about:posted_failure')

