# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sod', '0004_module_output_modules'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='directory_name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]