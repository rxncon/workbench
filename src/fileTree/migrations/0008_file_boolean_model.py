# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-15 14:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boolean_model', '0001_initial'),
        ('fileTree', '0007_auto_20170313_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='boolean_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bool_file', to='boolean_model.Bool_from_rxnconsys'),
        ),
    ]
