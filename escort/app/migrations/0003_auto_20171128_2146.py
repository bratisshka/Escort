# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-28 18:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20171128_2142'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='New',
            new_name='News',
        ),
    ]