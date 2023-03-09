# Generated by Django 3.2 on 2023-03-09 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialnetwork',
            name='social_network_name',
            field=models.CharField(choices=[('instagram', 'Instagram'), ('youTube', 'YouTube'), ('facebook', 'Facebook'), ('twitter', 'Twitter'), ('telegram', 'Telegram')], help_text='نام شبکه اجتماعی را وارد کنید', max_length=50, verbose_name='شبکه اجتماعی'),
        ),
    ]
