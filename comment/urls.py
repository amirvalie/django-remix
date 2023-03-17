from django.urls import path
from . import views

app_name='comment'

urlpatterns=[
    path('post_comment/<str:content_type_id>/<str:object_id>/',views.PostComment.as_view(),name='post_comment'),
]
