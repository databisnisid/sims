# Generated by Django 4.0.5 on 2022-06-10 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_remove_location_channel_1_remove_location_channel_2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='ping_status',
            field=models.BooleanField(default=True, verbose_name='Ping Status'),
        ),
    ]
