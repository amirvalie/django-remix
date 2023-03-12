from django.db import models
from django.db.models import Count,Q 
from django.core.exceptions import ValidationError
from django.db import models
from music.models import AbstractCommonField,AbstractDateFeild

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class Category(AbstractCommonField,AbstractDateFeild):
    parent=models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='والد',
        blank=True,
        null=True,
        related_name='child',
    )
    title=models.CharField(
        max_length=250,
        verbose_name='عنوان',
    )
    objects=CategoryManager()

    def clean(self):
        if self.parent:
            obj=self.parent
            if obj.parent:
                raise ValidationError({'parent':_('غیر مجاز! این کتگوری خود دارای والد دیگری میباشد.')})
        if self.child.exists() and self.parent:
            raise ValidationError({'parent':_('غیر مجاز! این کتگوری خود دارای فرزند میباشد.')})

    def __str__(self):
        return self.title
    class Meta:
        abstract=True
        verbose_name='دسته بندی'
        verbose_name_plural='دسته بندی ها'

class TrackCategory(Category):
    class Meta:
        verbose_name='دسته بندی موزیک'
        verbose_name_plural='دسته بندی موزیک ها'

    def tracks_of_category_and_sub_category(self):
        sub_categories_id=self.child.active().values_list('id',flat=True)
        if sub_categories_id:
            return Track.objects.active().filter(
                Q(category__id__in=sub_categories_id)|
                Q(category__id=self.id)
            )
        return self.tracks.active()
        
    def most_visited_songs(self):
        return self.tracks_of_category_and_sub_category().annotate(
            count=Count('hits')
        )

    def save(self, *args, **kwargs):
        ##use update manager instead of for loop
        if not self.status:
            for track in self.tracks.active():
                track.status = False
                track.save()
            if self.child.exists():
                for child_category in self.child.active():
                    child_category.status=False
                    child_category.save()
        super(TrackCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("music:tracks_of_category", args=[self.slug])

class ArtistCategory(Category):
    class Meta:
        verbose_name='دسته بندی هنرمند'
        verbose_name_plural='دسته بندی هنرمند ها'
    def artists_of_category_and_sub_category(self):
        sub_categories_id=self.child.active().values_list('id',flat=True)
        if sub_categories_id:
            return Artist.objects.active().filter(
                Q(category__id__in=sub_categories_id)|
                Q(category__id=self.id)
            )
        else:
            return self.artists.active()
            
    def save(self, *args, **kwargs):
        if not self.status:
            for artist in self.artsts.active():
                artist.status = False
                artist.save()
            if self.child.exists():
                for child_category in self.child.active():
                    child_category.status=False
                    child_category.save()
        super(ArtistCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("artist:artists_of_category", args=[self.slug])


class Sidebar(models.Model):
    title=models.CharField(
        max_length=250,
        verbose_name='عنوان'
    )
    category=models.ForeignKey(
        TrackCategory,
        on_delete=models.CASCADE,
        related_name='sidbars',
        verbose_name='دسته بندی',
        help_text='تمام آیتم های مربوط به دسته بندی انتخاب شده بر اساس تعداد بازدید ها در سایت قرار میگیرد.'
    )
    status=models.BooleanField(
        default=True,
        verbose_name='وضعیت',
    )
    class Meta:
        verbose_name='نوار کناری'
        verbose_name_plural='نوارهای کناری'

    def __str__(self):
        return self.title
