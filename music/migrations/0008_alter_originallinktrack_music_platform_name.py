# Generated by Django 3.2 on 2023-03-04 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_auto_20230304_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='originallinktrack',
            name='music_platform_name',
            field=models.CharField(choices=[('link_youtube', 'YouTube'), ('link_spotify', 'Spotify'), ('link_soundclud', 'SoundCloud')], help_text='نام شبکه اجتماعی را وارد کنید', max_length=50, verbose_name='شبکه اجتماعی'),
        ),
    ]