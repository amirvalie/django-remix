from django.db import models
from ckeditor.fields import RichTextField 
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse

# Create your models here.


class AboutWebsite(models.Model):
    logo=models.ImageField(
        upload_to='images/about/logo/',
        verbose_name='لوگو',
    )
    favicon=models.ImageField(
        upload_to='images/about/logo',
        verbose_name='فاویکون',
        null=True,
        blank=True,
        help_text='ابعاد عکس 16 * 16',
    )
    name=models.CharField(
        max_length=100,
        verbose_name='نام وب سایت'
    )
    description=RichTextField(
        verbose_name='توضیحات',
    )

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name='درباره وب سایت'
        verbose_name_plural='درباره وب سایت'

class AboutMe(models.Model):
    name=models.CharField(
        max_length=50,
        default='DJ Movan',
        verbose_name='نام',
    )
    description=RichTextField(
        verbose_name='توضحیات',
    )
    picture=models.ImageField(
        upload_to='images/about/profiles',
        verbose_name='عکس پروفایل',
    )
    social_networks = GenericRelation('artist.SocialNetwork')
    comments = GenericRelation('comment.Comment')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('about:about_me')

    class Meta:
        verbose_name='درباره من'
        verbose_name_plural='درباره من'

class Contact(models.Model):
    username=models.CharField(
        max_length=20,
        verbose_name='نام',
    )
    email=models.EmailField(
        verbose_name='ایمیل',
    )
    title=models.CharField(
        max_length=250,
        verbose_name='عنوان',
        null=True,
    )
    content=models.TextField(
        verbose_name='توضیحات',
    )
    
    def __str__(self):
        return self.username

    class Meta:
        verbose_name='ارتباط '
        verbose_name_plural='ارتباطات'
