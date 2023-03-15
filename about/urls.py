from django.urls import path
from . import views

app_name='about'

urlpatterns=[
    path('about-me/',views.About.as_view(),name='about-me'),
    path('contact/',views.Contact.as_view(),name='contact_me'),
]