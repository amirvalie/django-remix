# Generated by Django 3.2 on 2023-04-16 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialnetwork',
            name='social_network_name',
            field=models.CharField(choices=[('instagram', 'Instagram'), ('youtube', 'YouTube'), ('facebook', 'Facebook'), ('twitter', 'Twitter'), ('telegram', 'Telegram'), ('youtube', 'Aparat'), ('soundcloud', 'SoundCloud'), ('spotify', 'Spotify')], help_text='نام شبکه اجتماعی را وارد کنید', max_length=50, verbose_name='شبکه اجتماعی'),
        ),
    ]
