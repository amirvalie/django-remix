
from django.db import models
from django.db.models import Count,Avg
from django.utils.translation import gettext_lazy as _
from extentions.utils import jalali_converter
from django.utils import timezone
from ckeditor.fields import RichTextField 
from django.utils.html import format_html
from django.urls import reverse
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.contrib.contenttypes.fields import GenericRelation

now=timezone.now()

class AbstractDateFeild(models.Model):
    created=models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان ساخت'
    )
    updated=models.DateTimeField(
        auto_now=True,
        verbose_name='زمان اپدیت',
    )
    class Meta:
        abstract=True

class AbstractCommonField(models.Model):
    status=models.BooleanField(
        default=True,
        verbose_name='منتشر شود؟',
    )
    slug=models.SlugField(
        max_length=250,
        unique=True,
        verbose_name='لینک',
        allow_unicode=True,
    )
    class Meta:
        abstract=True


class TrackManager(models.Manager):
    def active(self):
        return self.filter(
            status=True,
        )
    def number_of_hits(self):
        return self.active().annotate(
                count=Count('hits')
            )
    def best_tracks(self):
        songs=[]
        number_of_hits=self.number_of_hits()
        for song in number_of_hits:
            if song.track_files.exists():
                songs.append(song)
        return songs

class IpAddress(AbstractDateFeild):
	ip_address = models.GenericIPAddressField(verbose_name='آدرس')
	def __str__(self):
		return self.ip_address
	class Meta:
		verbose_name = "آی‌پی"
		verbose_name_plural = "آی‌پی ها"
		# ordering = ['pub_date']


class Track(AbstractCommonField,AbstractDateFeild):
    title=models.CharField(
        max_length=250,
        verbose_name='عنوان',
    )
    finglish_title=models.CharField(
        max_length=250,
        verbose_name='عنوان فینگلیشی',
    )
    category=models.ForeignKey(
        'category.TrackCategory',
        on_delete=models.PROTECT,
        related_name='tracks',
        verbose_name='دسته بندی',
    )
    description=RichTextField(
        verbose_name='توضحیات'
    )
    cover=models.ImageField(
        upload_to='images/tracks/covers',
        verbose_name='کاور آهنگ',
        help_text='توجه داشته باشید ابعاد عکس باید 480 * 480 باشد',
    )
    thumbnail = models.ImageField(
        upload_to='images/tracks/thumbnails/',
        null=True,
        blank=True,
    )
    small = models.ImageField(
        upload_to='images/tracks/smalls/',
        null=True,
        blank=True,
    )
    artists=models.ManyToManyField(
        'artist.Artist',
        blank=True,
        related_name='tracks',
        verbose_name='هنرمندان',
    )
    best_song=models.BooleanField(
        default=True,
        verbose_name='آهنگ منتخب؟',
        help_text='اگر میخواهید این اهنگ در قسمت بهترین آهنگ ها قرار گیرد تیک این قسمت را بزنید.'
    )
    hits=models.ManyToManyField(
        IpAddress,
        editable=False,
    )
    published=models.DateTimeField(
        default=timezone.now,
        verbose_name='زمان انتشار',
    )
    comments=GenericRelation('comment.Comment')
    
    def get_absolute_url(self):
        return reverse("music:track_detail", args=[self.slug])

    def jpublish(self):
        return jalali_converter(self.published)
    jpublish.short_description = "زمان انتشار"

    def listen_online(self):
        online=self.track_files.filter(listen_online=True)
        if online:
            return online.first()
        return online

    def preview_url(self):
        return format_html(
            "<a href='{}' target='blank'>پیش‌نمایش</a>".format(reverse("track:preview-detail",
             kwargs={'slug': self.slug}))
        )
        
    def save(self, *args, **kwargs):
        if not self.status:
            self.banners.update(status=False)
        if self.cover:
            img = Image.open(self.cover)
            # Create thumbnail
            thumb_size = (272, 272)
            thumb_img = img.copy()
            thumb_img.thumbnail(thumb_size)
            thumb_bytes = BytesIO() 
            thumb_img.save(thumb_bytes, format='JPEG')
            thumb_file = ContentFile(thumb_bytes.getvalue())
            self.thumbnail.save(f'{self.cover.name.split("/")[-1]}_thumb.jpg', thumb_file, save=False)
            # Create small version
            small_size = (100, 100)
            small_img = img.copy()
            small_img.thumbnail(small_size)
            small_bytes = BytesIO()
            small_img.save(small_bytes, format='JPEG')
            small_file = ContentFile(small_bytes.getvalue())
            self.small.save(f'{self.cover.name.split("/")[-1]}_small.jpg', small_file, save=False)
        super(Track, self).save(*args, **kwargs)
    
    def visits(self):
        return self.hits.all().count()
        
    preview_url.short_description = "پیش‌نمایش"
    objects=TrackManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name='موزیک'
        verbose_name_plural='موزیک ها'

class TrackFile(models.Model):
    track=models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        related_name='track_files',
    )
    caption=models.CharField(
        max_length=250,
        verbose_name='عنوان',
    )
    track_file=models.FileField(
        upload_to='music/track_file',
        verbose_name='اپلود فایل'
    )

    listen_online=models.BooleanField(
        default=False,
        verbose_name='انلاین گوش بده',
        help_text='اگر میخواهید کاربرها این فایل را به صورت آنلاین گوش دهند این گزینه را انتخاب کنید.'
    )

    def __str__(self):
        return self.track.title
        
    class Meta:
        verbose_name='فایل موزیک'
        verbose_name_plural='فایل موزیک ها'

class OriginalLinkTrack(models.Model):
    MUSIC_PLATFORM=(
        ('link_youtube','YouTube'),
        ('link_spotify','Spotify'),
        ('link_soundclud','SoundCloud'),
    )
    track=models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        related_name='original_link_tracks',
    )
    music_platform_name=models.CharField(
        choices=MUSIC_PLATFORM,
        max_length=50,
        verbose_name='شبکه اجتماعی',
        help_text='نام شبکه اجتماعی را وارد کنید',
    )
    music_link=models.URLField(
        max_length=500,
        verbose_name='لینک اصلی موزیک را وارد کنید',
    )

    def __str__(self):
        return 'لینک اصلی' + self.track.title 

    class Meta:
        verbose_name='لینک اصلی آهنگ'
        verbose_name_plural='لینک اصلی آهنگ ها'
        
