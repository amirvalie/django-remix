# Generated by Django 3.2 on 2023-03-17 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0002_alter_contact_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='title',
            field=models.CharField(max_length=250, null=True, verbose_name='عنوان'),
        ),
    ]
