# Generated by Django 3.2 on 2023-03-22 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackfile',
            name='online_catpion',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان برای پخش آنلاین'),
        ),
    ]
