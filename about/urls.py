from django.urls import path
from . import views

urlpatterns=[
    path('about/',views.About.as_view(),name='about'),
    path('contact/',views.Contact.as_view(),name='contact'),
]