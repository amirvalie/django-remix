from django.shortcuts import render,HttpResponse,redirect
from django.core.mail import send_mail,BadHeaderError
from django.views import View
from django.http import HttpResponse,HttpResponseNotFound
from django.views.generic.edit import BaseFormView
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
            # email_subject = f'یک پیام جدید از طرف {form.cleaned_data["username"]}'
            # try:
            #     send_email(
            #         email_subject, 
            #         massage,
            #         settings.CONTACT_EMAIL
            #         ['admin@gmail.com']
            #     )
            # except BadHeaderError:
            #     return HttpResponse('عنوان نامعتبر')
            return redirect('about:posted_successfully')

class PostedSuccessfully(View):
    def get(self,request,*args,**kwargs):
        return render(request,'remix/posted-successfully.html')