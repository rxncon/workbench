# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-12 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileTree', '0002_auto_20160310_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='loaded',
            field=models.BooleanField(default=False),
        ),
    ]