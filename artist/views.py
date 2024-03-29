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
    template_name='remix/artist/artist-list.html'
    context_object_name='artists'
    paginate_by=10
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug == 'all_artists':
            return Artist.objects.active()
        category = get_object_or_404(ArtistCategory.objects.active(), slug=slug)
        return category.artists_of_category_and_sub_category()


class DetailArtist(DetailView):
    queryset=Artist.objects.active()
    template_name='remix/artist/artist-detail.html'
    context_object_name='artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_tracks'] = self.get_object().tracks.active()
        return context
