from django.shortcuts import render,HttpResponse,get_object_or_404
from django.db.models import Q
from itertools import chain
import json
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from category.models import (TrackCategory,)
from artist.models import(Artist,)

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
    template_name='remix/home.html'
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
        context['banners']=Banner.objects.filter(status=True,track__status=True)
        print('best_tracks_url',context['best_tracks_url'])
        print('best_tracks_artist',context['best_tracks_artist'])
        print('best_tracks_name',context['best_tracks_name'])
        print('best_tracks_numberc',context['best_tracks_number'])
        return context        

class DetailTrack(DetailView):
    template_name='remix/detail-track.html'
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
    template_name = 'remix/track-list.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        category = get_object_or_404(TrackCategory.objects.active(), slug=slug)
        return category.tracks_of_category_and_sub_category()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SearchTrackOrArtist(ListView):
    template_name='remix/search-result.html'
    context_object_name='tracks'
    def get_queryset(self):
        query=self.request.GET.get('q',None)
        tracks=Track.objects.active().filter(
            Q(title__icontains=query) | 
            Q(finglish_title__icontains=query) | 
            Q(artists__name__icontains=query)
        ).distinct()
        return tracks
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        query=self.request.GET.get('q',None)
        context['artists']=Artist.objects.active().filter(
            name__icontains=query
        ).distinct()
        print(context['artists'])
        print(context['tracks'])
        return context

class PreViewDetail(DetailView):
    template_name='remix/preview-detail-track.html'
    context_object_name='track'

    @method_decorator(permission_required('is_staff'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        slug=self.kwargs.get('slug')
        track=get_object_or_404(Track,slug=slug)
        return track
