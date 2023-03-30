from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import Comment

class CommentForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=50, required=True)
    content=forms.Textarea(attrs={'row':5,'cols':20})
    class Meta:
        model = Comment
        fields=['email','username','content']