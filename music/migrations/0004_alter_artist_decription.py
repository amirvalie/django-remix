# Generated by Django 3.2 on 2023-02-12 15:40

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_auto_20230212_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='decription',
            field=ckeditor.fields.RichTextField(verbose_name='توضیحات'),
        ),
    ]