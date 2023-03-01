# Generated by Django 3.2 on 2023-03-01 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0017_auto_20230226_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackfile',
            name='track_quality',
            field=models.CharField(choices=[('128', 'دانلود ریمیکس با کیفیت 128'), ('320', 'دانلود ریمیکس با کیفیت 320'), ('128', 'دانلود پادکست با کیفیت 128'), ('320', 'دانلود پادکست با کیفیت 320')], max_length=3, verbose_name='کیفیت آهنگ'),
        ),
    ]
