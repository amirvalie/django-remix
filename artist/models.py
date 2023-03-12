from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor.fields import RichTextField 
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from music.models import AbstractCommonField,AbstractDateFeild


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
    picture=models.ImageField(
        upload_to='images/artists/profile',
        verbose_name='عکس هنرمند',
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
    objects=ArtistManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("artist:single-bio", args=[self.slug])

    def picture_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.thumbnail.url))
    picture_tag.short_description = " عکس هنرمند"

    def save(self,**kwargs):
        if self.picture:
            img = Image.open(self.picture)
            # Create thumbnail
            thumb_size = (272, 272)
            thumb_img = img.copy()
            thumb_img.thumbnail(thumb_size)
            thumb_bytes = BytesIO() 
            thumb_img.save(thumb_bytes, format='JPEG')
            thumb_file = ContentFile(thumb_bytes.getvalue())
            self.thumbnail.save(f'{self.picture.name.split("/")[-1]}_thumb.jpg', thumb_file, save=False)
            #Create Small
            small_size = (100, 100)
            small_img = img.copy()
            small_img.thumbnail(small_size)
            small_bytes = BytesIO()
            small_img.save(small_bytes, format='JPEG')
            small_file = ContentFile(small_bytes.getvalue())
            self.small.save(f'{self.picture.name.split("/")[-1]}_small.jpg', small_file, save=False)
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
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    class Meta:
        verbose_name='شبکه اجتماعی'
        verbose_name_plural='شبکه های اجتماعی'


