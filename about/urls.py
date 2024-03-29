from django.urls import path
from . import views

app_name='about'

urlpatterns=[
    path('about-me/',views.About.as_view(),name='about_me'),
    path('contact/',views.Contact.as_view(),name='contact_me'),
    path('posted-sucessfully/',views.PostedSuccessfully.as_view(),name='posted_successfully'),
    path('posted-failure/',views.PostedByFailure.as_view(),name='posted_failure')
]