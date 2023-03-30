from django.shortcuts import redirect
from django.views import View
from .forms import CommentForm


class PostComment(View):
    def post(self,request,*args,**kwargs):
        obj_id=request.session.pop('object_id')
        content_type_id=request.session.pop('content_type_id')
        form=CommentForm(data=request.POST,obj_id=obj_id,content_type_id=content_type_id)
        if form.is_valid:
            comment=form.save()
            get_object=comment.content_type.get_object_for_this_type(
                pk=comment.object_id
            )
            request.session['success_massage']='ارسال پیام موفقیت آمیز بود'
            return redirect(get_object.get_absolute_url())
        else:
            return redirect('about:posted_failure')

