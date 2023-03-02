from django.shortcuts import render,HttpResponse,get_object_or_404
from django.db.models import Q
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
        )
        return context

class CategoryList(ListView):
	paginate_by = 5
	template_name = 'remix/category_list.html'

	def get_queryset(self):
		global category
		slug = self.kwargs.get('slug')
		category = get_object_or_404(Category.objects.active(), slug=slug)
		return category.tracks.active()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['category'] = category
		return context


class ListOfArtist(ListView):
    queryset=Artist.objects.filter(status=True)
    template_name='remix/archive-bio.html'
    context_object_name='artists'

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