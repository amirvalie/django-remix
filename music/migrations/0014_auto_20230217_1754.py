# Generated by Django 3.2 on 2023-02-17 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0013_auto_20230217_1731'),
    ]

    operations = [
        migrations.RenameField(
            model_name='track',
            old_name='publish_time',
            new_name='published',
        ),
        migrations.AddField(
            model_name='track',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='زمان اپدیت'),
        ),
        migrations.AlterField(
            model_name='track',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت'),
        ),
    ]