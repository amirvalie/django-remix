from django.urls import path
from . import views

app_name='music'

urlpatterns=[
    path('index/',views.Index.as_view(),name='index'),
    path('track/<slug:slug>/',views.DetailTrack.as_view(),name='detail_track'),
    path('index',views.AllPublicTrackOfCategory.as_view(),name='index'),
    path('index',views.ListOfArtist.as_view(),name='index'),
    path('index',views.DetailArtist.as_view(),name='index'),
]