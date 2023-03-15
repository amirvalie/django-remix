from django.db import models
from ckeditor.fields import RichTextField 
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.

class AboutMe(models.Model):
    description=RichTextField(
        verbose_name='توضحیات'
    )
    picture=models.ImageField(
        upload_to='images/about/profiles/',
        verbose_name='عکس پروفایل'
    )
    social_networks = GenericRelation('artist.SocialNetwork')

    def __str__(self):
        return 'درباره'
    
    class Meta:
        verbose_name='درباره'
        verbose_name_plural='درباره'
        
class Contact(models.Model):
    username=models.CharField(
        max_length=20,
        verbose_name='نام'
    )
    email=models.EmailField(
        verbose_name='ایمیل'
    )
    content=models.TextField(
        verbose_name='توضیحات',
    )
    def __str__(self):
        return self.username
    class Meta:
        verbose_name='ارتباط '
        verbose_name_plural='ارتباط ها'
