from django.shortcuts import render,HttpResponse,get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
)
from .models import (
    Artist
)
from category.models import (
    ArtistCategory
)

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
