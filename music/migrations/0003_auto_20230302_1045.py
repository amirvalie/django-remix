# Generated by Django 3.2 on 2023-03-02 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_artist_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='ArtistCategory',
        ),
        migrations.CreateModel(
            name='TrackCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='منتشر شود؟')),
                ('slug', models.SlugField(allow_unicode=True, max_length=250, unique=True, verbose_name='لینک')),
                ('title', models.CharField(max_length=250, verbose_name='عنوان')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='music.trackcategory', verbose_name='والد')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='track',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tracks', to='music.trackcategory', verbose_name='دسته بندی'),
        ),
    ]
