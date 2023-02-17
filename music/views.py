from django.shortcuts import render,HttpResponse
# from django.db import Q
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

class Index(ListView):
    queryset=Track.objects.remix()
    template_name='music/index.html'
    context_object_name='tracks'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['podcasts']=Track.objects.podcast()
        context['best_songs']=Track.objects.best_songs()
        context['atists']=Artist.objects.filter(status=True)
        context['banners']=Banner.objects.filter(status=True)
        context['coming_soon']=ComingSoon.objects.filter(status=True)
        return context        

class DetailTrack(DetailView):
    model=Track
    template_name='music/track_detail.html'
    context_object_name='track'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['related_tracks']=Track.objects.filter(
            Q(category=self.get_object().category) | 
            Q(description__contains=self.get_object().description)
        )
        return context

class AllPublicTrackOfCategory(DetailView):
    queryset=Category.objects.filter(status=True)
    template_name='music/category_tracks.html'
    context_object_name='tracks'
    def get_context_data(self,**kwargs):
        context=super().get_context_data()
        category=self.get_object()
        context['tracks']=category.tracks.active()
        return context
        
class ListOfArtist(ListView):
    queryset=Artist.objects.filter(status=True)
    template_name='music/list_of_artists.html'
    context_object_name='artists'

class DetailArtist(DetailView):
    queryset=Artist.objects.filter(status=True)
    template_name='music/detail_artist.html'
    context_object_name='artist'
