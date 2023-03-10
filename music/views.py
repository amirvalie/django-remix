from django.shortcuts import render,HttpResponse,get_object_or_404
from django.db.models import Q
from itertools import chain
from django.views.generic import (
    ListView,
    DetailView,
)
from .models import (
    Artist,
    Track,
    ArtistCategory,
    TrackCategory,
    Banner,
    ComingSoon,
)
from django.utils import timezone
now=timezone.now()

class Home(ListView):
    queryset=Track.objects.remix()
    template_name='remix/home.html'
    context_object_name='remixes'
    
    @staticmethod
    def return_songs_url(tracks:list):
        tracks_url=[]
        for track in tracks:
            tracks_url.append(track.track_files.first().track_file.url)
        return tracks_url

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['podcasts']=Track.objects.podcast()[:20]
        context['best_tracks']=Track.objects.best_tracks()[:20]
        context['best_tracks_urls']=Home.return_songs_url(context['best_tracks'])
        context['artists']=Artist.objects.active()[:6]
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
    paginate_by = 5
    template_name = 'remix/category-list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        if slug == 'all_remix':
            return Track.objects.remix()
        elif slug == 'all_podcast':
            return Track.objects.podcast()
        category = get_object_or_404(TrackCategory.objects.active(), slug=slug)
        return category.tracks_of_category_and_sub_category()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class ListOfArtist(ListView):
    template_name='remix/archive-bio.html'
    context_object_name='artists'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        if slug == 'all_artists':
            category_id=ArtistCategory.objects.active().values_list('id',flat=True)
            return Artist.objects.filter(status=True).filter(category__id__in=category_id) 
        category = get_object_or_404(ArtistCategory.objects.active(), slug=slug)
        return category.artists_of_category_and_sub_category()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context

class DetailArtist(DetailView):
    queryset=Artist.objects.active()
    template_name='remix/single-bio.html'
    context_object_name='artist'

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
        return context
