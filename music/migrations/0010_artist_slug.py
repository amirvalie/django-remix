# Generated by Django 3.2 on 2023-02-15 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_auto_20230215_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='slug',
            field=models.SlugField(default='titile', max_length=250, unique=True, verbose_name='لینک'),
            preserve_default=False,
        ),
    ]