from django.shortcuts import render,HttpResponse,redirect
from django.core.mail import send_mail,BadHeaderError
from django.views import View
from django.http import HttpResponse
from .models import(
    AboutMe,
    Contact,
)
from .forms import ContactForm


class About(View):
    def get(self,request,*args,**kwargs):
        if AboutMe.objects.last():
            return render(request,'remix/about/about.html')
        return redirect('music:home')

class Contact(View):
    def post(self,request,*args,**kwargs):
        form=ContactForm(data=request.POST or None)
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
        return redirect('about:posted_failure')

class PostedSuccessfully(View):
    def get(self,request,*args,**kwargs):
        return render(request,'remix/site_control/posted-successfully.html')

class PostedByFailure(View):
    def get(self,request,*args,**kwargs):
        return render(request,'remix/site_control/posted-by-failure.html')
