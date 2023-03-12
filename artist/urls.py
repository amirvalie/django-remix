from django.urls import path
from . import views

app_name='artist'

urlpatterns=[
    path('category/artists/<slug:slug>/',views.ListOfArtist.as_view(),name='artists_of_category'),
    path('single-bio/<slug:slug>/',views.DetailArtist.as_view(),name='single-bio'),
]
