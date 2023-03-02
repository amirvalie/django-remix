from django.db import models
from ckeditor.fields import RichTextField 

# Create your models here.

class AboutUs(models.Model):
    description=RichTextField(
        verbose_name='توضحیات'
    )
    picture=models.ImageField(
        upload_to='image/profile',
        verbose_name='عکس پروفایل'
    )
    def __str__(self):
        return 'درباره'
    
    class Meta:
        verbose_name='درباره'
        verbose_name_plural='درباره'
        
class Contact(models.Model):
    name=models.CharField(
        max_length=20,
        verbose_name='نام'
    )
    email=models.EmailField(
        verbose_name='ایمیل'
    )
    title=models.CharField(
        max_length=250,
        verbose_name='عنوان'
    )
    description=RichTextField(
        verbose_name='توضیحات',
    )
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='ارتباط '
        verbose_name_plural='ارتباط ها'
