from django.urls import path,re_path
from . import views

app_name='music'

urlpatterns=[
    path('',views.Home.as_view(),name='home'),
    re_path(r'^category/tracks/(?P<slug>[-\w]+)/$',views.ListOfTrack.as_view(),name='tracks_of_category'),
    re_path(r'^track/(?P<slug>[-\w]+)/$',views.DetailTrack.as_view(),name='track_detail'),
    re_path(r'^preview/track/(?P<slug>[-\w]+)/$',views.PreViewDetail.as_view(),name='preview_detail'),
    path('search-result/',views.SearchTrackOrArtist.as_view(),name='search'),
]

