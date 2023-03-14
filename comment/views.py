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
        print(kwargs)
        form=CommentForm(request.POST)
        if form.is_valid:
            content_type=get_object_or_404(
                ContentType,
                id=kwargs.get('content_type_id')
            )
            obj=form.save(commit=False)
            obj.content_type=content_type
            obj.object_id=kwargs.get('object_id')
            obj.save()
        return redirect('comment:posted_successfully')

class Postedsuccessfully(View):
    template_name='remix/posted-successfully.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)


