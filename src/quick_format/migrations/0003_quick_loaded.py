# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-12 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quick_format', '0002_remove_quick_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='quick',
            name='loaded',
            field=models.BooleanField(default=False),
        ),
    ]
