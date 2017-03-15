# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-13 20:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0008_auto_20170313_1937'),
        ('fileTree', '0006_auto_20160722_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='rea_graph',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reaction_graph_file', to='graphs.Graph_from_File'),
        ),
        migrations.AlterField(
            model_name='file',
            name='reg_graph',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='regulatory_graph_file', to='graphs.Graph_from_File'),
        ),
    ]