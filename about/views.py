from django.shortcuts import render,HttpResponse,redirect
from django.core.mail import send_mail,BadHeaderError
from django.views import View
from django.http import HttpResponse,HttpResponseNotFound

from django.views.generic import (
    FormView,
)
from .models import(
    AboutMe,
    Contact,
)
from .forms import ContactForm


class About(View):
    def get(self,request,*args,**kwargs):
        if AboutMe.objects.last():
            return render(request,'remix/about.html',{'owner':AboutMe.objects.last()})
        return HttpResponse('<h1>Page not found</h1>')

class Contact(View):
    def post(self,request,*args,**kwargs):
        form=ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            # body={
            #     'username':form.cleaned_data['username'],
            #     'email':form.cleaned_data['email'],
            #     'content':form.cleaned_data['content'],
            # }
            # massage="\n".join(body.values())
            # try:
            #     send_email(
            #         form.data['title'],
            #         massage,
            #         'admin@gmail.com'
            #         ['admin@gmail.com']
            #     )
            # except BadHeaderError:
            #     return HttpResponse('عنوان نامعتبر')
            return redirect('comment:posted_successfully')
