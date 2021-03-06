# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-29 15:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dependancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Имя модуля')),
                ('extension', models.CharField(choices=[('m', 'Matlab'), ('py', 'Python'), ('exe', 'Execution')], max_length=10, verbose_name='Расширение')),
                ('purpose', models.CharField(choices=[('text', 'Текст'), ('image', 'Изображения'), ('music', 'Музыка'), ('crypto', 'Крипта')], max_length=100, verbose_name='Тип входящих файлов')),
                ('directory_name', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField(verbose_name='Описание')),
                ('periodic', models.IntegerField(default=60, verbose_name='Периодичность')),
                ('timeout', models.IntegerField(default=10, verbose_name='Таймаут')),
                ('state', models.CharField(choices=[('run', 'Running'), ('stop', 'Stopped')], default='stop', max_length=20, verbose_name='Состояние')),
                ('sended_files', models.IntegerField(default=0, verbose_name='Количество посланных файлов')),
                ('is_service', models.BooleanField(default=False, verbose_name='Служебный?')),
                ('output_modules', models.ManyToManyField(blank=True, related_name='input_modules', through='sod.Dependancy', to='sod.Module')),
            ],
            options={
                'verbose_name_plural': 'модули',
                'verbose_name': 'модуль',
            },
        ),
        migrations.AddField(
            model_name='dependancy',
            name='input_module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='sod.Module'),
        ),
        migrations.AddField(
            model_name='dependancy',
            name='output_module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='sod.Module'),
        ),
    ]
