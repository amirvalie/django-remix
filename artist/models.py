from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor.fields import RichTextField 
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from music.models import AbstractCommonField,AbstractDateFeild
from django.utils.html import format_html
from site_control.resize_img import ResizeImage
from django.utils.text import slugify

class ArtistManager(models.Manager):
    def active(self):
        return self.filter(status=True)
        
class Artist(AbstractCommonField,AbstractDateFeild):
    name=models.CharField(
        max_length=50,
        verbose_name='نام',
        help_text='حداکثر 50 کاراکتر مجاز است',
    )
    category=models.ForeignKey(
        'category.ArtistCategory',
        on_delete=models.PROTECT,
        related_name='artists',
        verbose_name='دسته بندی',
    )
    decription=RichTextField(
        verbose_name='توضیحات',
    )
    cover=models.ImageField(
        upload_to='images/artists/cover',
        verbose_name='عکس هنرمند',
        help_text='ابعاد استاندارد عکس باید 300 * 300 باشد'
    )
    thumbnail=models.ImageField(
        upload_to='images/artists/thumbnails',
        verbose_name='عکس بندانگشتی',
        null=True,
        blank=True,
    )
    small = models.ImageField(
        upload_to='images/artists/smalls',
        null=True,
        blank=True,
    )
    social_networks = GenericRelation('SocialNetwork')
    comments = GenericRelation('comment.Comment')
    objects=ArtistManager()

    def __str__(self):
        return self.name
        
    def clean(self):
        if self.cover:
            img=Image.open(self.cover)
            if img.format == 'GIF':
                raise ValidationError({'cover':'فایل گیف مجاز نیست'})

    def get_absolute_url(self):
        return reverse("artist:artist_detail", args=[self.slug])

    def picture_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.small.url))
    picture_tag.short_description = " عکس هنرمند"

    def save(self,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name,allow_unicode=True)
        if self.cover:
            resize_img=ResizeImage(self.cover)
            resize_img.save(self.cover, (300,300))
            resize_img.save(self.thumbnail,(272, 272))
            resize_img.save(self.small,(120, 120))
        super(Artist, self).save(**kwargs)

    class Meta:
        verbose_name='هنرمند'
        verbose_name_plural='هنرمندان'

class SocialNetwork(models.Model):
    SOCIAL_MEDIA=(
        ('instagram','Instagram'),
        ('youtube','YouTube'),
        ('facebook','Facebook'),
        ('twitter','Twitter'),
        ('telegram','Telegram'),
        ('youtube','Aparat'),
        ('soundcloud','SoundCloud'),
        ('spotify','Spotify'),
    )
    social_network_name=models.CharField(
        choices=SOCIAL_MEDIA,
        max_length=50,
        verbose_name='شبکه اجتماعی',
        help_text='نام شبکه اجتماعی را وارد کنید',
    )
    url=models.URLField(
        max_length=500,
        verbose_name='لینک شبکه اجتماعی را وار',
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    class Meta:
        verbose_name='شبکه اجتماعی'
        verbose_name_plural='شبکه های اجتماعی'


