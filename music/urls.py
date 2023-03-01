from django.urls import path
from . import views

app_name='music'

urlpatterns=[
    path('',views.Index.as_view(),name='index'),
    path('track/<slug:slug>/',views.DetailTrack.as_view(),name='track_detail'),
    path('category/<slug:slug>/tracks/',views.AllPublicTrackOfCategory.as_view(),name='tracks_of_category'),
    path('artists/',views.ListOfArtist.as_view(),name='artists'),
    path('artist/<slug:slug>/',views.DetailArtist.as_view(),name='artist'),
    path('search-result/',views.SearchTrackOrArtist.as_view(),name='search'),
]