from django.shortcuts import render,HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
)
from .models import (
    Artist,
    Track,
    Category,
    Banner,
    ComingSoon,
)
# Create your views here.

class Home(ListView):
    model=Track.objects.remix()
    template_name='templates/music/index.html'
    context_object_name='track'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['podcast']=Track.objects.podcast()
        context['best_songs']=Track.objects.best_songs()
        context['atists']=Artist.objects.all()