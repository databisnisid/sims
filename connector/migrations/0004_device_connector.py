# Generated by Django 4.0.5 on 2022-06-13 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0003_remove_device_type_device_parameter_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='connector',
            field=models.CharField(choices=[('SNMP', 'SNMP')], default='SNMP', max_length=20, verbose_name='Connector Type'),
        ),
    ]
