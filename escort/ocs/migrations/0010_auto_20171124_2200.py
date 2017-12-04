# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-24 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocs', '0009_auto_20171124_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subtask',
            name='deadline_date',
        ),
        migrations.RemoveField(
            model_name='subtask',
            name='start_date',
        ),
        migrations.AlterField(
            model_name='subtask',
            name='name',
            field=models.CharField(max_length=2000, verbose_name='Заголовок задачи'),
        ),
    ]