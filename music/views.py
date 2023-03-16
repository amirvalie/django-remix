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
    def return_songs_url(tracks:list):
        tracks_url=[]
        for track in tracks:
            tracks_url.append(track.track_files.first().track_file.url)
        return json.dumps(tracks_url)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['best_tracks']=Track.objects.best_tracks()
        context['best_tracks_urls']=Home.return_songs_url(context['best_tracks'])
        context['artists']=Artist.objects.active()[:12]
        context['banners']=Banner.objects.filter(status=True)
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
        context['related_tracks']=Track.objects.filter(
            Q(category=self.get_object().category) | 
            Q(description__icontains=self.get_object().description)
        ).exclude(id=context['track'].id)
        return context

class ListOfTrack(ListView):
    paginate_by = 15
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
            Q(artists__name__icontains=query)
        )
        return tracks
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        query=self.request.GET.get('q',None)
        context['artists']=Artist.objects.active().filter(
            name__icontains=query
        )
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
