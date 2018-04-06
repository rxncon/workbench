# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-04-06 11:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import fileTree.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boolean_model', '__first__'),
        ('rule_based', '__first__'),
        ('rxncon_system', '__first__'),
        ('graphs', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=120)),
                ('loaded', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True)),
                ('file', models.FileField(upload_to=fileTree.models.upload_location)),
                ('comment', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('boolean_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bool_file', to='boolean_model.Bool_from_rxnconsys')),
                ('rea_graph', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reaction_graph_file', to='graphs.Graph_from_File')),
                ('reg_graph', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='regulatory_graph_file', to='graphs.Graph_from_File')),
                ('rule_based_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rule_based_file', to='rule_based.Rule_based_from_rxnconsys')),
                ('rxncon_system', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rxncon_system_file', to='rxncon_system.Rxncon_system')),
                ('sRea_graph', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='species reaction_graph_file+', to='graphs.Graph_from_File')),
            ],
            options={
                'ordering': ['-updated', '-timestamp'],
            },
        ),
    ]
