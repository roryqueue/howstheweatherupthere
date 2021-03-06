# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-08 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_app', '0002_auto_20161208_0936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='wunderground_url_format',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.AddField(
            model_name='location',
            name='state_abbreviation',
            field=models.TextField(default='none'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='state',
            field=models.TextField(),
        ),
    ]
