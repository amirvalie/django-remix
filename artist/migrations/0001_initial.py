# Generated by Django 3.2 on 2023-03-13 07:41

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialNetwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_network_name', models.CharField(choices=[('instagram', 'Instagram'), ('youtube', 'YouTube'), ('facebook', 'Facebook'), ('twitter', 'Twitter'), ('telegram', 'Telegram')], help_text='نام شبکه اجتماعی را وارد کنید', max_length=50, verbose_name='شبکه اجتماعی')),
                ('url', models.URLField(max_length=500, verbose_name='لینک شبکه اجتماعی را وار')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'شبکه اجتماعی',
                'verbose_name_plural': 'شبکه های اجتماعی',
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='زمان اپدیت')),
                ('status', models.BooleanField(default=True, verbose_name='منتشر شود؟')),
                ('slug', models.SlugField(allow_unicode=True, max_length=250, unique=True, verbose_name='لینک')),
                ('name', models.CharField(help_text='حداکثر 50 کاراکتر مجاز است', max_length=50, verbose_name='نام')),
                ('decription', ckeditor.fields.RichTextField(verbose_name='توضیحات')),
                ('picture', models.ImageField(upload_to='images/artists/profile', verbose_name='عکس هنرمند')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='images/artists/thumbnails', verbose_name='عکس بندانگشتی')),
                ('small', models.ImageField(blank=True, null=True, upload_to='images/artists/smalls')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='artists', to='category.artistcategory', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'هنرمند',
                'verbose_name_plural': 'هنرمندان',
            },
        ),
    ]
