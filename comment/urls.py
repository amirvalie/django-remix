from django.urls import path
from . import views

app_name='comment'

urlpatterns=[
    path('post_comment/',views.PostComment.as_view(),name='post_comment'),
]
