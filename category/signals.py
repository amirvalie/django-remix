
from django.db.models.signals import pre_save
from django.dispatch import receiver
from music.models import Track
from django.utils.text import slugify
from .models import (
    TrackCategory,
    ArtistCategory,
)


@receiver(pre_save,sender=Track)
@receiver(pre_save, sender=TrackCategory)
@receiver(pre_save, sender=ArtistCategory)
def generate_slug(sender, instance, **kwargs):
    print(instance.slug)
    if not instance.slug:
        slug = slugify(instance.title,allow_unicode=True)
        num = 1
        while sender.objects.filter(slug=slug).exists():
            slug = slugify(f'{instance.title}-{num}',allow_unicode=True)
            num += 1
        instance.slug = slug