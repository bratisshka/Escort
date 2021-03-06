# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-27 20:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ocs', '0010_auto_20171124_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='performer',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='ocs.Task'),
        ),
    ]
