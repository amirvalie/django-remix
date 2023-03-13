from django.urls import path
from . import views

app_name='comment'

urlpatterns=[
    path('post_comment/<str:content_type>/<str:object_id>/',views.PostComment.as_view(),name='post_comment'),
    path('posted-successfully/',views.Postedsuccessfully.as_view(),name='posted_successfully')
]
