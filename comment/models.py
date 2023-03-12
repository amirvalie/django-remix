from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from ckeditor.fields import RichTextField 
from music.models import AbstractDateFeild
now=timezone.now()


class ModelWithComment(models.Model):
    contet_type=models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'app_label__in':['music','artist'],
            'model__in':('artist','track')
        },
        verbose_name='مدل ها'
    )
    class Meta:
        verbose_name='مدل کامنت دار'
        verbose_name_plural='مدل های کامنت دار'

class Comment(AbstractDateFeild):
    email=models.EmailField(
        blank=True,
        null=True,
        verbose_name='ایمیل'
    )
    username=models.CharField(
        max_length=50,
        blank=True,
        verbose_name='نام کاربری',
    )
    content = RichTextField(
        verbose_name='توضیحات'
    )
    status=models.BooleanField(
        default=False,
        verbose_name='وضعیت',
    )
    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={
            'app_label__in':['music','artist'],
            'model__in':('artist','track')
        },
        verbose_name='مدل را انتخاب کنید'
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='شی مدل را انتخاب کنید'
    )
    content_object = GenericForeignKey()

    def __str__(self):
        return self.username
    class Meta:
        verbose_name='کامنت'
        verbose_name_plural='کامنت ها'

class Reply(AbstractDateFeild):
    username=models.CharField(
        max_length=50,
        verbose_name='نام کاربری',
        default='Admin'
    )
    comment=models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )
    answer=RichTextField(
        verbose_name='پاسخ',
    )
    class Meta:
        verbose_name='پاسخ'
        verbose_name_plural='پاسخ ها'


