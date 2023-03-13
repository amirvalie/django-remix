from django.shortcuts import render,reverse,get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.views import View
from .forms import CommentForm
from django.views.generic import (
    CreateView
)

class PostComment(CreateView):
    form_class=CommentForm
    content_object=None

    def post(self,request,*args,**kwargs):
        content_type=get_object_or_404(ContentType,self.kwargs.get('content_type_id'))
        self.content_object = content_type.get_object_for_this_type(pk=self.kwargs.get("object_id"))
        return super().post(request,*args,**kwargs)

    def get_form_kwargs(self):
        kwargs=self.get_form_kwargs()
        kwargs.update({
            'obj':self.content_object
        })
        return kwargs

class Postedsuccessfully(View):
    template_name='remix/posted-successfully.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)


