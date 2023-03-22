from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.http import HttpResponseBadRequest
from django.db.models import Q
from itertools import chain
import json
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from category.models import (TrackCategory,)
from artist.models import(Artist,)
from itertools import chain
from django.views.generic import (
    ListView,
    DetailView,
)
from .models import (
    Track,
)
from site_control.models import (
    HomePage,
    Banner,
)
now=timezone.now()

class Home(ListView):
    queryset=HomePage.objects.filter(status=True)[:5]
    template_name='remix/music/home.html'
    context_object_name='contents'
    
    @staticmethod
    def best_tracks_url(tracks:list):
        tracks_url=[]
        for track in tracks:
            tracks_url.append(track.track_files.first().track_file.url)
        return json.dumps(tracks_url)

    @staticmethod
    def best_tracks_artist(tracks:list):
        artists=[]
        for track in tracks:
            try:
                artists.append(track.artists.first().name)
            except:
                artists.append('unknown')
        return json.dumps(artists)

    @staticmethod
    def best_tracks_name(tracks:list):
        songs_name=[]
        for track in tracks:
            songs_name.append(track.finglish_title)
        return json.dumps(songs_name)

    @staticmethod
    def best_tracks_number(tracks:list):
        songs_number=[]
        for i in range(1,tracks.count()+1):
            songs_number.append(f'_{i}')
        return json.dumps(songs_number)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['best_tracks']=Track.objects.best_tracks()[:20]
        context['best_tracks_url']=Home.best_tracks_url(context['best_tracks'])
        context['best_tracks_artist']=Home.best_tracks_artist(context['best_tracks'])
        context['best_tracks_name']=Home.best_tracks_name(context['best_tracks'])
        context['best_tracks_number']=Home.best_tracks_number(context['best_tracks'])
        context['artists']=Artist.objects.active()[:12]
        context['banners']=Banner.objects.filter(status=True,track__status=True).order_by('-id')
        return context        

class DetailTrack(DetailView):
    template_name='remix/music/detail-track.html'
    context_object_name='track'
    
    def get_object(self):
        slug=self.kwargs.get('slug')
        track=get_object_or_404(Track.objects.active(),slug=slug)
        return track

    def get_context_data(self,**kwargs):
        ip_address = self.request.user.ip_address
        if ip_address not in self.object.hits.all():
            self.object.hits.add(ip_address)
        context=super().get_context_data(**kwargs)
        context['related_tracks']=Track.objects.active().filter(
            Q(category=self.get_object().category) | 
            Q(description__icontains=self.get_object().description)
        ).exclude(id=context['track'].id)
        return context

class ListOfTrack(ListView):
    paginate_by = 10
    template_name = 'remix/music/track-list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(TrackCategory.objects.active(), slug=slug)
        return category.tracks_of_category_and_sub_category()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category']=category
        return context

class SearchTrackOrArtist(ListView):
    template_name='remix/music/search-result.html'
    context_object_name='results'
    paginate_by=10

    def get_queryset(self):
        query=self.request.GET.get('q','')
        tracks=Track.objects.active().filter(
            Q(title__icontains=query) | 
            Q(finglish_title__icontains=query) | 
            Q(artists__name__icontains=query)
        ).distinct()    
        artists=Artist.objects.active().filter(
            name__icontains=query
        ).distinct()
        if tracks.exists() and artists.exists():
            result=list(chain(tracks,artists))
            return result
        return artists or tracks    
        
class PreViewDetail(DetailView):
    template_name='remix/music/preview-detail-track.html'
    context_object_name='track'

    @method_decorator(permission_required('is_staff'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        slug=self.kwargs.get('slug')
        track=get_object_or_404(Track,slug=slug)
        return track
