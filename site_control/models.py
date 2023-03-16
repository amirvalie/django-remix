from django.db import models
from django.contrib.contenttypes.models import ContentType
from category.models import TrackCategory
from music.models import (
    Track,
    AbstractDateFeild
)

class AbstractManageContent(AbstractDateFeild):
    FILTER_BASE=(
        ('time','زمان'),
        ('visit','بازدید')
    )
    title=models.CharField(
        max_length=250,
        verbose_name='عنوان'
    )
    status=models.BooleanField(
        default=True,
        verbose_name='وضعیت',
    )
    filter_base=models.CharField(
        choices=FILTER_BASE,
        max_length=5,
        verbose_name='فیلتر',
        help_text='در این قسمت شما میتوانید مشخص کنید که فیلتر بر اساس جدید ترین آیتم ها یا پربازدید ترین ها صورت بگیرد'
    )
    class Meta:
        abstract=True

# Create your models here.
class Banner(AbstractDateFeild):
    track=models.ForeignKey(
        Track,
        on_delete=models.PROTECT,
        verbose_name='آهنگ',
        help_text='لطفا آهنگ مورد نظر خود را برای این بنر مشخص کنید',
        related_name='banners',
    )
    caption=models.CharField(
        max_length=50,
        verbose_name='عنوان',
        help_text='حداکثر 50 کاراکتر مجاز است',
    )
    status=models.BooleanField(
        default=True,
        verbose_name='منتشر شود؟',
    )
    picture=models.ImageField(
        upload_to='images/banner',
        verbose_name='عکس',
        help_text='توجه داشته باشید ابعاد عکس باید 280 * 1200 باشد'
    )
    def __str__(self):
        return 'بنر' + self.track.title
    class Meta:
        verbose_name='بنر'
        verbose_name_plural='بنرها'

class ModelWithComment(models.Model):
    content_type=models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        limit_choices_to={
            'app_label__in':['music','artist','about'],
            'model__in':('artist','track','aboutme')
        },
        verbose_name='مدل ها'
    )
    class Meta:
        verbose_name='مدل کامنت دار'
        verbose_name_plural='مدل های کامنت دار'


class Sidebar(AbstractManageContent):
    category=models.ForeignKey(
        TrackCategory,
        on_delete=models.PROTECT,
        related_name='sidbars',
        verbose_name='دسته بندی',
    )
    class Meta:
        verbose_name='نوار کناری'
        verbose_name_plural='نوارهای کناری'

    def __str__(self):
        return self.title


class HomePage(AbstractManageContent):
    category=models.ForeignKey(
        TrackCategory,
        on_delete=models.PROTECT,
        related_name='home_contents',
        verbose_name='دسته بندی',
    )
    class Meta:
        verbose_name='مدیریت محتوای صفحه اصلی '
        verbose_name_plural='مدیریت محتوای صفحه اصلی '

    def __str__(self):
        return self.title