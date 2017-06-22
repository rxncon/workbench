# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-20 20:57
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('quick_format', '0003_auto_20170520_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quick',
            name='rxncon_system',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                       related_name='rxncon_system_quick', to='rxncon_system.Rxncon_system'),
        ),
    ]
