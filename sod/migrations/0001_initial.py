# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-21 22:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('purpose', models.CharField(choices=[('text', 'Текст'), ('image', 'Изображения'), ('music', 'Музыка'), ('crypto', 'Крипта')], max_length=100)),
                ('file', models.FileField(upload_to='sod/files/')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('extension', models.CharField(choices=[('m', 'Matlab'), ('py', 'Python'), ('exe', 'Execution')], max_length=10)),
                ('purpose', models.CharField(choices=[('text', 'Текст'), ('image', 'Изображения'), ('music', 'Музыка'), ('crypto', 'Крипта')], max_length=100)),
                ('file', models.FileField(upload_to='sod/modules/')),
                ('description', models.TextField()),
            ],
        ),
    ]
