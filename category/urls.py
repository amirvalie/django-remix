from django.urls import path
from . import views

app_name='artist'

urlpatterns=[
    # path('category/tracks/<slug:slug>/',views.ListOfTrack.as_view(),name='tracks_of_category'),
    # path('category/artists/<slug:slug>/',views.ListOfArtist.as_view(),name='artists_of_category'),
]
