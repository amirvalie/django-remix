# Generated by Django 3.2 on 2023-02-12 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CommingSoon',
            new_name='ComingSoon',
        ),
        migrations.AlterModelOptions(
            name='comingsoon',
            options={'verbose_name': 'به زودی اضافه میشود ', 'verbose_name_plural': 'به زودی اضافه میشوند'},
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music.category', verbose_name='والد'),
        ),
    ]