from django.urls import path
from . import views

app_name='music'

urlpatterns=[
    path('',views.Home.as_view(),name='home'),
    path('track/<slug:slug>/',views.DetailTrack.as_view(),name='track_detail'),
    path('category/tracks/<slug:slug>/',views.ListOfTrack.as_view(),name='tracks_of_category'),
    path('search-result/',views.SearchTrackOrArtist.as_view(),name='search'),
]