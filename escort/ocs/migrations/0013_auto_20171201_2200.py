# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-01 19:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocs', '0012_auto_20171128_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='performer',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]