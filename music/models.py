from django.db import models
from django.utils import timezone
from extentions.utils import jalali_converter
class TrackManager(models.Manager):
	def active(self):
		return self.filter(status=True)
class CategoryManager(models.Manager):
	def active(self):
		return self.filter(status=True)
    
class Category(models.Model):
    parent=models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='والد',
    )
    title=models.CharField(
        max_length=250,
        verbose_name='عنوان',
    )
    slug=models.SlugField(
        max_length=250,
        verbose_name='لینک',
    )
    status=models.BooleanField(
        default=False,
        verbose_name='انتشار',
    )
    def save(self, *args, **kwargs):
        if not self.status:
            for track in self.tracks.published():
                track.status = 'd'
                track.save()
        super(Category, self).save(*args, **kwargs)

    objects=CategoryManager()
    class Meta:
        verbose_name='دسته بندی'
        verbose_name_plural='دسته بندی ها'

class Artist(models.Model):
    full_name=models.CharField(
        max_length=50,
        verbose_name='نام کامل',
        help_text='حداکثر 50 کاراکتر مجاز است',
    )
    decription=models.TextField(
        verbose_name='توضیحات',
    )
    picture=models.ImageField(
        upload_to='/artist',
        verbose_name='عکس هنرمند',
    )
    class Meta:
        verbose_name='هنرمند'
        verbose_name_plural='هنرمندان'

class IpAddress(models.Model):
	pub_date = models.DateTimeField('زمان اولین بازدید')
	ip_address = models.GenericIPAddressField(verbose_name='آدرس')

	class Meta:
		verbose_name = "آی‌پی"
		verbose_name_plural = "آی‌پی ها"
		ordering = ['pub_date']

	def __str__(self):
		return self.ip_address

class Track(models.Model):
    title=models.CharField(
        max_length=120,
        verbose_name='عنوان',
    )
    slug=models.SlugField(
        max_length=120,
        verbose_name='لینک',
    )
    category=models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='tracks',
        verbose_name='دسته بندی',
    )
    description=models.TextField()
    artist=models.ManyToManyField(
        Artist,
        verbose_name='خواننده(ها)',
    )
    thumbnail=models.ImageField(
        upload_to='/',
        verbose_name='بندانگشتی',
    )
    cover=models.ImageField(
        upload_to='/cover',
        verbose_name='کاور آهنگ',
    )
    best_song=models.BooleanField(
        default=True,
        verbose_name='آهنگ منتخب؟',
        help_text='اگر میخواهید این آهنگ در قسمت(بهترین هارا گوش داهید)قرار گیرد تیک را بزنید',
    )
    status=models.BooleanField(
        default=False,
        verbose_name='انتشار',
    )
    hits=models.ForeignKey(
        IpAddress,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        editable=False,
    )
    # comment=models.ForeignKey(
    #     '',
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    # )

    created = models.DateTimeField(auto_now_add=True)
    publish_time=models.DateTimeField(
        default=timezone.now()        
    )
    objects=TrackManager()

    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = "زمان انتشار"

    def preview_url(self):
        return format_html(
            "<a href='{}' target='blank'>پیش‌نمایش</a>".format(reverse("track:preview-detail",
             kwargs={'slug': self.slug}))
        )
    preview_url.short_description = "پیش‌نمایش"

    class Meta:
        verbose_name='موزیک'
        verbose_name_plural='موزیک ها'

class Banner(models.Model):
    track=models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        verbose_name='آهنگ',
        help_text='لطفا آهنگ مورد نظر خود را برای این بنر مشخص کنید',
    )
    caption=models.CharField(
        max_length=50,
        verbose_name='عنوان',
        help_text='حداکثر 50 کاراکتر مجاز است',
    )
    picture=models.ImageField(
        upload_to='/',
        verbose_name='عکس',
    )
    class Meta:
        verbose_name='بنر'
        verbose_name_plural='بنرها'


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


