# Generated by Django 3.2 on 2023-03-13 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('music', '0001_initial'),
        ('category', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sidebar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='زمان اپدیت')),
                ('title', models.CharField(max_length=250, verbose_name='عنوان')),
                ('status', models.BooleanField(default=True, verbose_name='وضعیت')),
                ('filter_base', models.CharField(choices=[('time', 'زمان'), ('visit', 'بازدید')], help_text='در این قسمت شما میتوانید مشخص کنید که فیلتر بر اساس جدید ترین آیتم ها یا پربازدید ترین ها صورت بگیرد', max_length=5, verbose_name='فیلتر')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sidbars', to='category.trackcategory', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'نوار کناری',
                'verbose_name_plural': 'نوارهای کناری',
            },
        ),
        migrations.CreateModel(
            name='ModelWithComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.ForeignKey(limit_choices_to={'app_label__in': ['music', 'artist'], 'model__in': ('artist', 'track')}, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='مدل ها')),
            ],
            options={
                'verbose_name': 'مدل کامنت دار',
                'verbose_name_plural': 'مدل های کامنت دار',
            },
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='زمان اپدیت')),
                ('title', models.CharField(max_length=250, verbose_name='عنوان')),
                ('status', models.BooleanField(default=True, verbose_name='وضعیت')),
                ('filter_base', models.CharField(choices=[('time', 'زمان'), ('visit', 'بازدید')], help_text='در این قسمت شما میتوانید مشخص کنید که فیلتر بر اساس جدید ترین آیتم ها یا پربازدید ترین ها صورت بگیرد', max_length=5, verbose_name='فیلتر')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_contents', to='category.trackcategory', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'مدیریت محتوای صفحه',
                'verbose_name_plural': 'مدیریت محتوای صفحه',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='زمان اپدیت')),
                ('caption', models.CharField(help_text='حداکثر 50 کاراکتر مجاز است', max_length=50, verbose_name='عنوان')),
                ('status', models.BooleanField(default=True, verbose_name='منتشر شود؟')),
                ('picture', models.ImageField(help_text='توجه داشته باشید ابعاد عکس باید 280 * 1200 باشد', upload_to='image/banner', verbose_name='عکس')),
                ('track', models.ForeignKey(help_text='لطفا آهنگ مورد نظر خود را برای این بنر مشخص کنید', on_delete=django.db.models.deletion.CASCADE, related_name='banners', to='music.track', verbose_name='آهنگ')),
            ],
            options={
                'verbose_name': 'بنر',
                'verbose_name_plural': 'بنرها',
            },
        ),
    ]
