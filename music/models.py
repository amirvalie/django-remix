from django.db import models
from django.utils import timezone
from extentions.utils import jalali_converter
from ckeditor.fields import RichTextField 
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
now=timezone.now()

class TrackManager(models.Manager):
    def active(self):
        return self.filter(
            status=True,
            published__lte=now,
        )
    def remix(self):
        return self.filter(
            status=True,
            music_type='remix',
            published__lte=now,
        )
    def podcast(self):
        return self.filter(
            status=True,
            music_type='podcasat',
            published__lte=now,
        )
    def best_songs(self):
        return self.filter(
            status=True,
            best_song=True,
            published__lte=now,
        )
    def number_of_hits(self):
        return self.active().annotate(
                count=Count('hits')
            )
class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)

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
    
class CategoryABC(AbstractCommonField):
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
                raise ValidationError({'parent':_('غیر مجاز! والد خود دارای والد دیگری میباشد.')})

    def __str__(self):
        return self.title
    class Meta:
        abstract=True
        verbose_name='دسته بندی'
        verbose_name_plural='دسته بندی ها'
class TrackCategory(CategoryABC):
    class Meta:
        verbose_name='دسته بندی موزیک'
        verbose_name_plural='دسته بندی موزیک ها'
    def save(self, *args, **kwargs):
        if not self.status:
            for track in self.tracks.active():
                track.status = False
                track.save()
        super(TrackCategory, self).save(*args, **kwargs)

class ArtistCategory(CategoryABC):
    class Meta:
        verbose_name='دسته بندی هنرمند'
        verbose_name_plural='دسته بندی هنرمند ها'

class Artist(AbstractCommonField):
    name=models.CharField(
        max_length=50,
        verbose_name='نام',
        help_text='حداکثر 50 کاراکتر مجاز است',
    )
    category=models.ManyToManyField(
        ArtistCategory,
        related_name='artists',
        verbose_name='دسته بندی',
        #null and blank should be false laster
    )
    decription=RichTextField(
        verbose_name='توضیحات',
    )
    picture=models.ImageField(
        upload_to='image/artist',
        verbose_name='عکس هنرمند',
    )
 
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("music:artist", args=[self.slug])

    def picture_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.picture.url))
    picture_tag.short_description = " عکس هنرمند"
    class Meta:
        verbose_name='هنرمند'
        verbose_name_plural='هنرمندان'

class IpAddress(models.Model):
	pub_date = models.DateTimeField('زمان اولین بازدید')
	ip_address = models.GenericIPAddressField(verbose_name='آدرس')

	def __str__(self):
		return self.ip_address
	class Meta:
		verbose_name = "آی‌پی"
		verbose_name_plural = "آی‌پی ها"
		ordering = ['pub_date']


class Track(AbstractCommonField):
    MUSIC_TYPE=(
        ('remix','ریمیکس'),
        ('podcasat','پادکست'),
        ('other','دیگر'),
    )
    title=models.CharField(
        max_length=250,
        verbose_name='عنوان',
    )
    category=models.ManyToManyField(
        TrackCategory,
        related_name='tracks',
        verbose_name='دسته بندی',
        #null and blank should be false laster
    )
    music_type=models.CharField(
        choices=MUSIC_TYPE,
        verbose_name='نوع موزیک',
        max_length=15,
        default='other',
        help_text='اگر نوع موزیک ریمیکس یا پادکست است یکی از این گزینه هارا انتخاب کنید در غیر این صورت گزینه دیگر را انتخاب کنید',
    )
    description=RichTextField(
        verbose_name='توضحیات'
    )
    thumbnail=models.ImageField(
        upload_to='image/thumbnail',
        verbose_name='بندانگشتی',
    )
    cover=models.ImageField(
        upload_to='image/cover',
        verbose_name='کاور آهنگ',
    )
    artists=models.ManyToManyField(
        Artist,
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
        blank=True,
        # editable=False,
    )
    published=models.DateTimeField(
        default=timezone.now,
        verbose_name='زمان انتشار',
    )
    created=models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان ساخت'
    )
    updated=models.DateTimeField(
        auto_now=True,
        verbose_name='زمان اپدیت',
    )

    def get_absolute_url(self):
        return reverse("music:track_detail", args=[self.slug])

    def jpublish(self):
        return jalali_converter(self.published)
    jpublish.short_description = "زمان انتشار"

    def listen_online(self):
        track_320=self.track_files.filter(track_quality='320').first()
        track_128=self.track_files.filter(track_quality='128').first()
        track_file=track_320 if track_320 else track_128
        return track_file

    def preview_url(self):
        return format_html(
            "<a href='{}' target='blank'>پیش‌نمایش</a>".format(reverse("track:preview-detail",
             kwargs={'slug': self.slug}))
        )

    preview_url.short_description = "پیش‌نمایش"
    objects=TrackManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='موزیک'
        verbose_name_plural='موزیک ها'

class TrackFile(models.Model):
    TRACK_QUALITY=(
        ('320','320'),
        ('128','128'),
    )
    track=models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        related_name='track_files',
    )
    caption=models.CharField(
        max_length=250,
        verbose_name='عنوان',
        default='مثال:دانلود آهنگ/پادکست با کیفیت 320',
    )
    track_quality=models.CharField(
        max_length=3,
        choices=TRACK_QUALITY,
        verbose_name='کیفیت آهنگ',
        blank=True,
        null=True,
    )
    track_file=models.FileField(
        upload_to='music/track_file',
        verbose_name='اپلود فایل'
    )

    def __str__(self):
        return self.track.title + 'کیفیت' + self.track_quality
        
    class Meta:
        verbose_name='فایل موزیک'
        verbose_name_plural='فایل موزیک ها'

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
        null=True,
        blank=True
    )
    status=models.BooleanField(
        default=True,
        verbose_name='منتشر شود؟',
    )
    picture=models.ImageField(
        upload_to='image/banner',
        verbose_name='عکس',
        help_text='توجه داشته باشید ابعاد عکس باید 280 * 1200 باشد'
    )
    def __str__(self):
        return 'بنر' + self.track.title
    class Meta:
        verbose_name='بنر'
        verbose_name_plural='بنرها'

class OriginalLinkTrack(models.Model):
    MUSIC_PLATFORM=(
        ('youTube.','YouTube'),
        ('spotify.','Spotify'),
        ('soundcloud','SoundCloud'),
    )
    track=models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
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

class ComingSoon(models.Model):
    caption=models.CharField(
        max_length=50,
        verbose_name='عنوان',
        help_text='حداکثر 50 کاراکتر مجاز است',
    )
    thumbnail=models.ImageField(
        upload_to='image/comming_soon',
        verbose_name='بندانگشتی',
    )
    status=models.BooleanField(
        default=True,
        verbose_name='منتشر شود؟',
    )
    relase_date=models.DateField(
        default=timezone.now,
        verbose_name='تاریخ انتشار',
    )
    class Meta:
        verbose_name='به زودی اضافه میشود '
        verbose_name_plural='به زودی اضافه میشوند'
    def __str__(self):
        return self.caption


