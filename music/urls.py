from django.urls import path
from . import views

app_name='music'

urlpatterns=[
    path('index/',views.Index.as_view(),name='index'),
    path('track/<slug:slug>/',views.DetailTrack.as_view(),name='detail_track'),
    path('category/<slug:slug>/tracks/',views.AllPublicTrackOfCategory.as_view(),name='tracks_of_category'),
    path('artists/',views.ListOfArtist.as_view(),name='artists'),
    path('artist/<slug:slug>/',views.DetailArtist.as_view(),name='artist'),
    path('search-result/',views.SearchTrackOrArtist.as_view(),name='search'),
]