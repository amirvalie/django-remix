# Generated by Django 3.2 on 2023-03-04 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_alter_originallinktrack_music_platform_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='finglish_title',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان فینگلیشی'),
        ),
        migrations.AddField(
            model_name='track',
            name='finglish_title',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان فینگلیشی'),
        ),
    ]