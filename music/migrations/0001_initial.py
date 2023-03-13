# Generated by Django 3.2 on 2023-03-13 07:41

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('artist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='زمان اپدیت')),
                ('ip_address', models.GenericIPAddressField(verbose_name='آدرس')),
            ],
            options={
                'verbose_name': 'آی\u200cپی',
                'verbose_name_plural': 'آی\u200cپی ها',
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='زمان اپدیت')),
                ('status', models.BooleanField(default=True, verbose_name='منتشر شود؟')),
                ('slug', models.SlugField(allow_unicode=True, max_length=250, unique=True, verbose_name='لینک')),
                ('title', models.CharField(max_length=250, verbose_name='عنوان')),
                ('finglish_title', models.CharField(max_length=250, verbose_name='عنوان فینگلیشی')),
                ('description', ckeditor.fields.RichTextField(verbose_name='توضحیات')),
                ('cover', models.ImageField(help_text='توجه داشته باشید ابعاد عکس باید 480 * 480 باشد', upload_to='images/tracks/covers', verbose_name='کاور آهنگ')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='images/tracks/thumbnails/')),
                ('small', models.ImageField(blank=True, null=True, upload_to='images/tracks/smalls/')),
                ('best_song', models.BooleanField(default=True, help_text='اگر میخواهید این اهنگ در قسمت بهترین آهنگ ها قرار گیرد تیک این قسمت را بزنید.', verbose_name='آهنگ منتخب؟')),
                ('published', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان انتشار')),
                ('artists', models.ManyToManyField(blank=True, related_name='tracks', to='artist.Artist', verbose_name='هنرمندان')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tracks', to='category.trackcategory', verbose_name='دسته بندی')),
                ('hits', models.ManyToManyField(editable=False, to='music.IpAddress')),
            ],
            options={
                'verbose_name': 'موزیک',
                'verbose_name_plural': 'موزیک ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TrackFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=250, verbose_name='عنوان')),
                ('track_file', models.FileField(upload_to='music/track_file', verbose_name='اپلود فایل')),
                ('listen_online', models.BooleanField(default=False, help_text='اگر میخواهید کاربرها این فایل را به صورت آنلاین گوش دهند این گزینه را انتخاب کنید.', verbose_name='انلاین گوش بده')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track_files', to='music.track')),
            ],
            options={
                'verbose_name': 'فایل موزیک',
                'verbose_name_plural': 'فایل موزیک ها',
            },
        ),
        migrations.CreateModel(
            name='OriginalLinkTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music_platform_name', models.CharField(choices=[('link_youtube', 'YouTube'), ('link_spotify', 'Spotify'), ('link_soundclud', 'SoundCloud')], help_text='نام شبکه اجتماعی را وارد کنید', max_length=50, verbose_name='شبکه اجتماعی')),
                ('music_link', models.URLField(max_length=500, verbose_name='لینک اصلی موزیک را وارد کنید')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='original_link_tracks', to='music.track')),
            ],
            options={
                'verbose_name': 'لینک اصلی آهنگ',
                'verbose_name_plural': 'لینک اصلی آهنگ ها',
            },
        ),
    ]
