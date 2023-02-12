# Generated by Django 3.2 on 2023-02-12 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='توضحیات')),
                ('picture', models.ImageField(upload_to='image/profile', verbose_name='عکس پروفایل')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='نام')),
                ('email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=250, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='توضیحات')),
            ],
        ),
    ]
