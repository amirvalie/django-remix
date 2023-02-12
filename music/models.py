from django.db import models
from django.utils import timezone

class Category(models.Model):
    title=models.CharField(
        max_length=120,
        verbose_name='عنوان'
    )
    slug=models.SlugField(
        max_length=120,
        verbose_name='لینک'
    )
    public=models.BooleanField(default=False)

    class Meta:
        verbose_name='دسته بندی'
        verbose_name_plural='دسته بندی ها'


class Banner(models.Model):
    caption=models.CharField(
        max_length=50,
        verbose_name='عنوان'
    )
    picture=models.ImageField(
        upload_to='/',
        verbose_name='عکس',
    )
    class Meta:
        verbose_name='بنر'
        verbose_name_plural='بنرها'

class Artist(models.Model):
    full_name=models.CharField(
        max_length=50,
        verbose_name='نام کامل',
        help_text='در این قسمت اگر نیاز است نام کامل را بنویسید.'
    )
    decription=models.TextField(
        verbose_name='توضیحات'
    )
    picture=models.ImageField(
        upload_to='/artist',
        verbose_name='عکس هنرمند',
    )
    class Meta:
        verbose_name='هنرمند'
        verbose_name_plural='هنرمندان'

class Track(models.Model):
    title=models.CharField(
        max_length=120,
        verbose_name='عنوان',
    )
    slug=models.SlugField(
        max_length=120,
        verbose_name='لینک'
    )
    category=models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='دسته بندی'
        )
    description=models.TextField()
    artist=models.ManyToManyField(
        Artist,
        verbose_name='خواننده(ها)',
    )
    cover=models.ImageField(
        upload_to='/cover',
        verbose_name='کاور آهنگ'
    )
    best_song=models.BooleanField(
        default=True,
        verbose_name='آهنگ منتخب؟',
        help_text='اگر میخواهید این آهنگ در قسمت(بهترین هارا گوش داهید)قرار گیرد تیک را بزنید'
    )
    visists=models.ForeignKey(
        '',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        editable=False
    )
    commands=models.ForeignKey(
        '',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created=models.DateField(default=timezone.now(),editable=False)
    publish_time=models.DateTimeField(
        default=timezone.now()        
    )

    class Meta:
        verbose_name='موزیک'
        verbose_name_plural='موزیک ها'


class TrackFile(models.Model):
    MUSIC_QUALITY=(
        ('128','دانلود ترک با کیفیت 128'),
        ('320','دانلود ترک با کیفیت 320'),
    )
    track=models.ForeignKey(
        Track,
        on_delete=models.SET_NULL,
    )
    track_quality=models.CharField(
        max_length=3,
        choices=QUALITY,
    )
    track_file=models.FileField(
        upload_to='/track_file',
        verbose_name='اپلود فایل'
    )
    class Meta:
        verbose_name='فایل موزیک'
        verbose_name_plural='فایل موزیک ها'

class OriginalLinkTrack(models.Model):
    MUSIC_PLATFORM=(
        ('youTube.','YouTube'),
        ('spotify.','Spotify'),
        ('soundcloud','SoundCloud'),
    )
    track=models.ForeignKey(
        Track,
        on_delete=models.SET_NULL,
    )
    music_platform_name=models.CharField(
        choices=MUSIC_PLATFORM,
        max_length=50,
        verbose_name='شبکه اجتماعی',
        help_text='نام شبکه اجتماعی را وارد کنید',
    )
    music_platform_link=models.URLField(
        max_length=500,
        verbose_name='لینک شبکه اجتماعی هنرمند را وار',
    )
    class Meta:
        verbose_name='لینک اصلی آهنگ'
        verbose_name_plural='لینک اصلی آهنگ ها'
    
class SocialNetwork(models.Model):
    SOCIAL_MEDIA=(
        ('instagram.','Instagram'),
        ('youTube.','YouTube'),
        ('facebook.','Facebook'),
        ('twitter.','Twitter'),
        ('telegram.','Telegram'),
    )
    social_network_name=models.CharField(
        choices=SOCIAL_MEDIA,
        max_length=50,
        verbose_name='شبکه اجتماعی',
        help_text='نام شبکه اجتماعی را وارد کنید',
    )
    url=models.URLField(
        max_length=500,
        verbose_name='لینک شبکه اجتماعی هنرمند را وار',
    )
    class Meta:
        verbose_name='شبکه اجتماعی'
        verbose_name_plural='شبکه های اجتماعی'

class CommingSoon(models.Model):
    caption=models.CharField(
        max_length=50,
        verbose_name='عنوان',
        help_text='حداکثر 50 کاراکتر مجاز است',
    )
    thumbnail=models.ImageField(
        upload_to='/',
        verbose_name='بندانگشتی',
    )
    relase_date=models.DateField(
        default=timezone.now(),
        verbose_name='تاریخ انتشار',
    )


