# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-20 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('rxncon_system', '0002_rxncon_system_project_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rxncon_system',
            name='pickled_system',
            field=models.BinaryField(),
        ),
    ]
