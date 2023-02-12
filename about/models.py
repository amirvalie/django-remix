from django.db import models

# Create your models here.

class About(models.Model):
    description=models.TextField(
        verbose_name='توضحیات'
    )
    picture=models.ImageField(
        upload_to='/',
        verbose_name='عکس پروفایل'
    )
    
class Contact(models.Model):
    name=models.CharField(
        max_length=20,
        verbose_name='نام'
    )
    email=models.EmailField()
    title=models.CharField(
        max_length=250,
        verbose_name='عنوان'
    )
    description=models.TextField(
        verbose_name='توضیحات',
    )
