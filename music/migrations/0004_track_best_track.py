# Generated by Django 3.2 on 2023-04-01 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_alter_trackfile_online_catpion'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='best_track',
            field=models.BooleanField(default=False, help_text='اگر میخواهید این آهنگ جزو بهترین ها باشد این گزینه را فعال کنید.', verbose_name='بهترین آهنگ'),
        ),
    ]
