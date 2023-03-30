from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import Comment

class CommentForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=50, required=True)
    content=forms.Textarea(attrs={'row':5,'cols':20})

    def __init__(self,obj_id=None,content_type_id=None,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.obj_id=obj_id
        self.content_type_id=content_type_id
        self.fields['email'].widget.attrs['class']='username'
        self.fields['username'].widget.attrs['class']='username'
        self.fields['content'].widget.attrs['class']='con'

    class Meta:
        model = Comment
        fields=['email','username','content']
    
    def save(self,commit=True):
        comment = super().save(commit=False)
        comment.content_type=ContentType.objects.get(id=self.content_type_id)
        comment.object_id=self.obj_id
        comment.save()
        return comment

        