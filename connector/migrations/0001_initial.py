# Generated by Django 4.0.5 on 2022-06-10 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Parameter Name')),
                ('connector', models.CharField(choices=[('SNMP', 'SNMP')], default='SNMP', max_length=20, verbose_name='Connector Type')),
                ('value', models.CharField(max_length=100, verbose_name='Parameter Value')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'parameter',
                'verbose_name_plural': 'parameter list',
                'db_table': 'parameter',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Merk DVR/NVR')),
                ('type', models.CharField(max_length=30, verbose_name='Type DVR/NVR')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parameter_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='parameter_1', to='connector.parameter', verbose_name='Parameter 1')),
                ('parameter_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='parameter_2', to='connector.parameter', verbose_name='Parameter 2')),
                ('parameter_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='parameter_3', to='connector.parameter', verbose_name='Parameter 3')),
                ('parameter_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='parameter_4', to='connector.parameter', verbose_name='Parameter 4')),
            ],
            options={
                'verbose_name': 'DVR/NVR',
                'verbose_name_plural': 'DVR/NVR List',
                'db_table': 'device',
            },
        ),
    ]
