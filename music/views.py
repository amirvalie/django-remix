from django.shortcuts import render,HttpResponse,get_object_or_404
from django.db.models import Q
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

def find_ids(category_obj):
    ids=[]
    if category_obj.__class__ in  [TrackCategory,ArtistCategory]:
        if category_obj.child.exists():
            for cat_child in category_obj.child.active(): 
                ids.append(cat_child.id)
    ids.append(category_obj.id)
    return ids

class Index(ListView):
    queryset=Track.objects.remix()
    template_name='remix/home.html'
    context_object_name='tracks'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['podcasts']=Track.objects.podcast()
        context['best_songs']=Track.objects.best_songs()
        context['artists']=Artist.objects.filter(status=True)
        context['banners']=Banner.objects.filter(status=True)
        context['coming_soon']=ComingSoon.objects.filter(status=True)
        return context        

class DetailTrack(DetailView):
    template_name='remix/detail-track.html'
    context_object_name='track'
    
    def get_object(self):
        slug=self.kwargs.get('slug')
        track=get_object_or_404(Track.objects.active(),slug=slug)
        return track

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['related_tracks']=Track.objects.filter(
            Q(category=self.get_object().category) | 
            Q(description__contains=self.get_object().description)
        ).exclude(id=context['track'].id)
        return context

class ListOfTrack(ListView):
    paginate_by = 5
    template_name = 'remix/category-list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        if slug == 'all_remix':
            category = 'ریمیکس ها'
            return Track.objects.remix()
        elif slug == 'all_podcast':
            category='پادکست ها'
            return Track.objects.podcast()
        category = get_object_or_404(TrackCategory.objects.active(), slug=slug)
        ids=find_ids(category)
        return Track.objects.active().filter(category__id__in=ids) 

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
            category='هنرمندان'
            category_id=ArtistCategory.objects.active().values_list('id',flat=True)
            return Artist.objects.filter(status=True).filter(category__id__in=category_id) 
        category = get_object_or_404(ArtistCategory.objects.active(), slug=slug)
        ids=find_ids(category)
        return Artist.objects.filter(status=True).filter(category__id__in=ids) 
        
    def get_context_data(self, **kwargs):
        ip_address = self.request.user.ip_address
        if ip_address not in self.object.hits.all():
            self.object.hits.add(ip_address)

        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context

class DetailArtist(DetailView):
    queryset=Artist.objects.filter(status=True)
    template_name='remix/single-bio.html'
    context_object_name='artist'

class SearchTrackOrArtist(ListView):
    template_name='remix/search_result.html'
    def get_queryset(self):
        query=self.request.GET.get('q',None)
        result=Track.objects.filter(
            Q(title__icontains=query) | 
            Q(artists__name__icontains=query)
        )
        return result