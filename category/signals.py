
from django.db.models.signals import pre_save
from django.dispatch import receiver
from music.models import Track
from artist.models import Artist
from django.utils.text import slugify
from .models import (
    TrackCategory,
    ArtistCategory,
)




@receiver(pre_save,sender=Artist)
@receiver(pre_save,sender=Track)
@receiver(pre_save, sender=TrackCategory)
@receiver(pre_save, sender=ArtistCategory)
def generate_slug(sender, instance, **kwargs):
    if not instance.slug:
        if sender == Artist:
            slug = slugify(instance.name,allow_unicode=True)
        else:
            slug = slugify(instance.title,allow_unicode=True)
        num = 1
        while sender.objects.filter(slug=slug).exists():
            if sender == Artist:
                slug = slugify(f'{instance.name}-{num}',allow_unicode=True)
            else:
                slug = slugify(f'{instance.title}-{num}',allow_unicode=True)
            num += 1
        instance.slug = slug