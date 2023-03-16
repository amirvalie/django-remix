from django.urls import re_path
from . import views

app_name='artist'

urlpatterns=[
    re_path(r'^category/artists/(?P<slug>[-\w]+)/$',views.ListOfArtist.as_view(),name='artists_of_category'),
    re_path(r'^artist/(?P<slug>[-\w]+)/$',views.DetailArtist.as_view(),name='artist_detail'),
]
