
from django.db import models
from django.db.models import Count,Avg,Q,F
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
from site_control.resize_img import ResizeImage
from django.core.exceptions import ValidationError
from django.utils.text import slugify

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
        default=False,
        verbose_name='منتشر شود؟',
    )
    slug=models.SlugField(
        max_length=250,
        unique=True,
        verbose_name='لینک',
        null=True,
        blank=True,
        allow_unicode=True,
    )
    class Meta:
        abstract=True


class TrackManager(models.Manager):

    def active(self):
        return self.filter(
            status=True,
            published__lte=timezone.now()
        )

    def best_tracks(self):
        return self.active().filter(track_files__isnull=False).annotate(
            num_hits=Count('hits',distinct=True)*2 ,num_comment=Count('comments',distinct=True),
            avg_score=(F('num_hits') + F('num_comment'))
        ).distinct().order_by('-avg_score')

class IpAddress(AbstractDateFeild):
	ip_address = models.GenericIPAddressField(verbose_name='آدرس')
	def __str__(self):
		return self.ip_address
	class Meta:
		verbose_name = "آی‌پی"
		verbose_name_plural = "آی‌پی ها"


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
    lyrics=RichTextField(
        verbose_name='متن آهنگ',
        null=True,
        blank=True,
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
    hits=models.ManyToManyField(
        IpAddress,
    )
    published=models.DateTimeField(
        default=timezone.now,
        verbose_name='زمان انتشار',
    )
    comments=GenericRelation('comment.Comment')
    
    def clean(self):
        if self.cover:
            img=Image.open(self.cover)
            if img.format == 'GIF':
                raise ValidationError({'cover':'فایل گیف مجاز نیست'})

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
            "<a href='{}' target='blank'>پیش‌نمایش</a>".format(reverse("music:preview_detail",
             kwargs={'slug': self.slug}))
        )
    preview_url.short_description = "پیش‌نمایش"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title,allow_unicode=True)
            
        if not self.status:
            self.banners.update(status=False)
            
        if self.cover:
            resize_img=ResizeImage(self.cover)
            resize_img.save_cover(self.cover,(480, 480))
            resize_img.save_thumbnail(self.thumbnail,(272, 272))
            resize_img.save_small(self.small,(120, 120))
                
        super(Track, self).save(*args, **kwargs)
    
    def visits(self):
        return self.hits.all().count()

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
        
