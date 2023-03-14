from django.shortcuts import render,HttpResponse
from django.core.mail import send_mail,BadHeaderError
from django.shortcuts import render
from django.views import View
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
        queryset=AboutMe.objects.last()
        return render(request,'remix/about.html',{'owner':AboutMe.objects.last()})

class Contact(FormView):
    template_name='about/contanct.html'
    form_class=ContactForm  
    
    def form_valid(self, form):
        # title=form.data['title']
        # body={
        #     'name':form.cleaned_data['name'],
        #     'last_name':form.cleaned_data['last_name'],
        #     'email':form.cleaned_data['email'],
        #     'description':form.cleaned_data['description'],
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
        return super().form_valid(form)